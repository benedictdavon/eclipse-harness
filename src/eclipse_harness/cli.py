"""Professional, cross-platform Eclipse Harness command line."""

from __future__ import annotations

import argparse
import json
import shutil
import sys
import sysconfig
from pathlib import Path
from typing import Any, Mapping, Sequence

from .adapters import AdapterArtifact, CodexAdapter, CopilotAdapter, install_artifacts
from .authorization import ensure_repository_bounded
from .concurrency import assert_parallel_safe, execution_waves
from .config import load_config, write_default_config
from .contracts import ResultContract, ReviewContract, TaskContract
from .doctor import run_doctor, write_snapshot
from .errors import EclipseError
from .evaluation import RecordedHost, run_suite
from .gitops import GitRepository, WorktreeSpec
from .jsonutil import load_json
from .migration import inspect_soluna_workflow, write_migration
from .render import write_views
from .routing import Policy
from .security import scan_for_secrets
from .store import ReviewAttestation, RunStore


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="eclipse",
        description="Portable architect-worker-reviewer contracts and validation.",
    )
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="repository root")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="initialize non-destructive Eclipse project state")
    init.add_argument("--dry-run", action="store_true")

    validate = sub.add_parser("validate", help="validate a contract or Eclipse configuration")
    validate.add_argument("file", type=Path)
    validate.add_argument(
        "--kind", choices=("auto", "task", "result", "review", "config"), default="auto"
    )
    validate.add_argument("--task", type=Path, help="task contract for semantic result validation")

    inspect = sub.add_parser("inspect", help="inspect a validated contract")
    inspect.add_argument("file", type=Path)

    plan = sub.add_parser("plan", help="create, revise, or populate canonical run state")
    plan_sub = plan.add_subparsers(dest="plan_command", required=True)
    plan_create = plan_sub.add_parser("create", help="create a run and plan revision 1")
    plan_create.add_argument("--run-id", required=True)
    plan_create.add_argument("--objective", required=True)
    plan_create.add_argument("--plan-digest", required=True)
    plan_create.add_argument("--base-revision", required=True)
    plan_add = plan_sub.add_parser("add-task", help="add a validated task contract")
    plan_add.add_argument("--run-id", required=True)
    plan_add.add_argument("contract", type=Path)
    plan_revise = plan_sub.add_parser("revise", help="supersede active tasks with a new plan")
    plan_revise.add_argument("--run-id", required=True)
    plan_revise.add_argument("--plan-digest", required=True)
    plan_revise.add_argument("--base-revision", required=True)

    task = sub.add_parser("task", help="advance task execution state")
    task_sub = task.add_subparsers(dest="task_command", required=True)
    task_start = task_sub.add_parser("start", help="start a ready task attempt")
    task_start.add_argument("--run-id", required=True)
    task_start.add_argument("--task-id", required=True)

    result = sub.add_parser("result", help="ingest structured worker evidence")
    result_sub = result.add_subparsers(dest="result_command", required=True)
    result_ingest = result_sub.add_parser("ingest", help="validate and ingest one result")
    result_ingest.add_argument("--run-id", required=True)
    result_ingest.add_argument(
        "--observed-file",
        action="append",
        help="trusted changed path; repeat outside a Git worktree",
    )
    result_ingest.add_argument("file", type=Path)

    review = sub.add_parser("review", help="ingest independent structured review")
    review_sub = review.add_subparsers(dest="review_command", required=True)
    review_ingest = review_sub.add_parser("ingest", help="validate and ingest one review")
    review_ingest.add_argument("--run-id", required=True)
    review_ingest.add_argument(
        "--human-approval",
        action="store_true",
        help="explicitly attest that a human approved this review evidence",
    )
    review_ingest.add_argument("--principal", help="human principal recording approval")
    review_ingest.add_argument("file", type=Path)

    status = sub.add_parser("status", help="show canonical run status")
    status.add_argument("run_id")

    render = sub.add_parser("render", help="render ACTIVE_PLAN and HANDOFF from run.json")
    render.add_argument("run_id")
    render.add_argument("--output", type=Path, default=Path("plans"))

    concurrency = sub.add_parser("check-concurrency", help="check DAG and write ownership")
    concurrency.add_argument("contracts", nargs="+", type=Path)
    concurrency.add_argument("--max-writers", type=int, default=2)

    doctor = sub.add_parser("doctor", help="diagnose host, routes, permissions, and adapters")
    doctor.add_argument("--observations", type=Path)
    doctor.add_argument(
        "--trust-observations",
        action="store_true",
        help="treat explicitly supplied observations as user-attested host metadata",
    )
    doctor.add_argument("--write-snapshot", action="store_true")

    adapters = sub.add_parser("adapters", help="generate current host-specific wrappers")
    adapters_sub = adapters.add_subparsers(dest="adapters_command", required=True)
    generate = adapters_sub.add_parser("generate", help="generate Codex/Copilot profiles")
    generate.add_argument("--host", choices=("codex", "copilot", "all"), default="all")
    generate.add_argument("--output", type=Path)
    generate.add_argument("--dry-run", action="store_true")

    migrate = sub.add_parser("migrate", help="migrate recognizable prior workflow state")
    migrate_sub = migrate.add_subparsers(dest="migrate_command", required=True)
    soluna = migrate_sub.add_parser("soluna-workflow", help="migrate from soluna-workflow")
    soluna.add_argument("source", type=Path)
    soluna.add_argument("--output", type=Path)
    soluna.add_argument("--dry-run", action="store_true")

    worktree = sub.add_parser("worktree", help="prepare task git isolation")
    worktree_sub = worktree.add_subparsers(dest="worktree_command", required=True)
    prepare = worktree_sub.add_parser("prepare", help="create an isolated branch and worktree")
    prepare.add_argument("contract", type=Path)
    prepare.add_argument("--path", required=True, type=Path)
    prepare.add_argument("--branch", required=True)

    evaluate = sub.add_parser("eval", help="run deterministic or live evaluation suites")
    eval_sub = evaluate.add_subparsers(dest="eval_command", required=True)
    eval_run = eval_sub.add_parser("run", help="run a suite with recorded CI outcomes")
    eval_run.add_argument("suite", type=Path)
    eval_run.add_argument("--outcomes", required=True, type=Path)
    eval_run.add_argument("--output", required=True, type=Path)
    return parser


def _mapping(path: Path) -> Mapping[str, Any]:
    value = load_json(path)
    if not isinstance(value, dict):
        raise ValueError(f"{path} must contain a JSON object")
    return value


def _policy(root: Path) -> Policy:
    path = root / "policies" / "sol-luna.json"
    if not path.is_file():
        path = _installed_share() / "sol-luna.json"
    return Policy.from_dict(_mapping(path))


def _installed_share() -> Path:
    return Path(sysconfig.get_path("data")) / "share" / "eclipse-harness"


def _emit(value: Any, *, json_output: bool) -> None:
    if json_output:
        print(json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2))
    elif isinstance(value, str):
        print(value)
    elif isinstance(value, Mapping):
        for key, item in value.items():
            print(f"{key}: {item}")
    else:
        print(value)


def _validate(path: Path, kind: str, task_path: Path | None) -> Mapping[str, Any]:
    data = _mapping(path)
    if kind == "auto":
        if "task_contract_digest" in data and "outcome" in data:
            kind = "review"
        elif "task_contract_digest" in data:
            kind = "result"
        elif "task_id" in data:
            kind = "task"
        else:
            kind = "config"
    if kind == "task":
        contract: Any = TaskContract.from_dict(data)
    elif kind == "result":
        contract = ResultContract.from_dict(data)
        if task_path is not None:
            from .contracts import validate_result_against_task

            validate_result_against_task(contract, TaskContract.from_dict(_mapping(task_path)))
    elif kind == "review":
        contract = ReviewContract.from_dict(data)
    else:
        contract = load_config(path)
        return {"valid": True, "kind": "config", "schema_version": data["schema_version"]}
    findings = scan_for_secrets(data)
    if findings:
        raise ValueError(
            "contract contains probable secret(s): "
            + ", ".join(f"{item.path}:{item.kind}" for item in findings)
        )
    return {
        "valid": True,
        "kind": kind,
        "schema_version": data["schema_version"],
        "digest": contract.digest,
    }


def _init(root: Path, *, dry_run: bool) -> Mapping[str, Any]:
    config_path = ensure_repository_bounded(root, ".eclipse/config.json")
    if config_path.exists():
        load_config(config_path)
        config_action = "unchanged"
    else:
        config_action = "create"
        if not dry_run:
            write_default_config(config_path)
    skill_source = root / ".agents" / "skills"
    if not skill_source.is_dir():
        skill_source = _installed_share() / "skills"
    installed: list[str] = []
    if skill_source.is_dir() and skill_source.resolve() != (root / ".agents" / "skills").resolve():
        for source in sorted(skill_source.iterdir()):
            target = ensure_repository_bounded(root, f".agents/skills/{source.name}")
            if target.exists():
                continue
            installed.append(source.name)
            if not dry_run:
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copytree(source, target)
    return {"config": config_action, "skills_installed": installed, "dry_run": dry_run}


def _run(arguments: argparse.Namespace) -> tuple[int, Any]:
    root = arguments.root.resolve()
    store = RunStore(root)
    if arguments.command == "init":
        return 0, _init(root, dry_run=arguments.dry_run)
    if arguments.command == "validate":
        return 0, _validate(arguments.file, arguments.kind, arguments.task)
    if arguments.command == "inspect":
        return 0, _validate(arguments.file, "auto", None)
    if arguments.command == "plan":
        if arguments.plan_command == "create":
            state = store.create_run(
                arguments.run_id,
                arguments.objective,
                arguments.plan_digest,
                arguments.base_revision,
            )
        elif arguments.plan_command == "add-task":
            state = store.add_task(
                arguments.run_id, TaskContract.from_dict(_mapping(arguments.contract))
            )
        else:
            state = store.revise_plan(
                arguments.run_id, arguments.plan_digest, arguments.base_revision
            )
        return 0, state.to_dict()
    if arguments.command == "task":
        return 0, store.start_task(arguments.run_id, arguments.task_id).to_dict()
    if arguments.command == "result":
        result = ResultContract.from_dict(_mapping(arguments.file))
        return 0, store.ingest_result(
            arguments.run_id, result, observed_files=arguments.observed_file
        ).to_dict()
    if arguments.command == "review":
        if not arguments.human_approval or not arguments.principal:
            raise ValueError("review ingestion requires --human-approval and --principal")
        review = ReviewContract.from_dict(_mapping(arguments.file))
        return 0, store.ingest_review(
            arguments.run_id,
            review,
            attestation=ReviewAttestation.human(arguments.principal),
        ).to_dict()
    if arguments.command == "status":
        return 0, store.load(arguments.run_id).to_dict()
    if arguments.command == "render":
        output = ensure_repository_bounded(root, arguments.output.as_posix())
        paths = write_views(store.load(arguments.run_id), output)
        return 0, {"active_plan": str(paths[0]), "handoff": str(paths[1])}
    if arguments.command == "check-concurrency":
        tasks = [TaskContract.from_dict(_mapping(path)) for path in arguments.contracts]
        assert_parallel_safe(tasks)
        waves = execution_waves(tasks, max_parallel_writers=arguments.max_writers)
        return 0, {"safe": True, "waves": waves}
    if arguments.command == "doctor":
        snapshot = run_doctor(
            root,
            _policy(root),
            observation_file=arguments.observations,
            trust_observations=arguments.trust_observations,
        )
        if arguments.write_snapshot:
            write_snapshot(
                ensure_repository_bounded(root, ".eclipse/capabilities.json"), snapshot
            )
        return (0 if snapshot.healthy else 3), snapshot.to_dict()
    if arguments.command == "adapters":
        policy = _policy(root)
        config_path = root / ".eclipse" / "config.json"
        config = load_config(config_path) if config_path.is_file() else None
        max_concurrency = config.max_parallel_writers if config else 2
        hosts = ("codex", "copilot") if arguments.host == "all" else (arguments.host,)
        artifacts: list[AdapterArtifact] = []
        for host in hosts:
            adapter = CodexAdapter() if host == "codex" else CopilotAdapter()
            artifacts.extend(adapter.render(policy, max_concurrency=max_concurrency))
        output = (arguments.output or root).resolve()
        actions = install_artifacts(output, artifacts, dry_run=arguments.dry_run)
        return 0, {"actions": [item.__dict__ for item in actions], "output": str(output)}
    if arguments.command == "migrate":
        output = (arguments.output or root).resolve()
        migration = inspect_soluna_workflow(arguments.source)
        files = write_migration(
            arguments.source, output, migration, dry_run=arguments.dry_run
        )
        return 0, {**migration.to_dict(), "files": files, "dry_run": arguments.dry_run}
    if arguments.command == "worktree":
        supplied = TaskContract.from_dict(_mapping(arguments.contract))
        task = store.load_task(supplied.run_id, supplied.task_id)
        if task.digest != supplied.digest:
            raise ValueError("worktree contract does not match canonical run record")
        state = store.load(task.run_id)
        repository = GitRepository(root)
        base = str(task.data["provenance"]["base_revision"])
        if base != state.base_revision:
            raise ValueError("task base revision does not match canonical run state")
        repository.verify_base(base)
        scope = task.scope
        if scope["isolation"] != "worktree":
            raise ValueError("task contract must request worktree isolation")
        command_result = repository.prepare_worktree(
            WorktreeSpec(task.task_id, base, arguments.branch, arguments.path.resolve())
        )
        return 0, {"command": command_result.command, "path": str(arguments.path.resolve())}
    if arguments.command == "eval":
        outcomes = _mapping(arguments.outcomes)
        report = run_suite(arguments.suite, RecordedHost(outcomes), arguments.output)
        return 0, report
    raise AssertionError(f"unhandled command: {arguments.command}")


def main(argv: Sequence[str] | None = None) -> int:
    parser = _parser()
    arguments = parser.parse_args(argv)
    try:
        exit_code, result = _run(arguments)
        _emit(result, json_output=arguments.json)
        return exit_code
    except (EclipseError, OSError, ValueError, KeyError, TypeError) as error:
        payload = {"error": type(error).__name__, "message": str(error)}
        if arguments.json:
            print(json.dumps(payload, sort_keys=True), file=sys.stderr)
        else:
            print(f"error: {error}", file=sys.stderr)
        return error.exit_code if isinstance(error, EclipseError) else 2


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
