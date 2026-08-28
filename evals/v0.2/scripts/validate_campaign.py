"""Validate the frozen v0.2 case inventory using only the standard library."""

from __future__ import annotations

import collections
import hashlib
import json
from pathlib import Path
from typing import Any

ROOT = Path(__file__).parents[1]


def load(relative: str) -> dict[str, Any]:
    value = json.loads((ROOT / relative).read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise ValueError(f"{relative} must contain an object")
    return value


def file_digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def definition_tree_digest() -> str:
    entries: list[str] = []
    for path in sorted(ROOT.rglob("*")):
        if not path.is_file() or path.name == "freeze-manifest.json":
            continue
        if "results" in path.relative_to(ROOT).parts:
            continue
        relative = path.relative_to(ROOT.parents[1]).as_posix()
        entries.append(f"{file_digest(path)}  {relative}\n")
    return hashlib.sha256("".join(entries).encode("utf-8")).hexdigest()


def main() -> None:
    campaign = load("campaign.json")
    controlled = load(campaign["definitions"]["controlled_cases"])["cases"]
    repositories = load(campaign["definitions"]["real_repositories"])["repositories"]
    real = load(campaign["definitions"]["real_cases"])["cases"]

    assert len(controlled) == 20
    assert len({case["case_id"] for case in controlled}) == 20
    families = collections.Counter(case["family"] for case in controlled)
    assert len(families) == 10 and set(families.values()) == {2}

    assert len(repositories) == 5
    repo_ids = {repo["repo_id"] for repo in repositories}
    assert len(repo_ids) == 5
    assert len(real) == 30 and len({case["case_id"] for case in real}) == 30
    assert {case["repository"] for case in real} == repo_ids
    assert collections.Counter(case["repository"] for case in real) == {
        repo_id: 6 for repo_id in repo_ids
    }
    assert collections.Counter(case["task_category"] for case in real) == {
        "bounded-feature": 6,
        "multi-file-feature": 6,
        "bug-diagnosis-fix": 5,
        "behavior-preserving-refactor": 4,
        "architecture-sensitive": 3,
        "parallelization-candidate": 3,
        "review-correction": 3,
    }

    required = {
        "case_id",
        "case_type",
        "repository",
        "repository_commit",
        "host",
        "adapter",
        "task_category",
        "task_statement",
        "expected_write_scope",
        "acceptance_criteria",
        "validation",
        "policy",
        "notes",
    }
    for case in [*controlled, *real]:
        missing = required - set(case)
        assert not missing, f"{case.get('case_id')} missing {sorted(missing)}"
        assert case["task_statement"].strip()
        assert case["acceptance_criteria"]

    for fixture in sorted((ROOT / "controlled" / "fixtures").iterdir()):
        assert fixture.is_dir() and any(path.is_file() for path in fixture.rglob("*"))

    manifest = load("freeze-manifest.json")
    assert manifest["baseline_commit"] == campaign["baseline"]["commit"]
    assert manifest["definition_tree_sha256"] == definition_tree_digest()

    definitions = [
        ROOT / "campaign.json",
        ROOT / campaign["definitions"]["controlled_cases"],
        ROOT / campaign["definitions"]["real_repositories"],
        ROOT / campaign["definitions"]["real_cases"],
    ]
    print(json.dumps({path.relative_to(ROOT).as_posix(): file_digest(path) for path in definitions}, sort_keys=True))
    print("v0.2 campaign: PASS")


if __name__ == "__main__":
    main()
