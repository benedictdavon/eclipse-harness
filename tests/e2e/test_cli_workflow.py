from __future__ import annotations

import json
from pathlib import Path

from eclipse_harness.cli import main


def test_cli_validate_and_adapter_dry_run(capsys, tmp_path: Path) -> None:  # type: ignore[no-untyped-def]
    root = Path(__file__).parents[2]
    assert main(["--root", str(root), "--json", "validate", str(root / "examples/contracts/task.json")]) == 0
    validated = json.loads(capsys.readouterr().out)
    assert validated["valid"]
    assert main(["--root", str(root), "--json", "adapters", "generate", "--host", "all", "--output", str(tmp_path), "--dry-run"]) == 0
    actions = json.loads(capsys.readouterr().out)
    assert len(actions["actions"]) == 8
    assert not any(tmp_path.iterdir())


def test_cli_run_lifecycle(
    capsys,
    tmp_path: Path,
    task_data,
    result_data,
    review_data,
) -> None:  # type: ignore[no-untyped-def]
    task_file = tmp_path / "task.json"
    result_file = tmp_path / "result.json"
    review_file = tmp_path / "review.json"
    for path, value in ((task_file, task_data), (result_file, result_data), (review_file, review_data)):
        path.write_text(json.dumps(value), encoding="utf-8")
    base = task_data["provenance"]["base_revision"]
    commands = (
        ["--root", str(tmp_path), "plan", "create", "--run-id", "example-run", "--objective", "Example", "--plan-digest", "sha256:example-plan-v1", "--base-revision", base],
        ["--root", str(tmp_path), "plan", "add-task", "--run-id", "example-run", str(task_file)],
        ["--root", str(tmp_path), "task", "start", "--run-id", "example-run", "--task-id", "T001"],
        ["--root", str(tmp_path), "result", "ingest", "--run-id", "example-run", "--observed-file", "tests/fixtures/simple-python/src/simple/greeting.py", "--observed-file", "tests/fixtures/simple-python/tests/test_greeting.py", str(result_file)],
        ["--root", str(tmp_path), "review", "ingest", "--run-id", "example-run", "--human-approval", "--principal", "test-reviewer", str(review_file)],
        ["--root", str(tmp_path), "render", "example-run"],
    )
    for command in commands:
        assert main(command) == 0
        capsys.readouterr()
    assert (tmp_path / "plans/ACTIVE_PLAN.md").is_file()
    assert "`accepted`" in (tmp_path / "plans/ACTIVE_PLAN.md").read_text(encoding="utf-8")
