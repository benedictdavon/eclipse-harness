from __future__ import annotations

import json
from copy import deepcopy
from pathlib import Path

import jsonschema
import pytest


ROOT = Path(__file__).parents[2]


def test_all_schemas_are_valid() -> None:
    for path in (ROOT / "schemas").glob("*.schema.json"):
        schema = json.loads(path.read_text(encoding="utf-8"))
        jsonschema.Draft202012Validator.check_schema(schema)


def test_examples_validate_against_published_schemas() -> None:
    mapping = {
        "context.json": "context-manifest.schema.json",
        "task.json": "task-contract.schema.json",
        "result.json": "result-contract.schema.json",
        "review.json": "review-contract.schema.json",
    }
    for example_name, schema_name in mapping.items():
        value = json.loads((ROOT / "examples/contracts" / example_name).read_text(encoding="utf-8"))
        schema = json.loads((ROOT / "schemas" / schema_name).read_text(encoding="utf-8"))
        jsonschema.Draft202012Validator(schema).validate(value)


def test_policy_and_evaluation_schema() -> None:
    cases = (
        ("policies/sol-luna.json", "role-policy.schema.json"),
        ("examples/evaluation/suite.json", "evaluation-suite.schema.json"),
    )
    for value_path, schema_name in cases:
        value = json.loads((ROOT / value_path).read_text(encoding="utf-8"))
        schema = json.loads((ROOT / "schemas" / schema_name).read_text(encoding="utf-8"))
        jsonschema.Draft202012Validator(schema).validate(value)


@pytest.mark.parametrize(
    ("outcome", "exit_code"),
    [("passed", 1), ("failed", 0), ("failed", None), ("not-run", 0)],
)
def test_result_schema_rejects_inconsistent_command_evidence(
    outcome: str, exit_code: int | None
) -> None:
    value = json.loads((ROOT / "examples/contracts/result.json").read_text(encoding="utf-8"))
    value = deepcopy(value)
    value["commands"][0]["outcome"] = outcome
    value["commands"][0]["exit_code"] = exit_code
    schema = json.loads(
        (ROOT / "schemas/result-contract.schema.json").read_text(encoding="utf-8")
    )
    with pytest.raises(jsonschema.ValidationError):
        jsonschema.Draft202012Validator(schema).validate(value)


def test_skill_structure_and_references() -> None:
    skill_root = ROOT / ".agents" / "skills"
    expected = {
        "eclipse-orchestrate",
        "eclipse-execute",
        "eclipse-review",
        "eclipse-bootstrap",
        "eclipse-doctor",
    }
    assert {path.name for path in skill_root.iterdir()} == expected
    for directory in skill_root.iterdir():
        text = (directory / "SKILL.md").read_text(encoding="utf-8")
        assert text.startswith("---\nname: ")
        assert f"name: {directory.name}\n" in text
        assert "description:" in text
        assert len(text.splitlines()) < 120
        for reference in (directory / "references").glob("*.md"):
            assert reference.name in text


def test_core_skills_do_not_require_python_or_eclipse_runtime() -> None:
    skill_root = ROOT / ".agents" / "skills"
    combined = "\n".join(
        (skill_root / name / "SKILL.md").read_text(encoding="utf-8")
        for name in ("eclipse-orchestrate", "eclipse-execute", "eclipse-review")
    )
    prohibited = (
        ".eclipse/runs",
        "eclipse plan",
        "eclipse task start",
        "eclipse result ingest",
        "eclipse review ingest",
        "eclipse worktree",
    )
    assert not any(value in combined for value in prohibited)
    assert "optional CLI" in combined


def test_distribution_omits_runtime_engine_resources() -> None:
    absent = (
        ROOT / "src/eclipse_harness/store.py",
        ROOT / "src/eclipse_harness/events.py",
        ROOT / "src/eclipse_harness/gitops.py",
        ROOT / "src/eclipse_harness/migration.py",
        ROOT / "schemas/run-state.schema.json",
        ROOT / "schemas/config.schema.json",
    )
    assert not any(path.exists() for path in absent)
