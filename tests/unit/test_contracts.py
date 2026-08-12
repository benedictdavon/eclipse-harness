from __future__ import annotations

from typing import Any

import pytest

from eclipse_harness.contracts import (
    ResultContract,
    ReviewContract,
    TaskContract,
    validate_result_against_task,
    validate_review_against_result,
)
from eclipse_harness.errors import ContractValidationError


def test_task_rejects_missing_objective(task_data: dict[str, Any]) -> None:
    del task_data["objective"]
    with pytest.raises(ContractValidationError, match="objective"):
        TaskContract.from_dict(task_data)


def test_task_rejects_unknown_property(task_data: dict[str, Any]) -> None:
    task_data["surprise"] = True
    with pytest.raises(ContractValidationError, match="surprise"):
        TaskContract.from_dict(task_data)


def test_task_rejects_duplicate_criteria(task_data: dict[str, Any]) -> None:
    task_data["acceptance_criteria"].append(task_data["acceptance_criteria"][0])
    with pytest.raises(ContractValidationError, match="unique"):
        TaskContract.from_dict(task_data)


def test_unverified_identity_cannot_claim_effective_model(result_data: dict[str, Any]) -> None:
    result_data["worker_identity"]["effective_model"] = "gpt-5.6-luna"
    with pytest.raises(ContractValidationError, match="host-observed"):
        ResultContract.from_dict(result_data)


def test_contract_cannot_self_attest_host_identity(result_data: dict[str, Any]) -> None:
    result_data["worker_identity"]["verification"] = "host-observed"
    result_data["worker_identity"]["effective_model"] = "gpt-5.6-luna"
    with pytest.raises(ContractValidationError, match="trusted envelope"):
        ResultContract.from_dict(result_data)


def test_complete_result_requires_all_criteria(
    task: TaskContract, result_data: dict[str, Any]
) -> None:
    result_data["criteria_evidence"] = []
    result = ResultContract.from_dict(result_data)
    with pytest.raises(ContractValidationError, match="missing evidence"):
        validate_result_against_task(result, task)


def test_complete_result_requires_required_command(
    task: TaskContract, result_data: dict[str, Any]
) -> None:
    result_data["commands"][0]["outcome"] = "failed"
    result_data["commands"][0]["exit_code"] = 1
    result = ResultContract.from_dict(result_data)
    with pytest.raises(ContractValidationError, match="required command"):
        validate_result_against_task(result, task)


def test_task_rejects_unauthorized_network_command(task_data: dict[str, Any]) -> None:
    task_data["validation"][0]["command"] = "pip install unsafe-package"
    with pytest.raises(ContractValidationError, match="network.*not authorized"):
        TaskContract.from_dict(task_data)


def test_result_allows_bounded_undeclared_exploration_command(
    task: TaskContract, result_data: dict[str, Any]
) -> None:
    result_data["commands"].append(
        {
            "command": "rg greet tests/fixtures/simple-python",
            "purpose": "Bounded read-only exploration",
            "exit_code": 0,
            "outcome": "passed",
            "summary": "Located the fixture symbol.",
        }
    )
    result = ResultContract.from_dict(result_data)
    validate_result_against_task(result, task)


def test_result_rejects_unauthorized_effectful_undeclared_command(
    task: TaskContract, result_data: dict[str, Any]
) -> None:
    result_data["commands"].append(
        {
            "command": "pip install unexpected-package",
            "purpose": "Unauthorized dependency change",
            "exit_code": 0,
            "outcome": "passed",
            "summary": "installed",
        }
    )
    result = ResultContract.from_dict(result_data)
    with pytest.raises(ContractValidationError, match="network.*not authorized"):
        validate_result_against_task(result, task)


@pytest.mark.parametrize(
    ("outcome", "exit_code"),
    [
        ("passed", 1),
        ("passed", None),
        ("failed", 0),
        ("failed", None),
        ("not-run", 0),
        ("not-run", 1),
    ],
)
def test_command_evidence_rejects_contradictory_outcome_and_exit_code(
    result_data: dict[str, Any], outcome: str, exit_code: int | None
) -> None:
    result_data["commands"][0]["outcome"] = outcome
    result_data["commands"][0]["exit_code"] = exit_code
    with pytest.raises(ContractValidationError, match="exit_code"):
        ResultContract.from_dict(result_data)


def test_stale_result_is_rejected(task: TaskContract, result_data: dict[str, Any]) -> None:
    result_data["plan_revision"] = 2
    result = ResultContract.from_dict(result_data)
    with pytest.raises(ContractValidationError, match="plan_revision"):
        validate_result_against_task(result, task)


def test_accepted_review_requires_verdicts(
    task: TaskContract, result: ResultContract, review_data: dict[str, Any]
) -> None:
    review_data["criteria_verdicts"] = []
    review = ReviewContract.from_dict(review_data)
    with pytest.raises(ContractValidationError, match="must satisfy"):
        validate_review_against_result(review, result, task)


def test_accepted_review_cannot_contain_findings(
    task: TaskContract, result: ResultContract, review_data: dict[str, Any]
) -> None:
    review_data["findings"] = [
        {
            "id": "F-1",
            "severity": "high",
            "type": "acceptance-failure",
            "path": "src/example.py",
            "evidence": "Observed mismatch",
            "impact": "Incorrect behavior",
            "correction": "Correct the behavior",
            "disposition": "worker",
        }
    ]
    review = ReviewContract.from_dict(review_data)
    with pytest.raises(ContractValidationError, match="accepted review cannot"):
        validate_review_against_result(review, result, task)


def test_review_rejects_duplicate_verdicts(review_data: dict[str, Any]) -> None:
    review_data["criteria_verdicts"].append(review_data["criteria_verdicts"][0])
    with pytest.raises(ContractValidationError, match="unique"):
        ReviewContract.from_dict(review_data)


def test_accepted_review_rejects_effective_write_permissions(
    task: TaskContract, result: ResultContract, review_data: dict[str, Any]
) -> None:
    review_data["permissions"]["effective"] = "workspace-write"
    review = ReviewContract.from_dict(review_data)
    with pytest.raises(ContractValidationError, match="read-only"):
        validate_review_against_result(review, result, task)
