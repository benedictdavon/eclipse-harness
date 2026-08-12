"""Explicit run/task lifecycle with plan revision binding."""

from __future__ import annotations

import re
from dataclasses import dataclass, replace
from enum import Enum
from typing import Any, Mapping

from .constants import STATE_SCHEMA_VERSION
from .errors import RecoveryError, StateTransitionError, StaleWorkError

_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")
_TASK_RUNTIME_FIELDS = {
    "task_id",
    "contract_file",
    "contract_digest",
    "plan_revision",
    "dependencies",
    "state",
    "attempt",
    "review_rounds",
    "result_files",
    "review_files",
    "updated_at",
}
_RUN_FIELDS = {
    "schema_version",
    "run_id",
    "objective",
    "plan_revision",
    "plan_digest",
    "base_revision",
    "status",
    "tasks",
    "created_at",
    "updated_at",
    "metadata",
}


def _exact_fields(data: Mapping[str, Any], expected: set[str], label: str) -> None:
    unknown = sorted(set(data) - expected)
    missing = sorted(expected - set(data))
    if unknown or missing:
        raise RecoveryError(f"invalid {label} fields; missing={missing}, unknown={unknown}")


def _string(data: Mapping[str, Any], key: str, label: str) -> str:
    value = data.get(key)
    if not isinstance(value, str) or not value:
        raise RecoveryError(f"{label}.{key} must be a non-empty string")
    return value


def _integer(data: Mapping[str, Any], key: str, minimum: int, label: str) -> int:
    value = data.get(key)
    if not isinstance(value, int) or isinstance(value, bool) or value < minimum:
        raise RecoveryError(f"{label}.{key} must be an integer >= {minimum}")
    return value


def _strings(data: Mapping[str, Any], key: str, label: str) -> tuple[str, ...]:
    value = data.get(key)
    if not isinstance(value, list) or any(not isinstance(item, str) for item in value):
        raise RecoveryError(f"{label}.{key} must be an array of strings")
    return tuple(value)


class TaskState(str, Enum):
    PLANNED = "planned"
    READY = "ready"
    RUNNING = "running"
    EVIDENCE_PENDING = "evidence_pending"
    REVIEW_PENDING = "review_pending"
    CHANGES_REQUESTED = "changes_requested"
    READY_FOR_CORRECTION = "ready_for_correction"
    ACCEPTED = "accepted"
    BLOCKED = "blocked"
    ESCALATED = "escalated"
    FAILED = "failed"
    SUPERSEDED = "superseded"


class RunStateValue(str, Enum):
    PLANNED = "planned"
    ACTIVE = "active"
    BLOCKED = "blocked"
    ACCEPTED = "accepted"
    FAILED = "failed"
    ABORTED = "aborted"


_TRANSITIONS: Mapping[TaskState, frozenset[TaskState]] = {
    TaskState.PLANNED: frozenset({TaskState.READY, TaskState.SUPERSEDED}),
    TaskState.READY: frozenset({TaskState.RUNNING, TaskState.BLOCKED, TaskState.SUPERSEDED}),
    TaskState.RUNNING: frozenset(
        {
            TaskState.EVIDENCE_PENDING,
            TaskState.BLOCKED,
            TaskState.ESCALATED,
            TaskState.FAILED,
            TaskState.SUPERSEDED,
        }
    ),
    TaskState.EVIDENCE_PENDING: frozenset(
        {TaskState.REVIEW_PENDING, TaskState.FAILED, TaskState.SUPERSEDED}
    ),
    TaskState.REVIEW_PENDING: frozenset(
        {
            TaskState.ACCEPTED,
            TaskState.CHANGES_REQUESTED,
            TaskState.ESCALATED,
            TaskState.FAILED,
            TaskState.SUPERSEDED,
        }
    ),
    TaskState.CHANGES_REQUESTED: frozenset(
        {
            TaskState.READY_FOR_CORRECTION,
            TaskState.ESCALATED,
            TaskState.FAILED,
            TaskState.SUPERSEDED,
        }
    ),
    TaskState.READY_FOR_CORRECTION: frozenset(
        {TaskState.RUNNING, TaskState.BLOCKED, TaskState.SUPERSEDED}
    ),
    TaskState.BLOCKED: frozenset(
        {TaskState.READY, TaskState.READY_FOR_CORRECTION, TaskState.ESCALATED, TaskState.FAILED}
    ),
    TaskState.ESCALATED: frozenset({TaskState.READY, TaskState.FAILED, TaskState.SUPERSEDED}),
    TaskState.ACCEPTED: frozenset(),
    TaskState.FAILED: frozenset(),
    TaskState.SUPERSEDED: frozenset(),
}


@dataclass(frozen=True)
class TaskRuntime:
    task_id: str
    contract_file: str
    contract_digest: str
    plan_revision: int
    dependencies: tuple[str, ...]
    state: TaskState
    attempt: int
    review_rounds: int
    result_files: tuple[str, ...]
    review_files: tuple[str, ...]
    updated_at: str

    def transition(self, target: TaskState, *, updated_at: str) -> "TaskRuntime":
        if target not in _TRANSITIONS[self.state]:
            raise StateTransitionError(f"invalid task transition: {self.state.value} -> {target.value}")
        return replace(self, state=target, updated_at=updated_at)

    def to_dict(self) -> dict[str, Any]:
        return {
            "task_id": self.task_id,
            "contract_file": self.contract_file,
            "contract_digest": self.contract_digest,
            "plan_revision": self.plan_revision,
            "dependencies": list(self.dependencies),
            "state": self.state.value,
            "attempt": self.attempt,
            "review_rounds": self.review_rounds,
            "result_files": list(self.result_files),
            "review_files": list(self.review_files),
            "updated_at": self.updated_at,
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "TaskRuntime":
        _exact_fields(data, _TASK_RUNTIME_FIELDS, "task runtime")
        try:
            task_id = _string(data, "task_id", "task runtime")
            if not _ID.fullmatch(task_id):
                raise RecoveryError("task runtime.task_id has an invalid identifier")
            return cls(
                task_id=task_id,
                contract_file=_string(data, "contract_file", "task runtime"),
                contract_digest=_string(data, "contract_digest", "task runtime"),
                plan_revision=_integer(data, "plan_revision", 1, "task runtime"),
                dependencies=_strings(data, "dependencies", "task runtime"),
                state=TaskState(_string(data, "state", "task runtime")),
                attempt=_integer(data, "attempt", 0, "task runtime"),
                review_rounds=_integer(data, "review_rounds", 0, "task runtime"),
                result_files=_strings(data, "result_files", "task runtime"),
                review_files=_strings(data, "review_files", "task runtime"),
                updated_at=_string(data, "updated_at", "task runtime"),
            )
        except RecoveryError:
            raise
        except (KeyError, TypeError, ValueError) as error:
            raise RecoveryError(f"invalid task runtime state: {error}") from error


@dataclass(frozen=True)
class RunState:
    run_id: str
    objective: str
    plan_revision: int
    plan_digest: str
    base_revision: str
    status: RunStateValue
    tasks: Mapping[str, TaskRuntime]
    created_at: str
    updated_at: str
    metadata: Mapping[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": STATE_SCHEMA_VERSION,
            "run_id": self.run_id,
            "objective": self.objective,
            "plan_revision": self.plan_revision,
            "plan_digest": self.plan_digest,
            "base_revision": self.base_revision,
            "status": self.status.value,
            "tasks": {task_id: task.to_dict() for task_id, task in sorted(self.tasks.items())},
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "metadata": dict(self.metadata),
        }

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "RunState":
        _exact_fields(data, _RUN_FIELDS, "run state")
        if data.get("schema_version") != STATE_SCHEMA_VERSION:
            raise RecoveryError(f"unsupported run-state schema: {data.get('schema_version')!r}")
        try:
            raw_tasks = data["tasks"]
            if not isinstance(raw_tasks, dict):
                raise TypeError("tasks must be an object")
            tasks = {str(key): TaskRuntime.from_dict(value) for key, value in raw_tasks.items()}
            run_id = _string(data, "run_id", "run state")
            if not _ID.fullmatch(run_id):
                raise RecoveryError("run state.run_id has an invalid identifier")
            metadata = data.get("metadata")
            if not isinstance(metadata, dict):
                raise RecoveryError("run state.metadata must be an object")
            state = cls(
                run_id=run_id,
                objective=_string(data, "objective", "run state"),
                plan_revision=_integer(data, "plan_revision", 1, "run state"),
                plan_digest=_string(data, "plan_digest", "run state"),
                base_revision=_string(data, "base_revision", "run state"),
                status=RunStateValue(_string(data, "status", "run state")),
                tasks=tasks,
                created_at=_string(data, "created_at", "run state"),
                updated_at=_string(data, "updated_at", "run state"),
                metadata=dict(metadata),
            )
        except RecoveryError:
            raise
        except (KeyError, TypeError, ValueError) as error:
            raise RecoveryError(f"invalid run state: {error}") from error
        for task_id, task in state.tasks.items():
            if task_id != task.task_id:
                raise RecoveryError(f"task map key {task_id!r} disagrees with task_id")
            unknown = set(task.dependencies) - set(state.tasks)
            if unknown:
                raise RecoveryError(f"task {task_id} has missing dependencies: {sorted(unknown)}")
        return state

    def add_task(self, task: TaskRuntime, *, updated_at: str) -> "RunState":
        if task.task_id in self.tasks:
            raise StateTransitionError(f"task already exists: {task.task_id}")
        if task.plan_revision != self.plan_revision:
            raise StaleWorkError(
                f"task revision {task.plan_revision} does not match plan revision {self.plan_revision}"
            )
        unknown = set(task.dependencies) - set(self.tasks)
        if unknown:
            raise StateTransitionError(f"task has unknown dependencies: {sorted(unknown)}")
        tasks = dict(self.tasks)
        initial = TaskState.READY if not task.dependencies else TaskState.PLANNED
        tasks[task.task_id] = replace(task, state=initial, updated_at=updated_at)
        return replace(self, tasks=tasks, status=RunStateValue.ACTIVE, updated_at=updated_at)

    def update_task(self, task: TaskRuntime, *, updated_at: str) -> "RunState":
        if task.task_id not in self.tasks:
            raise StateTransitionError(f"unknown task: {task.task_id}")
        tasks = dict(self.tasks)
        tasks[task.task_id] = task
        tasks = _release_dependents(tasks, updated_at)
        status = _derive_run_status(tasks)
        return replace(self, tasks=tasks, status=status, updated_at=updated_at)

    def revise_plan(self, new_digest: str, *, base_revision: str, updated_at: str) -> "RunState":
        tasks = {
            task_id: (
                task
                if task.state in {TaskState.ACCEPTED, TaskState.FAILED, TaskState.SUPERSEDED}
                else task.transition(TaskState.SUPERSEDED, updated_at=updated_at)
            )
            for task_id, task in self.tasks.items()
        }
        return replace(
            self,
            plan_revision=self.plan_revision + 1,
            plan_digest=new_digest,
            base_revision=base_revision,
            tasks=tasks,
            status=RunStateValue.PLANNED,
            updated_at=updated_at,
        )


def _release_dependents(
    tasks: Mapping[str, TaskRuntime], updated_at: str
) -> dict[str, TaskRuntime]:
    updated = dict(tasks)
    accepted = {task_id for task_id, task in tasks.items() if task.state is TaskState.ACCEPTED}
    for task_id, task in tasks.items():
        if task.state is TaskState.PLANNED and set(task.dependencies) <= accepted:
            updated[task_id] = task.transition(TaskState.READY, updated_at=updated_at)
    return updated


def _derive_run_status(tasks: Mapping[str, TaskRuntime]) -> RunStateValue:
    if tasks and all(task.state is TaskState.ACCEPTED for task in tasks.values()):
        return RunStateValue.ACCEPTED
    if any(task.state is TaskState.BLOCKED for task in tasks.values()):
        return RunStateValue.BLOCKED
    if tasks and all(
        task.state in {TaskState.FAILED, TaskState.SUPERSEDED, TaskState.ACCEPTED}
        for task in tasks.values()
    ) and any(task.state is TaskState.FAILED for task in tasks.values()):
        return RunStateValue.FAILED
    return RunStateValue.ACTIVE if tasks else RunStateValue.PLANNED
