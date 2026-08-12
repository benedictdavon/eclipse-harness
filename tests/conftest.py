from __future__ import annotations

import copy
import json
from pathlib import Path
from typing import Any

import pytest

from eclipse_harness.contracts import ResultContract, ReviewContract, TaskContract


REPOSITORY_ROOT = Path(__file__).parents[1]


def load_example(name: str) -> dict[str, Any]:
    return json.loads((REPOSITORY_ROOT / "examples" / "contracts" / name).read_text(encoding="utf-8"))


@pytest.fixture
def task_data() -> dict[str, Any]:
    return copy.deepcopy(load_example("task.json"))


@pytest.fixture
def task(task_data: dict[str, Any]) -> TaskContract:
    return TaskContract.from_dict(task_data)


@pytest.fixture
def result_data(task: TaskContract) -> dict[str, Any]:
    value = copy.deepcopy(load_example("result.json"))
    value["task_contract_digest"] = task.digest
    return value


@pytest.fixture
def result(result_data: dict[str, Any]) -> ResultContract:
    return ResultContract.from_dict(result_data)


@pytest.fixture
def review_data(task: TaskContract, result: ResultContract) -> dict[str, Any]:
    value = copy.deepcopy(load_example("review.json"))
    value["task_contract_digest"] = task.digest
    value["result_digest"] = result.digest
    return value


@pytest.fixture
def review(review_data: dict[str, Any]) -> ReviewContract:
    return ReviewContract.from_dict(review_data)
