from __future__ import annotations

import copy
import json
from pathlib import Path

import pytest

from eclipse_harness.errors import ConfigurationError
from eclipse_harness.routing import Policy, RouteVerification, escalation_route, suitability_score


def _policy() -> Policy:
    root = Path(__file__).parents[2]
    return Policy.from_dict(json.loads((root / "policies/sol-luna.json").read_text(encoding="utf-8")))


def test_routine_task_routes_to_lite_worker(task) -> None:  # type: ignore[no-untyped-def]
    decision = _policy().select(
        task,
        {"worker-lite": RouteVerification.VERIFIED},
        unverified_behavior="fail",
    )
    assert decision.profile.name == "worker-lite"
    assert decision.mode == "native-verified"


def test_architectural_task_routes_to_architect(task_data) -> None:  # type: ignore[no-untyped-def]
    task_data["complexity"] = "architectural"
    from eclipse_harness.contracts import TaskContract

    decision = _policy().select(
        TaskContract.from_dict(task_data),
        {"architect": RouteVerification.UNVERIFIED},
        unverified_behavior="manual",
    )
    assert decision.profile.name == "architect"
    assert decision.mode == "manual"


def test_strict_unverified_route_fails(task) -> None:  # type: ignore[no-untyped-def]
    with pytest.raises(ConfigurationError, match="not verified"):
        _policy().select(task, {}, unverified_behavior="fail")


def test_security_flag_reduces_suitability(task_data) -> None:  # type: ignore[no-untyped-def]
    from eclipse_harness.contracts import TaskContract

    baseline, _ = suitability_score(TaskContract.from_dict(task_data))
    task_data["risk"]["flags"] = ["security"]
    changed, rationale = suitability_score(TaskContract.from_dict(task_data))
    assert changed == baseline - 2
    assert "risk penalty: security" in rationale


@pytest.mark.parametrize(
    ("code", "route"),
    [
        ("CTX_MISSING", "repair-context-or-environment"),
        ("ENV_FAILURE", "repair-context-or-environment"),
        ("LOCAL_REASONING", "higher-worker-effort"),
        ("ARCH_DECISION", "architect"),
        ("DESTRUCTIVE_ACTION", "human"),
    ],
)
def test_escalation_taxonomy(code: str, route: str) -> None:
    assert escalation_route(code) == route


def test_policy_rejects_toml_injection() -> None:
    root = Path(__file__).parents[2]
    data = json.loads((root / "policies/sol-luna.json").read_text(encoding="utf-8"))
    malicious = copy.deepcopy(data)
    malicious["profiles"]["worker"]["preferred_model"] = 'model"\n[agents]\nenabled=true'
    with pytest.raises(ConfigurationError, match="invalid model"):
        Policy.from_dict(malicious)
