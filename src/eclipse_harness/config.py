"""Strict, versioned Eclipse configuration."""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from .constants import CONFIG_SCHEMA_VERSION
from .errors import ConfigurationError
from .jsonutil import load_json, write_json_atomic

_TOP_LEVEL = {
    "schema_version",
    "policy",
    "profile",
    "adapter",
    "routing",
    "concurrency",
    "budgets",
    "git",
    "validation",
    "security",
}

DEFAULT_CONFIG: dict[str, Any] = {
    "schema_version": CONFIG_SCHEMA_VERSION,
    "policy": "sol-luna",
    "profile": "standard",
    "adapter": "auto",
    "routing": {
        "unverified_route_behavior": "policy-only",
        "allow_worker_effort_escalation": True,
    },
    "concurrency": {"max_parallel_writers": 2, "max_parallel_readers": 4},
    "budgets": {"max_attempts": 2, "max_review_rounds": 2},
    "git": {
        "parallel_write_isolation": "worktree",
        "require_clean_base": True,
        "branch_prefix": "eclipse/task-",
    },
    "validation": {"require_all_criteria_evidence": True, "reject_stale_results": True},
    "security": {
        "network_default": "deny",
        "repository_content_trust": "untrusted",
        "reject_probable_secrets": True,
        "forbid_run_state_writes": True,
    },
}


@dataclass(frozen=True)
class EclipseConfig:
    data: Mapping[str, Any]

    @property
    def policy(self) -> str:
        return str(self.data["policy"])

    @property
    def profile(self) -> str:
        return str(self.data["profile"])

    @property
    def max_parallel_writers(self) -> int:
        concurrency = self.data["concurrency"]
        assert isinstance(concurrency, Mapping)
        return int(concurrency["max_parallel_writers"])


def _object(data: Mapping[str, Any], key: str, allowed: set[str]) -> Mapping[str, Any]:
    value = data.get(key)
    if not isinstance(value, dict):
        raise ConfigurationError(f"{key} must be an object")
    unknown = sorted(set(value) - allowed)
    if unknown:
        raise ConfigurationError(f"unknown {key} field(s): {', '.join(unknown)}")
    return value


def _bool_fields(section: Mapping[str, Any], prefix: str) -> None:
    for key, value in section.items():
        if key.startswith(("allow_", "require_", "reject_", "forbid_")) and not isinstance(
            value, bool
        ):
            raise ConfigurationError(f"{prefix}.{key} must be boolean")


def validate_config(data: Mapping[str, Any]) -> EclipseConfig:
    unknown = sorted(set(data) - _TOP_LEVEL)
    if unknown:
        raise ConfigurationError(f"unknown configuration field(s): {', '.join(unknown)}")
    missing = sorted(_TOP_LEVEL - set(data))
    if missing:
        raise ConfigurationError(f"missing configuration field(s): {', '.join(missing)}")
    if data.get("schema_version") != CONFIG_SCHEMA_VERSION:
        raise ConfigurationError(
            f"unsupported config schema {data.get('schema_version')!r}; "
            f"expected {CONFIG_SCHEMA_VERSION!r}"
        )
    if data.get("profile") not in {"strict", "standard", "fast"}:
        raise ConfigurationError("profile must be strict, standard, or fast")
    if data.get("adapter") not in {"auto", "codex", "copilot", "manual"}:
        raise ConfigurationError("adapter must be auto, codex, copilot, or manual")
    if not isinstance(data.get("policy"), str) or not str(data["policy"]).strip():
        raise ConfigurationError("policy must be a non-empty string")

    routing = _object(
        data,
        "routing",
        {"unverified_route_behavior", "allow_worker_effort_escalation"},
    )
    if routing.get("unverified_route_behavior") not in {"fail", "policy-only", "manual"}:
        raise ConfigurationError("routing.unverified_route_behavior is invalid")
    concurrency = _object(
        data, "concurrency", {"max_parallel_writers", "max_parallel_readers"}
    )
    writers = concurrency.get("max_parallel_writers")
    readers = concurrency.get("max_parallel_readers")
    if not isinstance(writers, int) or isinstance(writers, bool) or not 1 <= writers <= 16:
        raise ConfigurationError("concurrency.max_parallel_writers must be 1..16")
    if not isinstance(readers, int) or isinstance(readers, bool) or not 1 <= readers <= 64:
        raise ConfigurationError("concurrency.max_parallel_readers must be 1..64")
    budgets = _object(data, "budgets", {"max_attempts", "max_review_rounds"})
    for key in ("max_attempts", "max_review_rounds"):
        value = budgets.get(key)
        if not isinstance(value, int) or isinstance(value, bool) or not 0 <= value <= 10:
            raise ConfigurationError(f"budgets.{key} must be 0..10")
    git = _object(
        data,
        "git",
        {"parallel_write_isolation", "require_clean_base", "branch_prefix"},
    )
    if git.get("parallel_write_isolation") not in {"worktree", "branch", "none"}:
        raise ConfigurationError("git.parallel_write_isolation is invalid")
    if not isinstance(git.get("branch_prefix"), str) or not git["branch_prefix"]:
        raise ConfigurationError("git.branch_prefix must be a non-empty string")
    validation = _object(
        data, "validation", {"require_all_criteria_evidence", "reject_stale_results"}
    )
    security = _object(
        data,
        "security",
        {
            "network_default",
            "repository_content_trust",
            "reject_probable_secrets",
            "forbid_run_state_writes",
        },
    )
    if security.get("network_default") not in {"deny", "allow-authorized"}:
        raise ConfigurationError("security.network_default is invalid")
    if security.get("repository_content_trust") not in {"untrusted", "trusted"}:
        raise ConfigurationError("security.repository_content_trust is invalid")
    for prefix, section in (
        ("routing", routing),
        ("git", git),
        ("validation", validation),
        ("security", security),
    ):
        _bool_fields(section, prefix)
    return EclipseConfig(data=dict(data))


def load_config(path: Path) -> EclipseConfig:
    value = load_json(path)
    if not isinstance(value, dict):
        raise ConfigurationError("configuration root must be an object")
    return validate_config(value)


def write_default_config(path: Path) -> None:
    write_json_atomic(path, DEFAULT_CONFIG)
