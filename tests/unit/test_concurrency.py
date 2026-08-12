from __future__ import annotations

import copy
from typing import Any

import pytest

from eclipse_harness.concurrency import assert_parallel_safe, execution_waves, validate_dag
from eclipse_harness.contracts import TaskContract
from eclipse_harness.errors import ConcurrencyError


def _task(
    data: dict[str, Any],
    task_id: str,
    write: str,
    *,
    dependencies: list[str] | None = None,
) -> TaskContract:
    value = copy.deepcopy(data)
    value["task_id"] = task_id
    value["scope"]["write_globs"] = [write]
    value["dependencies"] = dependencies or []
    return TaskContract.from_dict(value)


def test_disjoint_tasks_are_parallel_safe(task_data: dict[str, Any]) -> None:
    left = _task(task_data, "T001", "src/a/**")
    right = _task(task_data, "T002", "src/b/**")
    assert_parallel_safe([left, right])
    assert execution_waves([left, right]) == (("T001", "T002"),)


def test_overlap_is_rejected(task_data: dict[str, Any]) -> None:
    left = _task(task_data, "T001", "src/auth/service.py")
    right = _task(task_data, "T002", "src/auth/service.py")
    with pytest.raises(ConcurrencyError, match="write-overlap"):
        assert_parallel_safe([left, right])


def test_mid_component_wildcard_overlap_is_rejected(task_data: dict[str, Any]) -> None:
    left = _task(task_data, "T001", "src/a*.py")
    right = _task(task_data, "T002", "src/ab*.py")
    with pytest.raises(ConcurrencyError, match="write-overlap"):
        assert_parallel_safe([left, right])


def test_shared_interface_is_rejected(task_data: dict[str, Any]) -> None:
    left_data = copy.deepcopy(task_data)
    right_data = copy.deepcopy(task_data)
    left_data["task_id"] = "T001"
    right_data["task_id"] = "T002"
    left_data["scope"]["write_globs"] = ["src/a/**"]
    right_data["scope"]["write_globs"] = ["src/b/**"]
    left_data["scope"]["shared_interfaces"] = ["PublicAPI"]
    right_data["scope"]["shared_interfaces"] = ["PublicAPI"]
    with pytest.raises(ConcurrencyError, match="shared-interface"):
        assert_parallel_safe([TaskContract.from_dict(left_data), TaskContract.from_dict(right_data)])


def test_dependency_cycle_is_rejected(task_data: dict[str, Any]) -> None:
    left_data = copy.deepcopy(task_data)
    right_data = copy.deepcopy(task_data)
    left_data["task_id"], left_data["dependencies"] = "T001", ["T002"]
    right_data["task_id"], right_data["dependencies"] = "T002", ["T001"]
    with pytest.raises(ConcurrencyError, match="cycle"):
        validate_dag([TaskContract.from_dict(left_data), TaskContract.from_dict(right_data)])


def test_writer_limit_must_be_positive(task_data: dict[str, Any]) -> None:
    with pytest.raises(ConcurrencyError, match="positive"):
        execution_waves([_task(task_data, "T001", "src/a/**")], max_parallel_writers=0)


def test_duplicate_task_identifiers_are_rejected(task_data: dict[str, Any]) -> None:
    task = _task(task_data, "T001", "src/a/**")
    with pytest.raises(ConcurrencyError, match="unique"):
        validate_dag([task, task])


def test_dependency_dag_serializes_into_waves(task_data: dict[str, Any]) -> None:
    first = _task(task_data, "T001", "src/a/**")
    second = _task(
        task_data,
        "T002",
        "src/b/**",
        dependencies=["T001"],
    )
    assert execution_waves([first, second]) == (("T001",), ("T002",))


def test_parallel_siblings_and_downstream_dependencies_form_mixed_waves(
    task_data: dict[str, Any],
) -> None:
    first = _task(task_data, "T001", "src/a/**")
    sibling = _task(task_data, "T002", "src/b/**")
    downstream = _task(
        task_data,
        "T003",
        "src/c/**",
        dependencies=["T001", "T002"],
    )
    final = _task(
        task_data,
        "T004",
        "src/d/**",
        dependencies=["T003"],
    )
    assert execution_waves([first, sibling, downstream, final]) == (
        ("T001", "T002"),
        ("T003",),
        ("T004",),
    )
