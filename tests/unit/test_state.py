from __future__ import annotations

import pytest

from eclipse_harness.errors import StateTransitionError
from eclipse_harness.state import TaskRuntime, TaskState


def _runtime(state: TaskState = TaskState.READY) -> TaskRuntime:
    return TaskRuntime(
        task_id="T001",
        contract_file="contracts/T001.json",
        contract_digest="sha256:task",
        plan_revision=1,
        dependencies=(),
        state=state,
        attempt=0,
        review_rounds=0,
        result_files=(),
        review_files=(),
        updated_at="2026-08-12T00:00:00Z",
    )


def test_valid_state_path() -> None:
    runtime = _runtime().transition(TaskState.RUNNING, updated_at="1")
    runtime = runtime.transition(TaskState.EVIDENCE_PENDING, updated_at="2")
    runtime = runtime.transition(TaskState.REVIEW_PENDING, updated_at="3")
    runtime = runtime.transition(TaskState.ACCEPTED, updated_at="4")
    assert runtime.state is TaskState.ACCEPTED


def test_invalid_transition_is_rejected() -> None:
    with pytest.raises(StateTransitionError, match="invalid"):
        _runtime().transition(TaskState.ACCEPTED, updated_at="1")


def test_correction_path() -> None:
    runtime = _runtime(TaskState.REVIEW_PENDING)
    runtime = runtime.transition(TaskState.CHANGES_REQUESTED, updated_at="1")
    runtime = runtime.transition(TaskState.READY_FOR_CORRECTION, updated_at="2")
    assert runtime.state is TaskState.READY_FOR_CORRECTION
