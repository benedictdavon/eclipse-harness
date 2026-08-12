"""Dependency DAG and conservative parallel-write safety checks."""

from __future__ import annotations

import re
from dataclasses import dataclass
from typing import Iterable, Sequence

from .authorization import normalize_repo_path
from .contracts import TaskContract
from .errors import ConcurrencyError

_WILDCARD = re.compile(r"[*?[]")


@dataclass(frozen=True)
class Conflict:
    left_task: str
    right_task: str
    kind: str
    detail: str


def _static_prefix(pattern: str) -> str:
    normalized = normalize_repo_path(pattern)
    match = _WILDCARD.search(normalized)
    return (normalized if match is None else normalized[: match.start()]).rstrip("/")


def globs_may_overlap(left: str, right: str) -> bool:
    left_normalized = normalize_repo_path(left)
    right_normalized = normalize_repo_path(right)
    left_wild = _WILDCARD.search(left_normalized) is not None
    right_wild = _WILDCARD.search(right_normalized) is not None
    if not left_wild and not right_wild:
        return left_normalized == right_normalized
    left_prefix, right_prefix = _static_prefix(left), _static_prefix(right)
    if not left_prefix or not right_prefix:
        return True
    return (
        left_prefix == right_prefix
        # Static prefixes can end in the middle of a path component (for
        # example ``src/a*.py``).  Any prefix relationship may overlap; the
        # validator deliberately accepts false positives rather than unsafe
        # parallel writers.
        or left_prefix.startswith(right_prefix)
        or right_prefix.startswith(left_prefix)
    )


def pair_conflicts(left: TaskContract, right: TaskContract) -> tuple[Conflict, ...]:
    conflicts: list[Conflict] = []
    left_scope, right_scope = left.scope, right.scope
    if not left_scope["parallel_safe"] or not right_scope["parallel_safe"]:
        conflicts.append(
            Conflict(left.task_id, right.task_id, "parallel-policy", "task is not marked parallel-safe")
        )
    for left_glob in left_scope["write_globs"]:
        for right_glob in right_scope["write_globs"]:
            if globs_may_overlap(str(left_glob), str(right_glob)):
                conflicts.append(
                    Conflict(
                        left.task_id,
                        right.task_id,
                        "write-overlap",
                        f"{left_glob!r} may overlap {right_glob!r}",
                    )
                )
    interfaces = set(left_scope["shared_interfaces"]) & set(right_scope["shared_interfaces"])
    for interface in sorted(interfaces):
        conflicts.append(
            Conflict(left.task_id, right.task_id, "shared-interface", str(interface))
        )
    resources = set(left_scope["exclusive_resources"]) & set(right_scope["exclusive_resources"])
    for resource in sorted(resources):
        conflicts.append(
            Conflict(left.task_id, right.task_id, "exclusive-resource", str(resource))
        )
    if left.task_id in right.dependencies or right.task_id in left.dependencies:
        conflicts.append(
            Conflict(left.task_id, right.task_id, "dependency", "tasks have an ordering dependency")
        )
    if left_scope["isolation"] == "shared-readonly" or right_scope["isolation"] == "shared-readonly":
        conflicts.append(
            Conflict(left.task_id, right.task_id, "isolation", "write task requests read-only isolation")
        )
    return tuple(conflicts)


def assert_parallel_safe(tasks: Sequence[TaskContract]) -> None:
    conflicts = [
        conflict
        for index, left in enumerate(tasks)
        for right in tasks[index + 1 :]
        for conflict in pair_conflicts(left, right)
    ]
    if conflicts:
        details = "; ".join(
            f"{item.left_task}/{item.right_task} {item.kind}: {item.detail}" for item in conflicts
        )
        raise ConcurrencyError(details)


def validate_dag(tasks: Iterable[TaskContract]) -> tuple[str, ...]:
    task_list = tuple(tasks)
    by_id = {task.task_id: task for task in task_list}
    if len(by_id) != len(task_list):
        raise ConcurrencyError("task identifiers must be unique")
    for task in by_id.values():
        unknown = sorted(set(task.dependencies) - set(by_id))
        if unknown:
            raise ConcurrencyError(f"{task.task_id} has unknown dependencies: {', '.join(unknown)}")
    visiting: set[str] = set()
    visited: set[str] = set()
    order: list[str] = []

    def visit(task_id: str) -> None:
        if task_id in visiting:
            raise ConcurrencyError(f"dependency cycle detected at {task_id}")
        if task_id in visited:
            return
        visiting.add(task_id)
        for dependency in by_id[task_id].dependencies:
            visit(dependency)
        visiting.remove(task_id)
        visited.add(task_id)
        order.append(task_id)

    for task_id in sorted(by_id):
        visit(task_id)
    return tuple(order)


def execution_waves(
    tasks: Sequence[TaskContract], *, max_parallel_writers: int = 2
) -> tuple[tuple[str, ...], ...]:
    if (
        not isinstance(max_parallel_writers, int)
        or isinstance(max_parallel_writers, bool)
        or max_parallel_writers < 1
    ):
        raise ConcurrencyError("max_parallel_writers must be a positive integer")
    validate_dag(tasks)
    by_id = {task.task_id: task for task in tasks}
    pending = set(by_id)
    complete: set[str] = set()
    waves: list[tuple[str, ...]] = []
    while pending:
        candidates = sorted(
            task_id for task_id in pending if set(by_id[task_id].dependencies) <= complete
        )
        if not candidates:
            raise ConcurrencyError("no dispatchable task; dependency graph is inconsistent")
        wave: list[str] = []
        for task_id in candidates:
            candidate = by_id[task_id]
            if len(wave) >= max_parallel_writers:
                break
            if all(not pair_conflicts(candidate, by_id[selected]) for selected in wave):
                wave.append(task_id)
        if not wave:
            wave = [candidates[0]]
        waves.append(tuple(wave))
        pending.difference_update(wave)
        complete.update(wave)
    return tuple(waves)
