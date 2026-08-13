"""Deterministic evaluation records for workflow quality/cost comparisons."""

from __future__ import annotations

import statistics
import time
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping, Protocol

from .constants import EVALUATION_SCHEMA_VERSION
from .jsonutil import load_json, write_json_atomic


@dataclass(frozen=True)
class EvaluationCase:
    case_id: str
    fixture: str
    objective: str
    acceptance_ids: tuple[str, ...]
    forbidden_paths: tuple[str, ...]

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "EvaluationCase":
        try:
            return cls(
                case_id=str(data["case_id"]),
                fixture=str(data["fixture"]),
                objective=str(data["objective"]),
                acceptance_ids=tuple(str(item) for item in data["acceptance_ids"]),
                forbidden_paths=tuple(str(item) for item in data["forbidden_paths"]),
            )
        except (KeyError, TypeError) as error:
            raise ValueError(f"invalid evaluation case: {error}") from error


@dataclass(frozen=True)
class CaseResult:
    case_id: str
    strategy: str
    success: bool
    criteria_satisfied: int
    criteria_total: int
    test_pass_rate: float
    regressions: int
    review_findings: int
    architectural_violations: int
    unauthorized_paths: int
    latency_ms: int
    architect_invocations: int
    worker_invocations: int
    retries: int
    usage: Mapping[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return dict(self.__dict__)


class EvaluationHost(Protocol):
    def run_case(self, case: EvaluationCase, strategy: str) -> CaseResult: ...


class RecordedHost:
    """CI-safe host that reads declared results instead of calling live models."""

    def __init__(self, outcomes: Mapping[str, Any]):
        self.outcomes = outcomes

    def run_case(self, case: EvaluationCase, strategy: str) -> CaseResult:
        started = time.monotonic()
        key = f"{case.case_id}:{strategy}"
        raw = self.outcomes.get(key)
        if not isinstance(raw, dict):
            raise ValueError(f"missing recorded outcome: {key}")
        return CaseResult(
            case_id=case.case_id,
            strategy=strategy,
            success=bool(raw["success"]),
            criteria_satisfied=int(raw["criteria_satisfied"]),
            criteria_total=len(case.acceptance_ids),
            test_pass_rate=float(raw["test_pass_rate"]),
            regressions=int(raw.get("regressions", 0)),
            review_findings=int(raw.get("review_findings", 0)),
            architectural_violations=int(raw.get("architectural_violations", 0)),
            unauthorized_paths=int(raw.get("unauthorized_paths", 0)),
            latency_ms=int(raw.get("latency_ms", (time.monotonic() - started) * 1000)),
            architect_invocations=int(raw.get("architect_invocations", 0)),
            worker_invocations=int(raw.get("worker_invocations", 0)),
            retries=int(raw.get("retries", 0)),
            usage=dict(raw.get("usage", {"quality": "unavailable", "source": "recorded"})),
        )


def run_suite(path: Path, host: EvaluationHost, output: Path) -> Mapping[str, Any]:
    value = load_json(path)
    if not isinstance(value, dict) or value.get("schema_version") != EVALUATION_SCHEMA_VERSION:
        raise ValueError("unsupported evaluation suite")
    cases = [EvaluationCase.from_dict(item) for item in value.get("cases", [])]
    strategies = [str(item) for item in value.get("strategies", [])]
    if not cases or not strategies:
        raise ValueError("evaluation suite requires cases and strategies")
    results = [host.run_case(case, strategy) for case in cases for strategy in strategies]
    summary: dict[str, Any] = {}
    for strategy in strategies:
        selected = [item for item in results if item.strategy == strategy]
        summary[strategy] = {
            "cases": len(selected),
            "success_rate": sum(item.success for item in selected) / len(selected),
            "mean_test_pass_rate": statistics.fmean(item.test_pass_rate for item in selected),
            "regressions": sum(item.regressions for item in selected),
            "review_findings": sum(item.review_findings for item in selected),
            "architectural_violations": sum(item.architectural_violations for item in selected),
            "unauthorized_paths": sum(item.unauthorized_paths for item in selected),
            "architect_invocations": sum(item.architect_invocations for item in selected),
            "worker_invocations": sum(item.worker_invocations for item in selected),
            "retries": sum(item.retries for item in selected),
        }
    report = {
        "schema_version": EVALUATION_SCHEMA_VERSION,
        "suite": value.get("name"),
        "method": "recorded" if isinstance(host, RecordedHost) else "live",
        "results": [item.to_dict() for item in results],
        "summary": summary,
        "conclusion": None,
    }
    write_json_atomic(output, report)
    return report
