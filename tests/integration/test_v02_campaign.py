from __future__ import annotations

import collections
import hashlib
import json
import re
from copy import deepcopy
from pathlib import Path
from typing import Any

import jsonschema
import pytest

from eclipse_harness.contracts import (
    ResultContract,
    ReviewContract,
    TaskContract,
    validate_result_against_task,
    validate_review_against_result,
)
from eclipse_harness.jsonutil import digest_json
from tools.score_v02_campaign import observed_success, summarize

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


def _supplemental_runs(phase: str) -> dict[str, dict[str, Any]]:
    paths = (EVAL_ROOT / "supplemental" / "results" / phase).glob("*/run.json")
    return {path.parent.name: _load(path) for path in paths}


def _patch_files(path: Path) -> list[str]:
    """Return the exact repository paths changed by a frozen unified patch."""

    values = [
        before if after == "/dev/null" else after
        for before, after in re.findall(
            r"^diff --git a/(.+?) b/(.+?)$", path.read_text(encoding="utf-8"), re.MULTILINE
        )
    ]
    assert values and len(values) == len(set(values))
    return sorted(values)


def _patch_digest(path: Path) -> str:
    return "sha256:" + hashlib.sha256(path.read_bytes()).hexdigest()


def _assert_supplemental_task_binding(task: dict[str, Any], case: dict[str, Any]) -> None:
    """Fail closed when a stored task drifts from its frozen case definition."""

    if task["objective"] != case["task_statement"]:
        raise AssertionError("task objective differs from frozen task_statement")
    if [item["statement"] for item in task["acceptance_criteria"]] != case[
        "acceptance_criteria"
    ]:
        raise AssertionError("task acceptance criteria differ from frozen case")
    if [item["command"] for item in task["validation"]] != case["validation"]:
        raise AssertionError("task validation commands differ from frozen case")


def _assert_supplemental_result_binding(
    result: dict[str, Any], *, root: Path
) -> None:
    """Fail closed when result file/digest claims are not bound to its patch."""

    metadata = result["metadata"]
    patch_path = root / metadata["patch_path"]
    expected_files = _patch_files(patch_path)
    if result["files_changed"] != expected_files:
        raise AssertionError("result files_changed differs from its bound patch")
    if result["git"]["changed_files_digest"] != digest_json(expected_files):
        raise AssertionError("result changed-files digest differs from its bound patch")
    if metadata["patch_digest"] != _patch_digest(patch_path):
        raise AssertionError("result patch digest differs from its bound patch")


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


def test_v02_before_after_outcomes_are_recomputed_from_raw_evidence() -> None:
    baseline = _runs("baseline")
    candidate = _runs("v0.2")
    incomparable = {
        "V02-FIX-09A",
        "V02-FIX-09B",
        "V02-REAL-018",
        "V02-REAL-024",
        "V02-REAL-030",
    }
    assert set(baseline) == set(candidate)
    assert len(incomparable) == 5
    assert all(
        "evaluation-flaw" in baseline[case_id]["classification"]["problem_classes"]
        for case_id in incomparable
    )

    totals = summarize(ROOT)
    assert totals["baseline"]["runs"] == 50
    assert totals["v0.2"]["runs"] == 50
    assert totals["baseline"].get("evidence_supported_successes", 0) == 0
    assert totals["v0.2"]["evidence_supported_successes"] == 3


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
    assert all(run["metrics"]["reviewer_misses"] is None for run in real_runs.values())
    assert all(
        run["metrics"]["predeclared_expected_findings_missed"] is None
        for run in real_runs.values()
    )


def test_v02_run_corpus_validates_against_the_run_record_schema() -> None:
    schema = _load(EVAL_ROOT / "schemas/run-record.schema.json")
    validator = jsonschema.Draft202012Validator(schema)
    paths = sorted((EVAL_ROOT / "results").glob("*/*/run.json")) + sorted(
        (EVAL_ROOT / "supplemental" / "results").glob("*/*/run.json")
    )

    assert len(paths) == 110
    for path in paths:
        validator.validate(_load(path))


def test_v02_candidate_records_use_one_full_candidate_revision() -> None:
    candidate_runs = list(_runs("v0.2").values()) + list(
        _supplemental_runs("v0.2").values()
    )
    commits = {run["skill_commit"] for run in candidate_runs}

    assert len(candidate_runs) == 55
    assert commits == {"4438280c502e1e0d9e667e841206cc19b8e6521e"}
    assert all(re.fullmatch(r"[0-9a-f]{40}", commit) for commit in commits)


def test_v02_acceptance_score_uses_raw_evidence_not_recorded_booleans() -> None:
    record_path = EVAL_ROOT / "results/v0.2/V02-REAL-014/run.json"
    record = _load(record_path)
    mutated = deepcopy(record)
    mutated["metrics"]["task_success"] = False
    mutated["metrics"]["acceptance_success"] = False

    assert observed_success(ROOT, record, record_path)
    assert observed_success(ROOT, mutated, record_path)
    totals = summarize(ROOT)["v0.2"]
    assert totals["evidence_supported_successes"] == 3
    assert totals["structural_only"] == 18
    assert totals["inconclusive_acceptance"] == 21


def test_v02_real_structural_validation_is_not_scored_as_behavioral_acceptance() -> None:
    real_014 = _runs("v0.2")["V02-REAL-014"]
    structural_only = _runs("v0.2")["V02-REAL-013"]

    assert real_014["acceptance_evidence"]["kind"] == "behavioral-probe"
    assert real_014["acceptance_evidence"]["status"] == "pass"
    assert structural_only["acceptance_evidence"] == {
        "kind": "structural-only",
        "status": "unavailable",
        "path": "evals/v0.2/results/v0.2/V02-REAL-013/validation.txt",
        "criteria": [],
    }
    assert structural_only["metrics"]["acceptance_success"] is None


def test_v02_scorer_rejects_an_adversarial_record_artifact_mismatch(
    tmp_path: Path,
) -> None:
    record_path = EVAL_ROOT / "results/v0.2/V02-REAL-014/run.json"
    record = _load(record_path)
    failed_probe = tmp_path / "failed-probe.txt"
    failed_probe.write_text(
        "ECLIPSE_ACCEPTANCE_EVIDENCE: FAIL\nexit_code: 1\n",
        encoding="utf-8",
    )
    mismatched = deepcopy(record)
    mismatched["acceptance_evidence"]["status"] = "pass"
    mismatched["acceptance_evidence"]["path"] = str(failed_probe)

    assert not observed_success(ROOT, mismatched, record_path)


def test_v02_behavioral_probe_requires_marker_and_zero_exit_code(
    tmp_path: Path,
) -> None:
    record_path = EVAL_ROOT / "results/v0.2/V02-REAL-014/run.json"
    record = _load(record_path)
    marker_only = tmp_path / "marker-only.txt"
    marker_only.write_text("ECLIPSE_ACCEPTANCE_EVIDENCE: PASS\n", encoding="utf-8")
    mismatched = deepcopy(record)
    mismatched["acceptance_evidence"]["path"] = str(marker_only)

    assert not observed_success(ROOT, mismatched, record_path)


def test_v02_supplemental_campaign_exercises_correction_cases() -> None:
    cases = _load(EVAL_ROOT / "supplemental/cases.json")["cases"]
    baseline = _supplemental_runs("baseline")
    candidate = _supplemental_runs("v0.2")

    assert len(cases) == len(baseline) == len(candidate) == 5
    assert sum(case["case_type"] == "real" for case in cases) == 3
    assert all(case["task_category"] == "review-correction" for case in cases[2:])
    assert all(len(case["candidate_states"]) == 2 for case in cases)
    assert not (EVAL_ROOT / "supplemental/evidence").exists()
    for case in cases:
        for relative in case["candidate_states"]:
            patch = EVAL_ROOT / "supplemental" / relative
            assert patch.read_text(encoding="utf-8").startswith("diff --git ")
        assert baseline[case["case_id"]]["metrics"]["correction_cycles"] == 2
        assert candidate[case["case_id"]]["metrics"]["correction_cycles"] == 2
        assert candidate[case["case_id"]]["metrics"]["reviewer_misses"] is None
        assert (
            candidate[case["case_id"]]["metrics"]
            ["predeclared_expected_findings_missed"]
            == 0
        )
        for run in (baseline[case["case_id"]], candidate[case["case_id"]]):
            artifacts = run["artifacts"]
            assert len(artifacts["worker_rounds"]) == 2
            assert len(artifacts["review_rounds"]) == 2
            task = TaskContract.from_dict(_load(ROOT / artifacts["task"]))
            _assert_supplemental_task_binding(task.data, case)
            workers = [
                ResultContract.from_dict(_load(ROOT / path))
                for path in artifacts["worker_rounds"]
            ]
            reviews = [
                ReviewContract.from_dict(_load(ROOT / path))
                for path in artifacts["review_rounds"]
            ]
            for worker, review in zip(workers, reviews, strict=True):
                _assert_supplemental_result_binding(worker.data, root=ROOT)
                transcript = ROOT / worker.data["metadata"]["validation_evidence"]
                evidence = transcript.read_text(encoding="utf-8")
                command = worker.data["commands"][0]
                assert f"declared_command: {command['command']}" in evidence
                assert "stdout:" in evidence and "stderr:" in evidence
                expected_exit = (
                    f"exit_code: {command['exit_code']}"
                    if command["exit_code"] is not None
                    else "exit_code: unavailable"
                )
                assert expected_exit in evidence
                validate_result_against_task(worker, task)
                validate_review_against_result(review, worker, task)
            assert all(
                _load(ROOT / path)["review_round"] == round_number
                for round_number, path in enumerate(artifacts["review_rounds"], start=1)
            )


def test_v02_supplemental_task_binding_rejects_frozen_case_drift() -> None:
    case = _load(EVAL_ROOT / "supplemental/cases.json")["cases"][0]
    task = _load(
        EVAL_ROOT
        / "supplemental/results/v0.2/V02-SUP-FIX-01/role-artifacts/task-contract.json"
    )
    task["validation"][0]["command"] = "python -m unittest"

    with pytest.raises(AssertionError, match="validation commands"):
        _assert_supplemental_task_binding(task, case)


def test_v02_supplemental_result_binding_rejects_patch_file_or_digest_drift() -> None:
    result = _load(
        EVAL_ROOT
        / "supplemental/results/v0.2/V02-SUP-REAL-001/role-artifacts/worker-round-1.json"
    )
    wrong_files = deepcopy(result)
    wrong_files["files_changed"] = ["README.md"]
    wrong_files["git"]["changed_files_digest"] = digest_json(["README.md"])
    with pytest.raises(AssertionError, match="files_changed"):
        _assert_supplemental_result_binding(wrong_files, root=ROOT)

    wrong_digest = deepcopy(result)
    wrong_digest["git"]["changed_files_digest"] = digest_json([])
    with pytest.raises(AssertionError, match="changed-files digest"):
        _assert_supplemental_result_binding(wrong_digest, root=ROOT)


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
