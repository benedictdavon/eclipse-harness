"""Derive v0.2 evaluation totals from recorded evidence, not host success flags.

This is release-audit tooling, not an Eclipse runtime.  It deliberately treats
structural-only validation as inconclusive for a behavioural acceptance claim.
"""

from __future__ import annotations

import argparse
import json
from collections import Counter
from pathlib import Path
from typing import Any, Iterable


EVIDENCE_KINDS = {"behavioral-probe", "architecture-plan", "review-oracle"}
PASSING_TERMINAL_OUTCOMES = {"accepted", "architect-escalation"}


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def run_paths(root: Path) -> Iterable[Path]:
    eval_root = root / "evals" / "v0.2"
    yield from sorted((eval_root / "results").glob("*/*/run.json"))
    yield from sorted((eval_root / "supplemental" / "results").glob("*/*/run.json"))


def observed_success(root: Path, record: dict[str, Any], record_path: Path | None = None) -> bool:
    """Return an acceptance outcome derived from terminal/check/evidence facts.

    ``metrics.task_success`` and ``metrics.acceptance_success`` are intentionally
    ignored: they are retained as the original host-recorded claims, not score
    inputs.
    """

    evidence = record["acceptance_evidence"]
    if record["terminal_outcome"] not in PASSING_TERMINAL_OUTCOMES:
        return False
    if evidence["kind"] not in EVIDENCE_KINDS or evidence["status"] != "pass":
        return False

    checks = record["checks"]
    if checks["repository_commit"] != "pass" or checks["acceptance"] != "pass":
        return False
    if checks["write_scope"] not in {"pass", "not-applicable"}:
        return False

    path = evidence["path"]
    if not isinstance(path, str):
        return False
    repository_relative = root / path
    run_relative = record_path.parent / path if record_path is not None else None
    return repository_relative.is_file() or (run_relative is not None and run_relative.is_file())


def summarize(root: Path) -> dict[str, dict[str, int]]:
    totals: dict[str, Counter[str]] = {}
    for path in run_paths(root):
        record = load_json(path)
        phase = str(record["phase"])
        total = totals.setdefault(phase, Counter())
        total["runs"] += 1
        if observed_success(root, record, path):
            total["evidence_supported_successes"] += 1
        if record["acceptance_evidence"]["status"] == "unavailable":
            total["inconclusive_acceptance"] += 1
        if record["acceptance_evidence"]["kind"] == "structural-only":
            total["structural_only"] += 1
        missed = record["metrics"]["predeclared_expected_findings_missed"]
        if isinstance(missed, int):
            total["predeclared_expected_findings_missed"] += missed
    return {phase: dict(counter) for phase, counter in sorted(totals.items())}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=Path(__file__).parents[1])
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    report = summarize(args.root)
    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        for phase, totals in report.items():
            print(f"{phase}: {json.dumps(totals, sort_keys=True)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
