from __future__ import annotations

import json
from pathlib import Path

import jsonschema


ROOT = Path(__file__).parents[2]


def test_all_schemas_are_valid() -> None:
    for path in (ROOT / "schemas").glob("*.schema.json"):
        schema = json.loads(path.read_text(encoding="utf-8"))
        jsonschema.Draft202012Validator.check_schema(schema)


def test_examples_validate_against_published_schemas() -> None:
    mapping = {
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


def test_skill_structure_and_references() -> None:
    skill_root = ROOT / ".agents" / "skills"
    expected = {"eclipse-orchestrate", "eclipse-execute", "eclipse-review", "eclipse-doctor"}
    assert {path.name for path in skill_root.iterdir()} == expected
    for directory in skill_root.iterdir():
        text = (directory / "SKILL.md").read_text(encoding="utf-8")
        assert text.startswith("---\nname: ")
        assert f"name: {directory.name}\n" in text
        assert "description:" in text
        assert len(text.splitlines()) < 120
        for reference in (directory / "references").glob("*.md"):
            assert reference.name in text
