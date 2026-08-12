"""Standard-library validation for constrained development environments."""

from __future__ import annotations

import copy
import json
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).parents[1]
sys.path.insert(0, str(ROOT / "src"))

from eclipse_harness.adapters import CodexAdapter, CopilotAdapter, install_artifacts
from eclipse_harness.authorization import authorize_changed_files
from eclipse_harness.concurrency import assert_parallel_safe
from eclipse_harness.contracts import (
    ResultContract,
    ReviewContract,
    TaskContract,
    validate_result_against_task,
    validate_review_against_result,
)
from eclipse_harness.doctor import run_doctor
from eclipse_harness.evaluation import RecordedHost, run_suite
from eclipse_harness.migration import inspect_soluna_workflow, write_migration
from eclipse_harness.render import render_active_plan, render_handoff
from eclipse_harness.routing import Policy
from eclipse_harness.state import TaskState
from eclipse_harness.store import ReviewAttestation, RunStore


def load(path: str) -> dict[str, object]:
    value = json.loads((ROOT / path).read_text(encoding="utf-8"))
    assert isinstance(value, dict)
    return value


def main() -> None:
    task = TaskContract.from_dict(load("examples/contracts/task.json"))
    result_data = load("examples/contracts/result.json")
    result_data["task_contract_digest"] = task.digest
    result = ResultContract.from_dict(result_data)
    review_data = load("examples/contracts/review.json")
    review_data["task_contract_digest"] = task.digest
    review_data["result_digest"] = result.digest
    review = ReviewContract.from_dict(review_data)
    validate_result_against_task(result, task)
    validate_review_against_result(review, result, task)
    authorize_changed_files(task, result.data["files_changed"])

    disjoint_data = copy.deepcopy(task.data)
    disjoint_data["task_id"] = "T002"
    disjoint_data["scope"]["write_globs"] = ["src/independent/**"]
    assert_parallel_safe([task, TaskContract.from_dict(disjoint_data)])

    policy = Policy.from_dict(load("policies/sol-luna.json"))
    codex = CodexAdapter().render(policy)
    copilot = CopilotAdapter().render(policy)
    assert len(codex) == 5 and len(copilot) == 3
    snapshot = run_doctor(ROOT, policy)
    assert snapshot.routes["worker"]["effective_model"] is None

    with tempfile.TemporaryDirectory() as temporary:
        target = Path(temporary)
        install_artifacts(target, (*codex, *copilot))
        store = RunStore(target)
        store.create_run(
            task.run_id,
            "Example",
            task.plan_digest,
            str(task.data["provenance"]["base_revision"]),
        )
        state = store.add_task(task.run_id, task)
        assert state.tasks[task.task_id].state is TaskState.READY
        store.start_task(task.run_id, task.task_id)
        store.ingest_result(
            task.run_id, result, observed_files=result.data["files_changed"]
        )
        state = store.ingest_review(
            task.run_id, review, attestation=ReviewAttestation.human("self-check")
        )
        assert state.tasks[task.task_id].state is TaskState.ACCEPTED
        assert "accepted" in render_active_plan(state)
        assert "final human completion" in render_handoff(state)

        migration = inspect_soluna_workflow(ROOT / "tests/fixtures/legacy-soluna")
        write_migration(ROOT / "tests/fixtures/legacy-soluna", target / "migration", migration)
        assert (target / "migration/.eclipse/config.json").is_file()

        outcomes = load("examples/evaluation/recorded-outcomes.json")
        report = run_suite(
            ROOT / "examples/evaluation/suite.json",
            RecordedHost(outcomes),
            target / "evaluation.json",
        )
        assert report["conclusion"] is None

    for schema in (ROOT / "schemas").glob("*.json"):
        assert isinstance(json.loads(schema.read_text(encoding="utf-8")), dict)
    print("self-check: PASS")


if __name__ == "__main__":
    main()
