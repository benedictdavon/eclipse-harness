from __future__ import annotations

import pytest

from eclipse_harness.errors import StateTransitionError
from eclipse_harness.state import (
    TERMINAL_TASK_STATES,
    RunState,
    TaskLifecycle,
    TaskState,
)


def _task(state: TaskState = TaskState.READY) -> TaskLifecycle:
    return TaskLifecycle(task_id="T001", dependencies=(), state=state)


def test_valid_state_path() -> None:
    task = _task().transition(TaskState.RUNNING)
    task = task.transition(TaskState.EVIDENCE_PENDING)
    task = task.transition(TaskState.REVIEW_PENDING)
    task = task.transition(TaskState.ACCEPTED)
    assert task.state is TaskState.ACCEPTED


def test_invalid_transition_is_rejected() -> None:
    with pytest.raises(StateTransitionError, match="invalid"):
        _task().transition(TaskState.ACCEPTED)


def test_correction_path() -> None:
    task = _task(TaskState.REVIEW_PENDING)
    task = task.transition(TaskState.CHANGES_REQUESTED)
    task = task.transition(TaskState.READY_FOR_CORRECTION)
    assert task.state is TaskState.READY_FOR_CORRECTION


@pytest.mark.parametrize(
    "task_state",
    [state for state in TaskState if state not in TERMINAL_TASK_STATES],
)
def test_plan_revision_supersedes_every_nonterminal_state(task_state: TaskState) -> None:
    state = RunState(
        plan_revision=1,
        plan_digest="sha256:old",
        tasks={"T001": _task(task_state)},
    )
    revised = state.revise_plan("sha256:new")
    assert revised.plan_revision == 2
    assert revised.plan_digest == "sha256:new"
    assert revised.tasks["T001"].state is TaskState.SUPERSEDED


@pytest.mark.parametrize("task_state", list(TERMINAL_TASK_STATES))
def test_plan_revision_preserves_terminal_states(task_state: TaskState) -> None:
    state = RunState(1, "sha256:old", {"T001": _task(task_state)})
    assert state.revise_plan("sha256:new").tasks["T001"].state is task_state
