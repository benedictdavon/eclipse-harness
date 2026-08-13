"""Optional validation, adapter, diagnostic, and evaluation CLI."""

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
from .concurrency import execution_waves
from .contracts import (
    ContextManifest,
    ResultContract,
    ReviewContract,
    TaskContract,
    validate_result_against_task,
    validate_review_against_result,
)
from .doctor import run_doctor, write_snapshot
from .errors import EclipseError
from .evaluation import RecordedHost, run_suite
from .jsonutil import load_json
from .routing import Policy
from .security import scan_for_secrets


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="eclipse",
        description="Optional validators and adapters for the Eclipse skills and contracts.",
    )
    parser.add_argument("--root", type=Path, default=Path.cwd(), help="repository root")
    parser.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    sub = parser.add_subparsers(dest="command", required=True)

    init = sub.add_parser("init", help="copy packaged Eclipse skills without overwriting files")
    init.add_argument("--dry-run", action="store_true")

    validate = sub.add_parser("validate", help="validate an Eclipse protocol contract")
    validate.add_argument("file", type=Path)
    validate.add_argument(
        "--kind",
        choices=("auto", "context", "task", "result", "review"),
        default="auto",
    )
    validate.add_argument("--task", type=Path, help="governing task for semantic validation")
    validate.add_argument("--result", type=Path, help="worker result for review validation")

    inspect = sub.add_parser("inspect", help="report contract kind, version, and digest")
    inspect.add_argument("file", type=Path)

    concurrency = sub.add_parser(
        "check-concurrency",
        help="validate a task DAG and serialize it into ownership-safe execution waves",
    )
    concurrency.add_argument("contracts", nargs="+", type=Path)
    concurrency.add_argument("--max-writers", type=int, default=2)

    doctor = sub.add_parser("doctor", help="diagnose host-specific routes and permissions")
    doctor.add_argument("--observations", type=Path)
    doctor.add_argument(
        "--trust-observations",
        action="store_true",
        help="treat explicitly supplied observations as user-attested host metadata",
    )
    doctor.add_argument("--write-snapshot", action="store_true")

    adapters = sub.add_parser("adapters", help="generate host-specific skill wrappers")
    adapters_sub = adapters.add_subparsers(dest="adapters_command", required=True)
    generate = adapters_sub.add_parser("generate", help="generate Codex/Copilot profiles")
    generate.add_argument("--host", choices=("codex", "copilot", "all"), default="all")
    generate.add_argument("--output", type=Path)
    generate.add_argument(
        "--max-concurrency",
        type=int,
        help="Codex-only maximum concurrent agent threads (default: 2)",
    )
    generate.add_argument("--dry-run", action="store_true")

    evaluate = sub.add_parser("eval", help="run deterministic evaluation cases")
    eval_sub = evaluate.add_subparsers(dest="eval_command", required=True)
    eval_run = eval_sub.add_parser("run", help="run a suite with recorded outcomes")
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


def _contract_kind(data: Mapping[str, Any]) -> str:
    if "task_contract_digest" in data and "outcome" in data:
        return "review"
    if "task_contract_digest" in data:
        return "result"
    if "task_id" in data:
        return "task"
    if set(data) == {"schema_version", "summary", "references", "trusted_sources"}:
        return "context"
    raise ValueError("could not infer contract kind; pass --kind")


def _validate(
    path: Path,
    kind: str,
    task_path: Path | None,
    result_path: Path | None,
) -> Mapping[str, Any]:
    data = _mapping(path)
    if kind == "auto":
        kind = _contract_kind(data)
    if kind == "context":
        contract: Any = ContextManifest.from_dict(data)
    elif kind == "task":
        contract = TaskContract.from_dict(data)
    elif kind == "result":
        contract = ResultContract.from_dict(data)
        if task_path is not None:
            validate_result_against_task(contract, TaskContract.from_dict(_mapping(task_path)))
    else:
        contract = ReviewContract.from_dict(data)
        if (task_path is None) != (result_path is None):
            raise ValueError("review semantic validation requires both --task and --result")
        if task_path is not None and result_path is not None:
            task = TaskContract.from_dict(_mapping(task_path))
            result = ResultContract.from_dict(_mapping(result_path))
            validate_review_against_result(contract, result, task)
    findings = scan_for_secrets(data)
    if findings:
        raise ValueError(
            "contract contains probable secret(s): "
            + ", ".join(f"{item.path}:{item.kind}" for item in findings)
        )
    return {
        "valid": True,
        "kind": kind,
        "schema_version": data.get("schema_version", "embedded"),
        "digest": contract.digest,
    }


def _init(root: Path, *, dry_run: bool) -> Mapping[str, Any]:
    source_root = _installed_share() / "skills"
    target_root = ensure_repository_bounded(root, ".agents/skills")
    if not source_root.is_dir():
        if target_root.is_dir():
            return {
                "skills": "already present in repository",
                "installed": [],
                "dry_run": dry_run,
            }
        raise ValueError("packaged Eclipse skills are unavailable; copy .agents/skills manually")
    actions: list[dict[str, str]] = []
    for source in sorted(source_root.iterdir()):
        target = target_root / source.name
        action = "unchanged" if target.exists() else "create"
        actions.append({"skill": source.name, "action": action})
        if action == "create" and not dry_run:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copytree(source, target)
    return {"skills": "checked", "actions": actions, "dry_run": dry_run}


def _run(arguments: argparse.Namespace) -> tuple[int, Any]:
    root = arguments.root.resolve()
    if arguments.command == "init":
        return 0, _init(root, dry_run=arguments.dry_run)
    if arguments.command == "validate":
        return 0, _validate(
            arguments.file,
            arguments.kind,
            arguments.task,
            arguments.result,
        )
    if arguments.command == "inspect":
        return 0, _validate(arguments.file, "auto", None, None)
    if arguments.command == "check-concurrency":
        tasks = [TaskContract.from_dict(_mapping(path)) for path in arguments.contracts]
        waves = execution_waves(tasks, max_parallel_writers=arguments.max_writers)
        return 0, {"dag_valid": True, "waves": waves}
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
        if arguments.host == "copilot" and arguments.max_concurrency is not None:
            raise ValueError("--max-concurrency applies only to the Codex adapter")
        hosts = ("codex", "copilot") if arguments.host == "all" else (arguments.host,)
        artifacts: list[AdapterArtifact] = []
        for host in hosts:
            if host == "codex":
                maximum = 2 if arguments.max_concurrency is None else arguments.max_concurrency
                artifacts.extend(CodexAdapter().render(policy, max_concurrency=maximum))
            else:
                artifacts.extend(CopilotAdapter().render(policy))
        output = (arguments.output or root).resolve()
        actions = install_artifacts(output, artifacts, dry_run=arguments.dry_run)
        return 0, {"actions": [item.__dict__ for item in actions], "output": str(output)}
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
