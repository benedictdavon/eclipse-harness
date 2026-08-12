from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

from eclipse_harness.cli import main
from eclipse_harness.contracts import TaskContract
from eclipse_harness.jsonutil import digest_json


def test_cli_validate_and_adapter_dry_run(capsys, tmp_path: Path) -> None:  # type: ignore[no-untyped-def]
    root = Path(__file__).parents[2]
    assert main(["--root", str(root), "--json", "validate", str(root / "examples/contracts/task.json")]) == 0
    validated = json.loads(capsys.readouterr().out)
    assert validated["valid"]
    assert main(["--root", str(root), "--json", "adapters", "generate", "--host", "all", "--output", str(tmp_path), "--dry-run"]) == 0
    actions = json.loads(capsys.readouterr().out)
    assert len(actions["actions"]) == 8
    assert not any(tmp_path.iterdir())


def test_cli_validates_context_without_creating_runtime_state(capsys, tmp_path: Path) -> None:  # type: ignore[no-untyped-def]
    root = Path(__file__).parents[2]
    assert main(
        [
            "--root",
            str(tmp_path),
            "--json",
            "validate",
            str(root / "examples/contracts/context.json"),
            "--kind",
            "context",
        ]
    ) == 0
    validated = json.loads(capsys.readouterr().out)
    assert validated["valid"] and validated["kind"] == "context"
    assert not (tmp_path / ".eclipse/runs").exists()


def test_cli_rejects_correctly_digested_result_outside_task_write_scope(
    capsys, tmp_path: Path  # type: ignore[no-untyped-def]
) -> None:
    root = Path(__file__).parents[2]
    task_value = json.loads(
        (root / "examples/contracts/task.json").read_text(encoding="utf-8")
    )
    task_value["scope"]["write_globs"] = ["src/foo/**"]
    task = TaskContract.from_dict(task_value)
    result_value = json.loads(
        (root / "examples/contracts/result.json").read_text(encoding="utf-8")
    )
    result_value["task_contract_digest"] = task.digest
    result_value["files_changed"] = ["README.md"]
    result_value["git"]["changed_files_digest"] = digest_json(["README.md"])
    task_path = tmp_path / "task.json"
    result_path = tmp_path / "result.json"
    task_path.write_text(json.dumps(task_value), encoding="utf-8")
    result_path.write_text(json.dumps(result_value), encoding="utf-8")

    assert main(
        [
            "--root",
            str(root),
            "--json",
            "validate",
            str(result_path),
            "--task",
            str(task_path),
        ]
    ) == 2
    error = json.loads(capsys.readouterr().err)
    assert "outside authorized write_globs" in error["message"]
    assert "digest-mismatch" not in error["message"]


def test_cli_serializes_valid_dependency_dag_into_waves(capsys, tmp_path: Path) -> None:  # type: ignore[no-untyped-def]
    root = Path(__file__).parents[2]
    template = json.loads((root / "examples/contracts/task.json").read_text(encoding="utf-8"))
    paths: list[Path] = []
    for task_id, dependencies, write_glob in (
        ("a", [], "src/a.py"),
        ("b", [], "src/b.py"),
        ("c", ["a", "b"], "src/c.py"),
    ):
        value = deepcopy(template)
        value["task_id"] = task_id
        value["dependencies"] = dependencies
        value["scope"]["write_globs"] = [write_glob]
        path = tmp_path / f"{task_id}.json"
        path.write_text(json.dumps(value), encoding="utf-8")
        paths.append(path)

    assert main(
        [
            "--root",
            str(root),
            "--json",
            "check-concurrency",
            *(str(path) for path in paths),
        ]
    ) == 0
    report = json.loads(capsys.readouterr().out)
    assert report == {"dag_valid": True, "waves": [["a", "b"], ["c"]]}


def test_cli_rejects_decorative_copilot_concurrency_flag(capsys, tmp_path: Path) -> None:  # type: ignore[no-untyped-def]
    root = Path(__file__).parents[2]
    assert main(
        [
            "--root",
            str(root),
            "--json",
            "adapters",
            "generate",
            "--host",
            "copilot",
            "--max-concurrency",
            "3",
            "--output",
            str(tmp_path),
        ]
    ) == 2
    error = json.loads(capsys.readouterr().err)
    assert "applies only to the Codex adapter" in error["message"]
