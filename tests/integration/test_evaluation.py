from __future__ import annotations

import json
from pathlib import Path

from eclipse_harness.evaluation import RecordedHost, run_suite


def test_recorded_evaluation_produces_no_claimed_conclusion(tmp_path: Path) -> None:
    root = Path(__file__).parents[2]
    outcomes = json.loads((root / "examples/evaluation/recorded-outcomes.json").read_text(encoding="utf-8"))
    output = tmp_path / "result.json"
    report = run_suite(
        root / "examples/evaluation/suite.json",
        RecordedHost(outcomes),
        output,
    )
    assert report["conclusion"] is None
    assert report["method"] == "recorded"
    assert output.is_file()
