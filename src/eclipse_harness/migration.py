"""Conservative migration from recognizable soluna-workflow layouts."""

from __future__ import annotations

import shutil
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from .authorization import ensure_repository_bounded
from .config import DEFAULT_CONFIG, validate_config
from .errors import ConfigurationError
from .jsonutil import write_json_atomic
from .tomlutil import load_toml


@dataclass(frozen=True)
class MigrationItem:
    source: str
    disposition: str
    detail: str

    def to_dict(self) -> dict[str, str]:
        return {"source": self.source, "disposition": self.disposition, "detail": self.detail}


@dataclass(frozen=True)
class MigrationResult:
    detected: bool
    config: Mapping[str, Any]
    items: tuple[MigrationItem, ...]
    warnings: tuple[str, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": "1.0",
            "source": "soluna-workflow",
            "detected": self.detected,
            "items": [item.to_dict() for item in self.items],
            "warnings": list(self.warnings),
        }


def inspect_soluna_workflow(source: Path) -> MigrationResult:
    source = source.resolve()
    config_path = ensure_repository_bounded(source, ".codex/config.toml")
    plan_path = ensure_repository_bounded(source, "plans/ACTIVE_PLAN.md")
    handoff_path = ensure_repository_bounded(source, "plans/HANDOFF.md")
    context_path = ensure_repository_bounded(source, "docs/ai/PROJECT_CONTEXT.md")
    detected = config_path.is_file() or plan_path.is_file() or context_path.is_file()
    if not detected:
        raise ConfigurationError(f"no recognizable soluna-workflow layout under {source}")
    config = _copy_config()
    items: list[MigrationItem] = []
    warnings: list[str] = []
    if config_path.is_file():
        if config_path.stat().st_size > 1024 * 1024:
            raise ConfigurationError("legacy config exceeds the 1 MiB migration limit")
        try:
            with config_path.open("rb") as handle:
                legacy = load_toml(handle)
        except ValueError as error:
            raise ConfigurationError(f"legacy config is invalid TOML: {error}") from error
        agents = legacy.get("agents", {})
        if isinstance(agents, dict):
            legacy_threads = agents.get("max_concurrent_threads_per_session", agents.get("max_threads"))
            if isinstance(legacy_threads, int) and not isinstance(legacy_threads, bool):
                config["concurrency"]["max_parallel_writers"] = min(max(legacy_threads, 1), 2)
                items.append(
                    MigrationItem(
                        ".codex/config.toml:max_threads",
                        "mapped",
                        "mapped conservatively to max_parallel_writers; generated Codex config uses the canonical field",
                    )
                )
            if "max_depth" in agents:
                items.append(
                    MigrationItem(
                        ".codex/config.toml:max_depth",
                        "not-mapped",
                        "not treated as V2 recursion protection; worker adapters disable agents instead",
                    )
                )
                warnings.append("legacy max_depth did not provide a portable recursion guarantee")
    if context_path.is_file():
        items.append(
            MigrationItem(
                "docs/ai/PROJECT_CONTEXT.md",
                "preserve",
                "copied verbatim for human review; repository content remains untrusted context",
            )
        )
    for path in (plan_path, handoff_path):
        if path.is_file():
            items.append(
                MigrationItem(
                    str(path.relative_to(source)).replace("\\", "/"),
                    "archive-for-manual-conversion",
                    "preserved but not asserted as canonical; prose cannot be losslessly converted without semantic review",
                )
            )
    items.append(
        MigrationItem(
            "legacy custom agents",
            "replace-generated",
            "role intent maps to Eclipse policy; current host profiles must be regenerated",
        )
    )
    validate_config(config)
    return MigrationResult(True, config, tuple(items), tuple(warnings))


def write_migration(
    source: Path,
    output: Path,
    result: MigrationResult,
    *,
    dry_run: bool = False,
) -> tuple[str, ...]:
    source = source.resolve()
    output = output.resolve()
    planned = [".eclipse/config.json", ".eclipse/migration-report.json"]
    context = ensure_repository_bounded(source, "docs/ai/PROJECT_CONTEXT.md")
    plan = ensure_repository_bounded(source, "plans/ACTIVE_PLAN.md")
    handoff = ensure_repository_bounded(source, "plans/HANDOFF.md")
    if context.is_file():
        planned.append("docs/ai/PROJECT_CONTEXT.legacy.md")
    if plan.is_file():
        planned.append(".eclipse/migration/ACTIVE_PLAN.legacy.md")
    if handoff.is_file():
        planned.append(".eclipse/migration/HANDOFF.legacy.md")
    if dry_run:
        return tuple(planned)
    targets = {relative: ensure_repository_bounded(output, relative) for relative in planned}
    conflicts = [relative for relative, target in targets.items() if target.exists()]
    if conflicts:
        raise ConfigurationError(
            "migration refuses to overwrite existing path(s): " + ", ".join(conflicts)
        )
    write_json_atomic(targets[planned[0]], result.config)
    write_json_atomic(targets[planned[1]], result.to_dict())
    copies = (
        (context, targets.get("docs/ai/PROJECT_CONTEXT.legacy.md")),
        (plan, targets.get(".eclipse/migration/ACTIVE_PLAN.legacy.md")),
        (handoff, targets.get(".eclipse/migration/HANDOFF.legacy.md")),
    )
    for source_path, target_path in copies:
        if source_path.is_file() and target_path is not None:
            target_path.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source_path, target_path)
    return tuple(planned)


def _copy_config() -> dict[str, Any]:
    import copy

    return copy.deepcopy(DEFAULT_CONFIG)
