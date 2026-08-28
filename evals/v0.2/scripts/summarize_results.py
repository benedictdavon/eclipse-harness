"""Aggregate already-recorded v0.2 run records; never execute agents or mutate repos."""

from __future__ import annotations

import collections
import json
import sys
from pathlib import Path
from typing import Any


def load_records(root: Path) -> list[dict[str, Any]]:
    records: list[dict[str, Any]] = []
    for path in sorted(root.glob("*/run.json")):
        value = json.loads(path.read_text(encoding="utf-8"))
        if not isinstance(value, dict):
            raise ValueError(f"{path} must contain an object")
        records.append(value)
    return records


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("usage: summarize_results.py RESULTS_DIRECTORY")
    records = load_records(Path(sys.argv[1]))
    qualifying = [record for record in records if record["classification"]["qualifying"]]
    summary = {
        "records": len(records),
        "qualifying": len(qualifying),
        "terminal_outcomes": collections.Counter(record["terminal_outcome"] for record in records),
        "successes": sum(record["metrics"]["task_success"] is True for record in records),
        "acceptance_successes": sum(record["metrics"]["acceptance_success"] is True for record in records),
        "scope_violations": sum(record["metrics"]["scope_violations"] for record in records),
        "architecture_escalations": sum(record["metrics"]["architecture_escalations"] for record in records),
        "false_architecture_escalations": sum(record["metrics"]["false_architecture_escalations"] for record in records),
        "reviewer_misses": sum(record["metrics"]["reviewer_misses"] for record in records),
        "correction_cycles": sum(record["metrics"]["correction_cycles"] for record in records),
        "problem_classes": collections.Counter(
            problem for record in records for problem in record["classification"]["problem_classes"]
        ),
        "severities": collections.Counter(record["classification"]["severity"] for record in records),
    }
    print(json.dumps(summary, indent=2, sort_keys=True, default=dict))


if __name__ == "__main__":
    main()
