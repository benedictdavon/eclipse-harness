from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from eclipse_harness.contracts import ResultContract, ReviewContract, TaskContract
from eclipse_harness.errors import RecoveryError, StaleWorkError, StateTransitionError
from eclipse_harness.state import RunStateValue, TaskState
from eclipse_harness.store import ReviewAttestation, RunStore


def test_end_to_end_store_flow(
    tmp_path: Path,
    task: TaskContract,
    result: ResultContract,
    review: ReviewContract,
) -> None:
    store = RunStore(tmp_path)
    store.create_run(
        task.run_id,
        "Example",
        task.plan_digest,
        str(task.data["provenance"]["base_revision"]),
    )
    state = store.add_task(task.run_id, task)
    assert state.tasks[task.task_id].state is TaskState.READY
    state = store.start_task(task.run_id, task.task_id)
    assert state.tasks[task.task_id].attempt == 1
    state = store.ingest_result(
        task.run_id, result, observed_files=result.data["files_changed"]
    )
    assert state.tasks[task.task_id].state is TaskState.REVIEW_PENDING
    state = store.ingest_review(
        task.run_id, review, attestation=ReviewAttestation.human("test-reviewer")
    )
    assert state.status is RunStateValue.ACCEPTED
    assert state.tasks[task.task_id].state is TaskState.ACCEPTED
    assert (tmp_path / ".eclipse/runs/example-run/events.jsonl").is_file()


def test_plan_revision_rejects_stale_task(tmp_path: Path, task_data) -> None:  # type: ignore[no-untyped-def]
    task = TaskContract.from_dict(task_data)
    store = RunStore(tmp_path)
    store.create_run(
        task.run_id, "Example", task.plan_digest, str(task.data["provenance"]["base_revision"])
    )
    store.revise_plan(task.run_id, "sha256:new", "new-base")
    with pytest.raises(StaleWorkError, match="does not match"):
        store.add_task(task.run_id, task)


def test_plan_revision_supersedes_active_task(tmp_path: Path, task: TaskContract) -> None:
    store = RunStore(tmp_path)
    store.create_run(
        task.run_id, "Example", task.plan_digest, str(task.data["provenance"]["base_revision"])
    )
    store.add_task(task.run_id, task)
    state = store.revise_plan(task.run_id, "sha256:new", "new-base")
    assert state.plan_revision == 2
    assert state.tasks[task.task_id].state is TaskState.SUPERSEDED


def test_duplicate_task_does_not_overwrite_immutable_contract(
    tmp_path: Path, task: TaskContract
) -> None:
    store = RunStore(tmp_path)
    store.create_run(
        task.run_id, "Example", task.plan_digest, str(task.data["provenance"]["base_revision"])
    )
    store.add_task(task.run_id, task)
    before = store.load_task(task.run_id, task.task_id).digest
    with pytest.raises(StateTransitionError, match="already exists"):
        store.add_task(task.run_id, task)
    assert store.load_task(task.run_id, task.task_id).digest == before


def test_store_rejects_probable_secrets(
    tmp_path: Path, task: TaskContract, result: ResultContract
) -> None:
    store = RunStore(tmp_path)
    store.create_run(
        task.run_id, "Example", task.plan_digest, str(task.data["provenance"]["base_revision"])
    )
    store.add_task(task.run_id, task)
    store.start_task(task.run_id, task.task_id)
    data = copy.deepcopy(dict(result.data))
    data["implementation_summary"] = "ghp_abcdefghijklmnopqrstuvwxyz1234567890"
    with pytest.raises(RecoveryError, match="probable secret"):
        store.ingest_result(
            task.run_id,
            ResultContract.from_dict(data),
            observed_files=data["files_changed"],
        )


def test_store_rejects_worker_file_list_mismatch(
    tmp_path: Path, task: TaskContract, result: ResultContract
) -> None:
    store = RunStore(tmp_path)
    store.create_run(
        task.run_id, "Example", task.plan_digest, str(task.data["provenance"]["base_revision"])
    )
    store.add_task(task.run_id, task)
    store.start_task(task.run_id, task.task_id)
    with pytest.raises(StaleWorkError, match="do not match"):
        store.ingest_result(
            task.run_id,
            result,
            observed_files=[*result.data["files_changed"], "unauthorized.py"],
        )


def test_store_rejects_run_identity_tampering(tmp_path: Path, task: TaskContract) -> None:
    store = RunStore(tmp_path)
    store.create_run(task.run_id, "Example", task.plan_digest, "base")
    path = tmp_path / ".eclipse/runs/example-run/run.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["run_id"] = "other-run"
    path.write_text(json.dumps(data), encoding="utf-8")
    with pytest.raises(RecoveryError, match="identity mismatch"):
        store.load(task.run_id)
