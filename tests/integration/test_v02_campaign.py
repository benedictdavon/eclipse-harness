from __future__ import annotations

import collections
import hashlib
import json
import re
from pathlib import Path
from typing import Any

from eclipse_harness.contracts import (
    ResultContract,
    ReviewContract,
    TaskContract,
    validate_result_against_task,
    validate_review_against_result,
)

ROOT = Path(__file__).parents[2]
EVAL_ROOT = ROOT / "evals" / "v0.2"


def _load(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def _digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _json_blocks(path: Path) -> list[dict[str, Any]]:
    text = path.read_text(encoding="utf-8")
    if text.lstrip().startswith("{"):
        value = json.loads(text)
        assert isinstance(value, dict)
        return [value]
    values = re.findall(r"```json\s*(\{.*?\})\s*```", text, flags=re.DOTALL)
    return [json.loads(value) for value in values]


def test_v02_frozen_campaign_counts_and_categories() -> None:
    controlled = _load(EVAL_ROOT / "controlled/cases.json")["cases"]
    real = _load(EVAL_ROOT / "real/cases.json")["cases"]
    repositories = _load(EVAL_ROOT / "real/repositories.json")["repositories"]

    assert len(controlled) == 20
    assert set(collections.Counter(case["family"] for case in controlled).values()) == {2}
    assert len(repositories) == 5
    assert len(real) == 30
    assert collections.Counter(case["task_category"] for case in real) == {
        "bounded-feature": 6,
        "multi-file-feature": 6,
        "bug-diagnosis-fix": 5,
        "behavior-preserving-refactor": 4,
        "architecture-sensitive": 3,
        "parallelization-candidate": 3,
        "review-correction": 3,
    }


def test_v02_freeze_manifest_matches_key_definitions() -> None:
    manifest = _load(EVAL_ROOT / "freeze-manifest.json")
    for relative, expected in manifest["files"].items():
        assert _digest(EVAL_ROOT / relative) == expected


def test_v02_freeze_hashes_have_cross_platform_lf_checkout() -> None:
    attributes = (ROOT / ".gitattributes").read_text(encoding="utf-8")
    assert "* text=auto eol=lf" in attributes


def test_v02_real_repositories_and_cases_are_consistent() -> None:
    repositories = _load(EVAL_ROOT / "real/repositories.json")["repositories"]
    cases = _load(EVAL_ROOT / "real/cases.json")["cases"]
    commits = {repo["repo_id"]: repo["commit"] for repo in repositories}
    assert set(commits) == {case["repository"] for case in cases}
    assert all(case["repository_commit"] == commits[case["repository"]] for case in cases)


def test_skill_guidance_uses_executor_wire_role() -> None:
    orchestrate = (ROOT / ".agents/skills/eclipse-orchestrate/SKILL.md").read_text(
        encoding="utf-8"
    )
    execute = (ROOT / ".agents/skills/eclipse-execute/SKILL.md").read_text(
        encoding="utf-8"
    )

    assert "`execution_profile.role`; “worker” is descriptive prose only" in orchestrate
    assert "`worker_identity.role` to the wire-format literal `executor`" in execute


def _runs(phase: str) -> dict[str, dict[str, Any]]:
    paths = (EVAL_ROOT / "results" / phase).glob("*/run.json")
    return {path.parent.name: _load(path) for path in paths}


def test_v02_both_campaign_phases_preserve_every_case() -> None:
    frozen_ids = {
        case["case_id"]
        for source in ("controlled/cases.json", "real/cases.json")
        for case in _load(EVAL_ROOT / source)["cases"]
    }
    baseline = _runs("baseline")
    candidate = _runs("v0.2")

    assert set(baseline) == frozen_ids
    assert set(candidate) == frozen_ids
    assert all(run["classification"]["qualifying"] for run in baseline.values())
    assert all(run["classification"]["qualifying"] for run in candidate.values())


def test_v02_before_after_outcomes_are_locked_to_raw_records() -> None:
    baseline = _runs("baseline")
    candidate = _runs("v0.2")
    incomparable = {
        "V02-FIX-09A",
        "V02-FIX-09B",
        "V02-REAL-018",
        "V02-REAL-024",
        "V02-REAL-030",
    }
    classifications: collections.Counter[str] = collections.Counter()

    for case_id, before in baseline.items():
        if case_id in incomparable:
            classifications["incomparable"] += 1
            continue
        before_success = before["metrics"]["task_success"] is True
        after_success = candidate[case_id]["metrics"]["task_success"] is True
        if not before_success and after_success:
            classifications["improved"] += 1
        elif before_success and not after_success:
            classifications["regressed"] += 1
        else:
            classifications["unchanged"] += 1

    assert classifications == {
        "improved": 19,
        "unchanged": 26,
        "incomparable": 5,
    }
    assert sum(
        run["metrics"]["task_success"] is True for run in baseline.values()
    ) == 21
    assert sum(
        run["metrics"]["task_success"] is True for run in candidate.values()
    ) == 39


def test_v02_real_rerun_does_not_invent_unavailable_measurements() -> None:
    real_runs = {
        case_id: run
        for case_id, run in _runs("v0.2").items()
        if case_id.startswith("V02-REAL-")
    }

    assert len(real_runs) == 30
    assert all(run["metrics"]["usage"] == {} for run in real_runs.values())
    assert all(
        run["metrics"]["repeated_discovery"] is None for run in real_runs.values()
    )
    assert all(
        run["checks"]["review_independence"] == "unverified"
        for run in real_runs.values()
    )
    assert sum(
        run["metrics"]["scope_violations"] for run in real_runs.values()
    ) == 0


def test_v02_selected_real_contract_handoffs_validate_semantically() -> None:
    validated = 0
    for run in _runs("v0.2").values():
        if not run["case_id"].startswith("V02-REAL-"):
            continue
        artifacts = run["artifacts"]
        for artifact in artifacts.values():
            paths = artifact if isinstance(artifact, list) else [artifact]
            assert all((ROOT / path).is_file() for path in paths if path is not None)
        task_values = _json_blocks(ROOT / artifacts["task"])
        tasks = {
            value["task_id"]: TaskContract.from_dict(value)
            for value in task_values
            if "task_id" in value and "execution_profile" in value
        }
        result_paths = artifacts.get("result_tasks") or (
            [artifacts["result"]] if artifacts.get("result") else []
        )
        results: dict[str, ResultContract] = {}
        for relative in result_paths:
            for value in _json_blocks(ROOT / relative):
                if "worker_identity" not in value:
                    continue
                result = ResultContract.from_dict(value)
                task = tasks[result.task_id]
                validate_result_against_task(result, task)
                results[result.task_id] = result
                validated += 1

        observed_files = {
            line
            for line in (ROOT / run["artifacts"]["patch"]).with_name(
                "changed-files.txt"
            ).read_text(encoding="utf-8").splitlines()
            if line
        }
        reported_files = {
            str(path)
            for result in results.values()
            for path in result.data["files_changed"]
        }
        assert observed_files == reported_files

        reviews = {
            value["task_id"]: ReviewContract.from_dict(value)
            for value in _json_blocks(ROOT / artifacts["review"])
            if "reviewer_identity" in value
        }
        assert set(reviews) == set(results)
        for task_id, review in reviews.items():
            validate_review_against_result(review, results[task_id], tasks[task_id])

    assert validated == 27
