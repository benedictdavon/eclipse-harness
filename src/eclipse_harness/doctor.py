"""Non-destructive host, adapter, permission, and route diagnostics."""

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


def _version(command: str, repository_root: Path) -> tuple[bool, str | None, str | None]:
    executable = shutil.which(command)
    if executable is None:
        return False, None, None
    resolved = Path(executable).resolve()
    try:
        resolved.relative_to(repository_root)
    except ValueError:
        pass
    else:
        return False, None, None
    for arguments in ((executable, "--version"), (executable, "version")):
        try:
            completed = run_bounded(arguments, timeout=10, output_limit=4096)
        except subprocess.TimeoutExpired:
            continue
        if completed.returncode == 0:
            output = (completed.stdout + completed.stderr).strip()
            version = output.splitlines()[0][:200] if output else "version unavailable"
            return True, version, str(resolved)
    return True, "installed; version unavailable", str(resolved)


def _read_toml(path: Path) -> Mapping[str, Any] | None:
    if not path.is_file():
        return None
    if path.stat().st_size > 1024 * 1024:
        return None
    try:
        with path.open("rb") as handle:
            value = load_toml(handle)
        return value
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
    codex_present, codex_version, _ = _version("codex", root)
    copilot_present, copilot_version, _ = _version("copilot", root)
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
    if host_name == "manual":
        diagnostics.append(
            Diagnostic("host", "warning", "no supported CLI detected; manual protocol mode remains usable")
        )
    else:
        diagnostics.append(Diagnostic("host", "pass", f"detected {host_name}"))

    skill_names = ("eclipse-orchestrate", "eclipse-execute", "eclipse-review", "eclipse-doctor")
    missing_skills = [
        name for name in skill_names if not (root / ".agents" / "skills" / name / "SKILL.md").is_file()
    ]
    skills = {
        "supported": host_name != "manual" or True,
        "project_path": ".agents/skills",
        "configured": not missing_skills,
        "missing": missing_skills,
        "effective": "unverified" if host_name == "manual" else "discoverable",
    }
    diagnostics.append(
        Diagnostic(
            "skills",
            "error" if missing_skills else "pass",
            "missing: " + ", ".join(missing_skills) if missing_skills else "all four skills present",
        )
    )

    codex_config = _read_toml(root / ".codex" / "config.toml")
    codex_agents = {
        name: _read_toml(root / ".codex" / "agents" / f"eclipse_{name}.toml")
        for name in ("architect", "worker", "escalation_worker", "reviewer")
    }
    copilot_agents = {
        name: (root / ".github" / "agents" / f"eclipse-{name}.agent.md").is_file()
        for name in ("architect", "worker", "reviewer")
    }
    configured_codex = codex_config is not None and all(value is not None for value in codex_agents.values())
    configured_copilot = all(copilot_agents.values())
    agents = {
        "supported": host_name != "manual",
        "codex_configured": configured_codex,
        "copilot_configured": configured_copilot,
        "native_spawn_effective": "unverified",
        "worker_recursion": _recursion_status(codex_agents),
    }
    diagnostics.append(
        Diagnostic(
            "agents",
            "pass" if configured_codex or configured_copilot else "warning",
            "host agent profiles found" if configured_codex or configured_copilot else "no native profiles installed",
        )
    )
    if agents["worker_recursion"] != "configured-disabled":
        diagnostics.append(
            Diagnostic(
                "worker-recursion",
                "warning",
                "non-recursion is not mechanically configured or cannot be verified",
            )
        )

    concurrency_value: Any = None
    if codex_config and isinstance(codex_config.get("agents"), dict):
        concurrency_value = codex_config["agents"].get("max_concurrent_threads_per_session")
        if "max_threads" in codex_config["agents"]:
            diagnostics.append(
                Diagnostic("concurrency", "warning", "legacy max_threads field is configured")
            )
    concurrency = {
        "requested": concurrency_value,
        "effective": "unverified",
        "write_safety_enforced_by": "eclipse contract validator",
    }

    reviewer_codex = codex_agents.get("reviewer") or {}
    reviewer_sandbox = reviewer_codex.get("sandbox_mode")
    reviewer_copilot_path = root / ".github" / "agents" / "eclipse-reviewer.agent.md"
    reviewer_copilot = (
        read_text_bounded(reviewer_copilot_path) if reviewer_copilot_path.is_file() else ""
    )
    copilot_read_only_intent = "tools: [\"read\", \"search\"]" in reviewer_copilot
    permissions = {
        "reviewer": {
            "desired": "read-only",
            "configured": reviewer_sandbox or ("read/search only" if copilot_read_only_intent else None),
            "effective": "unverified",
            "enforcement": "host-conditional",
        },
        "worker": {
            "desired": "scoped-write",
            "configured": "workspace-write" if configured_codex else "tool-profile",
            "effective": "unverified",
            "enforcement": "contract validator plus host controls",
        },
    }
    if reviewer_sandbox != "read-only" and not copilot_read_only_intent:
        diagnostics.append(
            Diagnostic("reviewer-permissions", "error", "read-only reviewer intent is not configured")
        )

    git_present, git_version, git_executable = _version("git", root)
    worktrees = False
    if git_present and (root / ".git").exists():
        assert git_executable is not None
        try:
            completed = subprocess.run(
                (git_executable, "worktree", "list", "--porcelain"),
                cwd=root,
                text=True,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL,
                check=False,
                timeout=30,
            )
            worktrees = completed.returncode == 0
        except subprocess.TimeoutExpired:
            diagnostics.append(Diagnostic("git", "warning", "git worktree probe timed out"))
    git = {"installed": git_present, "version": git_version, "worktrees": worktrees}
    diagnostics.append(
        Diagnostic("git", "pass" if worktrees else "warning", "worktrees available" if worktrees else "worktrees unavailable")
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
        if profile.preferred_model is None:
            routes[name] = {
                "requested_model": None,
                "configured_model": None,
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
            "configured_model": _configured_model(name, codex_agents),
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
    if codex_name == "escalation_worker":
        key = "escalation_worker"
    elif codex_name in agents:
        key = codex_name
    else:
        return None
    data = agents.get(key)
    value = data.get("model") if isinstance(data, dict) else None
    return value if isinstance(value, str) else None
