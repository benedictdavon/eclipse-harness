"""Non-destructive, host-specific adapter, permission, and route diagnostics."""

from __future__ import annotations

import os
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Mapping

from . import __version__
from .constants import CAPABILITY_SCHEMA_VERSION
from .jsonutil import load_json, read_text_bounded, write_json_atomic
from .process import run_bounded
from .routing import Policy
from .tomlutil import load_toml


@dataclass(frozen=True)
class Diagnostic:
    check: str
    level: str
    message: str

    def to_dict(self) -> dict[str, str]:
        return {"check": self.check, "level": self.level, "message": self.message}


@dataclass(frozen=True)
class CapabilitySnapshot:
    host: Mapping[str, Any]
    skills: Mapping[str, Any]
    agents: Mapping[str, Any]
    concurrency: Mapping[str, Any]
    permissions: Mapping[str, Any]
    git: Mapping[str, Any]
    routes: Mapping[str, Any]
    diagnostics: tuple[Diagnostic, ...]

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": CAPABILITY_SCHEMA_VERSION,
            "eclipse_version": __version__,
            "host": dict(self.host),
            "skills": dict(self.skills),
            "agents": dict(self.agents),
            "concurrency": dict(self.concurrency),
            "permissions": dict(self.permissions),
            "git": dict(self.git),
            "routes": dict(self.routes),
            "diagnostics": [item.to_dict() for item in self.diagnostics],
        }

    @property
    def healthy(self) -> bool:
        return not any(item.level == "error" for item in self.diagnostics)


def _version(command: str, repository_root: Path) -> tuple[bool, str | None]:
    executable = shutil.which(command)
    if executable is None:
        return False, None
    resolved = Path(executable).resolve()
    try:
        resolved.relative_to(repository_root)
    except ValueError:
        pass
    else:
        return False, None
    for arguments in ((executable, "--version"), (executable, "version")):
        try:
            completed = run_bounded(arguments, timeout=10, output_limit=4096)
        except subprocess.TimeoutExpired:
            continue
        if completed.returncode == 0:
            output = (completed.stdout + completed.stderr).strip()
            return True, output.splitlines()[0][:200] if output else "version unavailable"
    return True, "installed; version unavailable"


def _read_toml(path: Path) -> Mapping[str, Any] | None:
    if not path.is_file() or path.stat().st_size > 1024 * 1024:
        return None
    try:
        with path.open("rb") as handle:
            return load_toml(handle)
    except (OSError, ValueError):
        return None


def _load_observations(path: Path | None) -> Mapping[str, Any]:
    if path is None:
        return {}
    value = load_json(path)
    return value if isinstance(value, dict) else {}


def run_doctor(
    repository_root: Path,
    policy: Policy,
    *,
    observation_file: Path | None = None,
    trust_observations: bool = False,
) -> CapabilitySnapshot:
    root = repository_root.resolve()
    diagnostics: list[Diagnostic] = []
    codex_present, codex_version = _version("codex", root)
    copilot_present, copilot_version = _version("copilot", root)
    surface_hint = os.environ.get("ECLIPSE_HOST")
    if surface_hint in {"codex-cli", "codex-app", "copilot-cli", "copilot-cloud", "manual"}:
        host_name = surface_hint
    elif codex_present:
        host_name = "codex-cli"
    elif copilot_present:
        host_name = "copilot-cli"
    else:
        host_name = "manual"
    host = {
        "name": host_name,
        "codex": {"installed": codex_present, "version": codex_version},
        "copilot": {"installed": copilot_present, "version": copilot_version},
    }
    diagnostics.append(
        Diagnostic(
            "host",
            "warning" if host_name == "manual" else "pass",
            "manual protocol mode" if host_name == "manual" else f"detected {host_name}",
        )
    )

    skill_names = (
        "eclipse-orchestrate",
        "eclipse-execute",
        "eclipse-review",
        "eclipse-bootstrap",
        "eclipse-doctor",
    )
    missing_skills = [
        name
        for name in skill_names
        if not (root / ".agents" / "skills" / name / "SKILL.md").is_file()
    ]
    skills = {
        "project_path": ".agents/skills",
        "configured": not missing_skills,
        "missing": missing_skills,
        "effective": "unverified" if host_name == "manual" else "discoverable",
        "python_required": False,
    }
    diagnostics.append(
        Diagnostic(
            "skills",
            "error" if missing_skills else "pass",
            "missing: " + ", ".join(missing_skills)
            if missing_skills
            else "all Eclipse skills present",
        )
    )

    codex_config = _read_toml(root / ".codex" / "config.toml")
    codex_agents = {
        name: _read_toml(root / ".codex" / "agents" / f"eclipse_{name}.toml")
        for name in ("architect", "worker", "escalation_worker", "reviewer")
    }
    copilot_agent_text = {
        name: _read_optional_text(root / ".github" / "agents" / f"eclipse-{name}.agent.md")
        for name in ("architect", "worker", "reviewer")
    }
    configured_codex = codex_config is not None and all(
        value is not None for value in codex_agents.values()
    )
    configured_copilot = all(value is not None for value in copilot_agent_text.values())
    codex_recursion = _recursion_status(codex_agents)
    agents = {
        "active_host": host_name,
        "codex": {
            "configured": configured_codex,
            "native_spawn_effective": "unverified",
            "worker_recursion": codex_recursion,
        },
        "copilot": {
            "configured": configured_copilot,
            "native_spawn_effective": "unverified",
            "worker_recursion": "instruction-only" if configured_copilot else "unavailable",
        },
    }
    for adapter, configured in (("codex", configured_codex), ("copilot", configured_copilot)):
        diagnostics.append(
            Diagnostic(
                f"agents:{adapter}",
                "pass" if configured else "warning",
                f"{adapter} profiles configured" if configured else f"{adapter} profiles absent",
            )
        )
    if configured_codex and codex_recursion != "configured-disabled":
        diagnostics.append(
            Diagnostic(
                "worker-recursion:codex",
                "warning",
                "Codex worker non-recursion is not mechanically configured",
            )
        )

    concurrency_value: Any = None
    if codex_config and isinstance(codex_config.get("agents"), dict):
        concurrency_value = codex_config["agents"].get(
            "max_concurrent_threads_per_session"
        )
        if "max_threads" in codex_config["agents"]:
            diagnostics.append(
                Diagnostic("concurrency:codex", "warning", "legacy max_threads field is configured")
            )
    concurrency = {
        "codex": {"requested": concurrency_value, "effective": "unverified"},
        "copilot": {"requested": None, "effective": "unverified"},
        "execution_waves": "host-scheduled; optional Eclipse validation only",
    }

    codex_reviewer = codex_agents.get("reviewer") or {}
    codex_worker = codex_agents.get("worker") or {}
    codex_reviewer_sandbox = codex_reviewer.get("sandbox_mode")
    codex_worker_sandbox = codex_worker.get("sandbox_mode")
    copilot_reviewer = copilot_agent_text.get("reviewer") or ""
    copilot_worker = copilot_agent_text.get("worker") or ""
    copilot_read_only_intent = 'tools: ["read", "search"]' in copilot_reviewer
    copilot_write_intent = all(
        tool in copilot_worker for tool in ('"edit"', '"execute"')
    )
    permissions = {
        "codex": {
            "reviewer": {
                "desired": "read-only",
                "configured": codex_reviewer_sandbox,
                "effective": "unverified",
                "enforcement": "host-conditional",
            },
            "worker": {
                "desired": "scoped-write",
                "configured": codex_worker_sandbox,
                "effective": "unverified",
                "enforcement": "host-conditional",
            },
        },
        "copilot": {
            "reviewer": {
                "desired": "read-only",
                "configured": "read/search only" if copilot_read_only_intent else None,
                "effective": "unverified",
                "enforcement": "surface-dependent",
            },
            "worker": {
                "desired": "scoped-write",
                "configured": "edit/execute tools" if copilot_write_intent else None,
                "effective": "unverified",
                "enforcement": "surface-dependent",
            },
        },
    }
    _permission_diagnostic(
        diagnostics,
        host="codex",
        configured=configured_codex,
        reviewer_ok=codex_reviewer_sandbox == "read-only",
    )
    _permission_diagnostic(
        diagnostics,
        host="copilot",
        configured=configured_copilot,
        reviewer_ok=copilot_read_only_intent,
    )

    git_present, git_version = _version("git", root)
    git = {
        "installed": git_present,
        "version": git_version,
        "ownership": "host",
    }
    diagnostics.append(
        Diagnostic(
            "git",
            "pass" if git_present else "warning",
            "git available to host" if git_present else "git unavailable; host/manual workflow decides",
        )
    )

    observations = _load_observations(observation_file)
    if observation_file is not None and not trust_observations:
        diagnostics.append(
            Diagnostic(
                "observations",
                "warning",
                "observation file is untrusted; pass --trust-observations only after host verification",
            )
        )
    observed_routes = observations.get("routes", {}) if isinstance(observations, dict) else {}
    routes: dict[str, Any] = {}
    for name, profile in policy.profiles.items():
        codex_model = _configured_model(name, codex_agents)
        configured_by_host = {"codex": codex_model, "copilot": None}
        active_configured = (
            codex_model if host_name in {"codex-cli", "codex-app"} else None
        )
        if profile.preferred_model is None:
            routes[name] = {
                "requested_model": None,
                "configured_model": active_configured,
                "configured_by_host": configured_by_host,
                "effective_model": None,
                "verification": "unavailable",
                "status": "unavailable",
            }
            continue
        observation = observed_routes.get(name, {}) if isinstance(observed_routes, dict) else {}
        effective_model = observation.get("effective_model") if isinstance(observation, dict) else None
        source = observation.get("source") if isinstance(observation, dict) else None
        verified = (
            trust_observations
            and source == "host-observed"
            and isinstance(effective_model, str)
        )
        requested = profile.preferred_model
        status = "unverified"
        if verified:
            status = "verified" if effective_model == requested else "broken"
        routes[name] = {
            "requested_model": requested,
            "configured_model": active_configured,
            "configured_by_host": configured_by_host,
            "effective_model": effective_model if verified else None,
            "verification": "host-observed" if verified else "unverified",
            "status": status,
        }
        if status == "broken":
            diagnostics.append(
                Diagnostic(
                    f"route:{name}",
                    "error",
                    f"requested {requested}, observed {effective_model}; native cost routing is unsafe",
                )
            )
        elif status == "unverified":
            diagnostics.append(
                Diagnostic(
                    f"route:{name}",
                    "warning",
                    f"requested {requested}; effective model is unverified",
                )
            )
    return CapabilitySnapshot(
        host=host,
        skills=skills,
        agents=agents,
        concurrency=concurrency,
        permissions=permissions,
        git=git,
        routes=routes,
        diagnostics=tuple(diagnostics),
    )


def write_snapshot(path: Path, snapshot: CapabilitySnapshot) -> None:
    write_json_atomic(path, snapshot.to_dict())


def _read_optional_text(path: Path) -> str | None:
    return read_text_bounded(path) if path.is_file() else None


def _permission_diagnostic(
    diagnostics: list[Diagnostic],
    *,
    host: str,
    configured: bool,
    reviewer_ok: bool,
) -> None:
    if not configured:
        diagnostics.append(
            Diagnostic(
                f"reviewer-permissions:{host}",
                "warning",
                f"{host} reviewer profile is not configured",
            )
        )
    elif reviewer_ok:
        diagnostics.append(
            Diagnostic(
                f"reviewer-permissions:{host}",
                "pass",
                f"{host} reviewer requests read-only access",
            )
        )
    else:
        diagnostics.append(
            Diagnostic(
                f"reviewer-permissions:{host}",
                "error",
                f"{host} reviewer does not request read-only access",
            )
        )


def _recursion_status(agents: Mapping[str, Mapping[str, Any] | None]) -> str:
    workers = (agents.get("worker"), agents.get("escalation_worker"))
    if all(
        isinstance(item, dict)
        and isinstance(item.get("agents"), dict)
        and item["agents"].get("enabled") is False
        for item in workers
    ):
        return "configured-disabled"
    return "unverified"


def _configured_model(
    profile_name: str, agents: Mapping[str, Mapping[str, Any] | None]
) -> str | None:
    codex_name = profile_name.replace("-", "_")
    key = "escalation_worker" if codex_name == "escalation_worker" else codex_name
    data = agents.get(key)
    value = data.get("model") if isinstance(data, dict) else None
    return value if isinstance(value, str) else None
