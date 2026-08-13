"""Pure lifecycle semantics for hosts that want deterministic plan checks.

This module has no persistence, locking, scheduling, git, or execution behavior. Hosts may
use it as an optional protocol validator while retaining ownership of their actual workflow
state.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum
from typing import Mapping

from .errors import StateTransitionError


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


TERMINAL_TASK_STATES = frozenset(
    {TaskState.ACCEPTED, TaskState.FAILED, TaskState.SUPERSEDED}
)

_TRANSITIONS: Mapping[TaskState, frozenset[TaskState]] = {
    TaskState.PLANNED: frozenset({TaskState.READY, TaskState.SUPERSEDED}),
    TaskState.READY: frozenset(
        {TaskState.RUNNING, TaskState.BLOCKED, TaskState.SUPERSEDED}
    ),
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
        {
            TaskState.READY,
            TaskState.READY_FOR_CORRECTION,
            TaskState.ESCALATED,
            TaskState.FAILED,
            TaskState.SUPERSEDED,
        }
    ),
    TaskState.ESCALATED: frozenset(
        {TaskState.READY, TaskState.FAILED, TaskState.SUPERSEDED}
    ),
    TaskState.ACCEPTED: frozenset(),
    TaskState.FAILED: frozenset(),
    TaskState.SUPERSEDED: frozenset(),
}


@dataclass(frozen=True)
class TaskLifecycle:
    """A host-independent task state used only for protocol reasoning."""

    task_id: str
    dependencies: tuple[str, ...]
    state: TaskState

    def transition(self, target: TaskState) -> "TaskLifecycle":
        if target not in _TRANSITIONS[self.state]:
            raise StateTransitionError(
                f"invalid task transition: {self.state.value} -> {target.value}"
            )
        return replace(self, state=target)


@dataclass(frozen=True)
class RunState:
    """In-memory plan-revision helper; never canonical Eclipse-owned state."""

    plan_revision: int
    plan_digest: str
    tasks: Mapping[str, TaskLifecycle]

    def revise_plan(self, new_digest: str) -> "RunState":
        if not new_digest.strip():
            raise StateTransitionError("new plan digest must not be empty")
        tasks = {
            task_id: (
                task
                if task.state in TERMINAL_TASK_STATES
                else task.transition(TaskState.SUPERSEDED)
            )
            for task_id, task in self.tasks.items()
        }
        return replace(
            self,
            plan_revision=self.plan_revision + 1,
            plan_digest=new_digest,
            tasks=tasks,
        )
