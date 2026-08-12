"""Atomic canonical run-state persistence and contract ingestion."""

from __future__ import annotations

import json
import os
import sys
from contextlib import contextmanager
from dataclasses import replace
from datetime import datetime, timezone
from functools import wraps
from pathlib import Path
from typing import Any, Iterable, Iterator, Mapping
from uuid import uuid4

from .authorization import (
    authorize_changed_files,
    authorize_result,
    ensure_repository_bounded,
    normalize_repo_path,
)
from .contracts import (
    ResultContract,
    ResultStatus,
    ReviewContract,
    ReviewOutcome,
    TaskContract,
    validate_result_against_task,
    validate_review_against_result,
)
from .errors import RecoveryError, StateTransitionError, StaleWorkError
from .events import RunEvent
from .gitops import GitError, GitRepository
from .jsonutil import canonical_json, load_json, write_json_atomic
from .jsonutil import digest_json
from .security import scan_for_secrets
from .state import RunState, RunStateValue, TaskRuntime, TaskState


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")


class ReviewAttestation:
    """Trusted root-channel approval kept separate from untrusted review JSON."""

    def __init__(self, source: str, principal: str, invocation_id: str):
        if source not in {"human-approved", "host-authenticated"}:
            raise RecoveryError("review attestation source is not trusted")
        if not principal.strip() or not invocation_id.strip():
            raise RecoveryError("review attestation principal and invocation id are required")
        self.source = source
        self.principal = principal
        self.invocation_id = invocation_id

    @classmethod
    def human(cls, principal: str) -> "ReviewAttestation":
        return cls("human-approved", principal, str(uuid4()))

    def to_dict(self) -> dict[str, str]:
        return {
            "source": self.source,
            "principal": self.principal,
            "invocation_id": self.invocation_id,
            "attested_at": utc_now(),
        }


def _locked(method: Any) -> Any:
    @wraps(method)
    def wrapper(self: "RunStore", run_id: str, *args: Any, **kwargs: Any) -> Any:
        with self._run_lock(run_id):
            return method(self, run_id, *args, **kwargs)

    return wrapper


class RunStore:
    def __init__(self, repository_root: Path):
        self.repository_root = repository_root.resolve()
        self.runs_root = ensure_repository_bounded(self.repository_root, ".eclipse/runs")

    def run_dir(self, run_id: str) -> Path:
        if not run_id or any(character not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789._-" for character in run_id):
            raise RecoveryError(f"invalid run id: {run_id!r}")
        return ensure_repository_bounded(self.runs_root, run_id)

    @_locked
    def create_run(
        self,
        run_id: str,
        objective: str,
        plan_digest: str,
        base_revision: str,
        *,
        metadata: Mapping[str, Any] | None = None,
    ) -> RunState:
        directory = self.run_dir(run_id)
        if directory.exists():
            raise StateTransitionError(f"run already exists: {run_id}")
        self._reject_secrets(metadata or {}, "run metadata")
        now = utc_now()
        state = RunState(
            run_id=run_id,
            objective=objective,
            plan_revision=1,
            plan_digest=plan_digest,
            base_revision=base_revision,
            status=RunStateValue.PLANNED,
            tasks={},
            created_at=now,
            updated_at=now,
            metadata=dict(metadata or {}),
        )
        self._save(state)
        self._event(state, "run.created", None, {"plan_revision": 1, "base_revision": base_revision})
        return state

    def load(self, run_id: str) -> RunState:
        path = self.run_dir(run_id) / "run.json"
        if not path.is_file():
            raise RecoveryError(f"run state not found: {path}")
        value = load_json(path)
        if not isinstance(value, dict):
            raise RecoveryError("run.json must contain an object")
        state = RunState.from_dict(value)
        if state.run_id != run_id:
            raise RecoveryError(
                f"run state identity mismatch: requested {run_id!r}, found {state.run_id!r}"
            )
        return state

    @_locked
    def add_task(self, run_id: str, task: TaskContract) -> RunState:
        state = self.load(run_id)
        self._assert_current(state, task.run_id, task.plan_revision, task.plan_digest)
        self._reject_secrets(task.data, "task contract")
        provenance = task.data["provenance"]
        assert isinstance(provenance, Mapping)
        if provenance.get("base_revision") != state.base_revision:
            raise StaleWorkError("task base revision does not match canonical run base")
        relative = f"contracts/{task.task_id}.json"
        now = utc_now()
        runtime = TaskRuntime(
            task_id=task.task_id,
            contract_file=relative,
            contract_digest=task.digest,
            plan_revision=task.plan_revision,
            dependencies=task.dependencies,
            state=TaskState.PLANNED,
            attempt=0,
            review_rounds=0,
            result_files=(),
            review_files=(),
            updated_at=now,
        )
        state = state.add_task(runtime, updated_at=now)
        self._write_immutable(self._run_record_path(run_id, relative), task.data)
        self._save(state)
        self._event(state, "task.added", task.task_id, {"contract_digest": task.digest})
        return state

    @_locked
    def start_task(self, run_id: str, task_id: str) -> RunState:
        state = self.load(run_id)
        runtime = self._task(state, task_id)
        if runtime.attempt >= self._task_budget(run_id, runtime, "max_attempts"):
            raise StateTransitionError(f"attempt budget exhausted for {task_id}")
        now = utc_now()
        updated = runtime.transition(TaskState.RUNNING, updated_at=now)
        updated = replace(updated, attempt=updated.attempt + 1)
        state = state.update_task(updated, updated_at=now)
        self._save(state)
        self._event(state, "task.started", task_id, {"attempt": updated.attempt})
        return state

    @_locked
    def ingest_result(
        self,
        run_id: str,
        result: ResultContract,
        *,
        observed_files: Iterable[str] | None = None,
    ) -> RunState:
        state = self.load(run_id)
        runtime = self._task(state, result.task_id)
        task = self.load_task(run_id, result.task_id)
        self._assert_current(
            state,
            str(result.data["run_id"]),
            int(result.data["plan_revision"]),
            str(result.data["plan_digest"]),
        )
        if runtime.state is not TaskState.RUNNING:
            raise StateTransitionError(f"task {result.task_id} is not running")
        if int(result.data["attempt"]) != runtime.attempt:
            raise StaleWorkError("result attempt does not match active task attempt")
        validate_result_against_task(result, task)
        observed = self._observe_changed_files(task, observed_files)
        reported = tuple(sorted(str(item) for item in result.data["files_changed"]))
        if observed != reported:
            raise StaleWorkError(
                f"worker-reported files do not match trusted observation; "
                f"reported={list(reported)!r}, observed={list(observed)!r}"
            )
        git = result.data["git"]
        assert isinstance(git, Mapping)
        if git.get("changed_files_digest") != digest_json(list(observed)):
            raise StaleWorkError("changed-file observation digest does not match result")
        authorize_changed_files(task, observed)
        authorize_result(task, result)
        self._reject_secrets(result.data, "result contract")
        now = utc_now()
        relative = f"results/{result.task_id}-A{runtime.attempt}.json"
        self._write_immutable(self._run_record_path(run_id, relative), result.data)
        updated = replace(runtime, result_files=(*runtime.result_files, relative))
        if result.status is ResultStatus.COMPLETE:
            updated = updated.transition(TaskState.EVIDENCE_PENDING, updated_at=now)
            updated = updated.transition(TaskState.REVIEW_PENDING, updated_at=now)
        elif result.status is ResultStatus.BLOCKED:
            updated = updated.transition(TaskState.BLOCKED, updated_at=now)
        elif result.status is ResultStatus.ESCALATED:
            updated = updated.transition(TaskState.ESCALATED, updated_at=now)
        else:
            updated = updated.transition(TaskState.FAILED, updated_at=now)
        state = state.update_task(updated, updated_at=now)
        self._save(state)
        self._event(state, "result.ingested", result.task_id, {"status": result.status.value})
        return state

    @_locked
    def ingest_review(
        self,
        run_id: str,
        review: ReviewContract,
        *,
        attestation: ReviewAttestation,
    ) -> RunState:
        state = self.load(run_id)
        runtime = self._task(state, review.task_id)
        if runtime.state is not TaskState.REVIEW_PENDING:
            raise StateTransitionError(f"task {review.task_id} is not pending review")
        task = self.load_task(run_id, review.task_id)
        result = self.load_result(run_id, runtime.result_files[-1])
        validate_review_against_result(review, result, task)
        self._reject_secrets(review.data, "review contract")
        expected_round = runtime.review_rounds + 1
        if review.data["review_round"] != expected_round:
            raise StaleWorkError(f"expected review round {expected_round}")
        if expected_round > self._task_budget(run_id, runtime, "max_review_rounds"):
            raise StateTransitionError(f"review budget exhausted for {review.task_id}")
        now = utc_now()
        relative = f"reviews/{review.task_id}-R{expected_round}.json"
        self._write_immutable(self._run_record_path(run_id, relative), review.data)
        attestation_relative = f"reviews/{review.task_id}-R{expected_round}.attestation.json"
        self._write_immutable(
            self._run_record_path(run_id, attestation_relative), attestation.to_dict()
        )
        updated = replace(
            runtime,
            review_rounds=expected_round,
            review_files=(*runtime.review_files, relative),
        )
        if review.outcome is ReviewOutcome.ACCEPTED:
            updated = updated.transition(TaskState.ACCEPTED, updated_at=now)
        elif review.outcome is ReviewOutcome.CHANGES_REQUESTED:
            updated = updated.transition(TaskState.CHANGES_REQUESTED, updated_at=now)
            updated = updated.transition(TaskState.READY_FOR_CORRECTION, updated_at=now)
        elif review.outcome is ReviewOutcome.ESCALATED:
            updated = updated.transition(TaskState.ESCALATED, updated_at=now)
        else:
            updated = updated.transition(TaskState.FAILED, updated_at=now)
        state = state.update_task(updated, updated_at=now)
        self._save(state)
        self._event(
            state,
            "review.ingested",
            review.task_id,
            {"outcome": review.outcome.value, "attestation_source": attestation.source},
        )
        return state

    @_locked
    def revise_plan(self, run_id: str, new_digest: str, base_revision: str) -> RunState:
        state = self.load(run_id).revise_plan(
            new_digest,
            base_revision=base_revision,
            updated_at=utc_now(),
        )
        self._save(state)
        self._event(state, "plan.revised", None, {"plan_revision": state.plan_revision})
        return state

    def load_task(self, run_id: str, task_id: str) -> TaskContract:
        runtime = self._task(self.load(run_id), task_id)
        value = load_json(self._run_record_path(run_id, runtime.contract_file))
        if not isinstance(value, dict):
            raise RecoveryError("task contract must be an object")
        task = TaskContract.from_dict(value)
        if task.digest != runtime.contract_digest:
            raise RecoveryError(f"task contract digest mismatch: {task_id}")
        return task

    def load_result(self, run_id: str, relative: str) -> ResultContract:
        value = load_json(self._run_record_path(run_id, relative))
        if not isinstance(value, dict):
            raise RecoveryError("result contract must be an object")
        return ResultContract.from_dict(value)

    def _task(self, state: RunState, task_id: str) -> TaskRuntime:
        try:
            return state.tasks[task_id]
        except KeyError as error:
            raise StateTransitionError(f"unknown task: {task_id}") from error

    def _task_budget(self, run_id: str, runtime: TaskRuntime, field: str) -> int:
        task = self.load_task(run_id, runtime.task_id)
        budgets = task.data["budgets"]
        assert isinstance(budgets, Mapping)
        return int(budgets[field])

    def _run_record_path(self, run_id: str, relative: str) -> Path:
        return ensure_repository_bounded(self.run_dir(run_id), relative)

    def _observe_changed_files(
        self, task: TaskContract, observed_files: Iterable[str] | None
    ) -> tuple[str, ...]:
        if observed_files is not None:
            return tuple(sorted(normalize_repo_path(str(item)) for item in observed_files))
        if not (self.repository_root / ".git").exists():
            raise RecoveryError(
                "trusted changed-file observation is required outside a Git working tree"
            )
        provenance = task.data["provenance"]
        assert isinstance(provenance, Mapping)
        try:
            return GitRepository(self.repository_root).changed_files(
                str(provenance["base_revision"])
            )
        except GitError as error:
            raise RecoveryError(f"could not observe changed files: {error}") from error

    @contextmanager
    def _run_lock(self, run_id: str) -> Iterator[None]:
        lock = ensure_repository_bounded(self.runs_root, f".locks/{run_id}.lock")
        lock.parent.mkdir(parents=True, exist_ok=True)
        handle = lock.open("a+b")
        try:
            if sys.platform == "win32":  # pragma: no cover - exercised on Windows CI
                import msvcrt

                handle.seek(0)
                if handle.read(1) == b"":
                    handle.write(b"0")
                    handle.flush()
                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_LOCK, 1)
            else:  # pragma: no cover - platform branch
                import fcntl

                fcntl.flock(handle.fileno(), fcntl.LOCK_EX)
            yield
        finally:
            if sys.platform == "win32":  # pragma: no cover - exercised on Windows CI
                import msvcrt

                handle.seek(0)
                msvcrt.locking(handle.fileno(), msvcrt.LK_UNLCK, 1)
            else:  # pragma: no cover - platform branch
                import fcntl

                fcntl.flock(handle.fileno(), fcntl.LOCK_UN)
            handle.close()

    @staticmethod
    def _reject_secrets(value: object, label: str) -> None:
        findings = scan_for_secrets(value)
        if findings:
            locations = ", ".join(f"{item.path}:{item.kind}" for item in findings)
            raise RecoveryError(f"{label} contains probable secret(s): {locations}")

    @staticmethod
    def _write_immutable(path: Path, value: object) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        serialized = json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
        try:
            with path.open("x", encoding="utf-8", newline="\n") as handle:
                handle.write(serialized)
                handle.flush()
                os.fsync(handle.fileno())
        except FileExistsError as error:
            existing = load_json(path)
            if canonical_json(existing) == canonical_json(value):
                raise RecoveryError(f"immutable record already exists: {path}") from error
            raise RecoveryError(f"refusing to overwrite immutable record: {path}") from error

    def _assert_current(self, state: RunState, run_id: str, revision: int, digest: str) -> None:
        if run_id != state.run_id:
            raise StaleWorkError(f"contract run {run_id!r} does not match {state.run_id!r}")
        if revision != state.plan_revision or digest != state.plan_digest:
            raise StaleWorkError(
                f"contract plan {revision}/{digest} does not match current "
                f"{state.plan_revision}/{state.plan_digest}"
            )

    def _save(self, state: RunState) -> None:
        write_json_atomic(self._run_record_path(state.run_id, "run.json"), state.to_dict())

    def _event(
        self,
        state: RunState,
        event_type: str,
        task_id: str | None,
        details: Mapping[str, Any],
    ) -> None:
        event = RunEvent(
            event_id=str(uuid4()),
            run_id=state.run_id,
            event_type=event_type,
            timestamp=utc_now(),
            task_id=task_id,
            details=details,
        )
        path = self._run_record_path(state.run_id, "events.jsonl")
        path.parent.mkdir(parents=True, exist_ok=True)
        with path.open("a", encoding="utf-8", newline="\n") as handle:
            handle.write(json.dumps(event.to_dict(), sort_keys=True) + "\n")
