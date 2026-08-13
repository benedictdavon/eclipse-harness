"""Vendor-neutral routing abstractions and Sol/Luna reference policy."""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping, Protocol, Sequence

from .contracts import TaskContract
from .errors import ConfigurationError

_MODEL = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/-]{0,127}$")
_REASONING = {"none", "low", "medium", "high", "xhigh", "max", "ultra"}


class Role(str, Enum):
    ARCHITECT = "architect"
    EXECUTOR = "executor"
    REVIEWER = "reviewer"
    DOCTOR = "doctor"


class RouteVerification(str, Enum):
    VERIFIED = "verified"
    BROKEN = "broken"
    UNVERIFIED = "unverified"
    UNAVAILABLE = "unavailable"


@dataclass(frozen=True)
class RouteProfile:
    name: str
    role: Role
    capability_tier: str
    cost_tier: str
    reasoning_effort: str
    preferred_model: str | None
    desired_permissions: tuple[str, ...]


@dataclass(frozen=True)
class RouteDecision:
    profile: RouteProfile
    suitability_score: int
    rationale: tuple[str, ...]
    verification: RouteVerification
    mode: str


class RoutingPolicy(Protocol):
    name: str

    def select(
        self,
        task: TaskContract,
        route_status: Mapping[str, RouteVerification],
        *,
        unverified_behavior: str,
    ) -> RouteDecision: ...


def suitability_score(task: TaskContract) -> tuple[int, tuple[str, ...]]:
    score = 0
    rationale: list[str] = []
    criteria = task.data["acceptance_criteria"]
    assert isinstance(criteria, Sequence)
    if criteria:
        score += 2
        rationale.append("acceptance criteria are explicit")
    write_globs = task.scope["write_globs"]
    if len(write_globs) <= 4:
        score += 2
        rationale.append("write set is small")
    decisions = task.data["decisions"]
    assert isinstance(decisions, Mapping)
    if decisions.get("fixed"):
        score += 2
        rationale.append("architecture decisions are fixed")
    if task.data["validation"]:
        score += 1
        rationale.append("task is independently testable")
    if not task.scope["shared_interfaces"]:
        score += 1
        rationale.append("no shared interface change declared")
    authorization = task.data["authorization"]
    assert isinstance(authorization, Mapping)
    if not authorization.get("external_side_effects"):
        score += 1
        rationale.append("no external side effects")
    risk = task.data["risk"]
    assert isinstance(risk, Mapping)
    penalty_flags = {
        "security",
        "migration",
        "persistent-data",
        "concurrency",
        "public-api",
    }
    for flag in sorted(set(risk.get("flags", ())) & penalty_flags):
        score -= 2
        rationale.append(f"risk penalty: {flag}")
    if task.data["complexity"] == "architectural":
        score -= 4
        rationale.append("architectural complexity remains")
    return score, tuple(rationale)


@dataclass(frozen=True)
class Policy:
    name: str
    profiles: Mapping[str, RouteProfile]

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "Policy":
        if data.get("schema_version") != "1.0":
            raise ConfigurationError("unsupported policy schema")
        name = data.get("name")
        if not isinstance(name, str) or not name:
            raise ConfigurationError("policy name is required")
        raw_profiles = data.get("profiles")
        if not isinstance(raw_profiles, dict) or not raw_profiles:
            raise ConfigurationError("policy profiles must be a non-empty object")
        profiles: dict[str, RouteProfile] = {}
        allowed = {
            "role",
            "capability_tier",
            "cost_tier",
            "reasoning_effort",
            "preferred_model",
            "desired_permissions",
        }
        for profile_name, raw in raw_profiles.items():
            if not isinstance(raw, dict):
                raise ConfigurationError(f"profile {profile_name} must be an object")
            unknown = set(raw) - allowed
            if unknown:
                raise ConfigurationError(f"unknown fields in profile {profile_name}: {sorted(unknown)}")
            try:
                role = Role(str(raw["role"]))
                reasoning = raw["reasoning_effort"]
                if not isinstance(reasoning, str) or reasoning not in _REASONING:
                    raise ConfigurationError(
                        f"invalid reasoning effort in profile {profile_name}"
                    )
                model = raw.get("preferred_model")
                if model is not None and (
                    not isinstance(model, str) or not _MODEL.fullmatch(model)
                ):
                    raise ConfigurationError(f"invalid model id in profile {profile_name}")
                profiles[str(profile_name)] = RouteProfile(
                    name=str(profile_name),
                    role=role,
                    capability_tier=str(raw["capability_tier"]),
                    cost_tier=str(raw["cost_tier"]),
                    reasoning_effort=reasoning,
                    preferred_model=model,
                    desired_permissions=tuple(str(item) for item in raw["desired_permissions"]),
                )
            except (KeyError, TypeError, ValueError) as error:
                raise ConfigurationError(f"invalid route profile {profile_name}: {error}") from error
        return cls(name=name, profiles=profiles)

    def select(
        self,
        task: TaskContract,
        route_status: Mapping[str, RouteVerification],
        *,
        unverified_behavior: str,
    ) -> RouteDecision:
        score, rationale = suitability_score(task)
        if score <= 2 or task.data["complexity"] == "architectural":
            profile_name = "architect"
        elif task.data["complexity"] == "trivial" and score >= 6:
            profile_name = "worker-lite"
        else:
            profile_name = "worker"
        if profile_name not in self.profiles:
            raise ConfigurationError(f"policy lacks required profile {profile_name!r}")
        profile = self.profiles[profile_name]
        verification = route_status.get(profile_name, RouteVerification.UNVERIFIED)
        mode = "native-verified" if verification is RouteVerification.VERIFIED else "policy-only"
        if verification is RouteVerification.BROKEN:
            mode = "explicit-worker-fallback"
        if verification in {RouteVerification.UNVERIFIED, RouteVerification.UNAVAILABLE}:
            if unverified_behavior == "fail":
                raise ConfigurationError(f"route {profile_name} is not verified")
            if unverified_behavior == "manual":
                mode = "manual"
        return RouteDecision(profile, score, rationale, verification, mode)


_ARCHITECT_CODES = {"SPEC_AMBIGUOUS", "SCOPE_EXPANSION", "ARCH_DECISION", "SECURITY_DECISION"}
_HUMAN_CODES = {"AUTH_REQUIRED", "DESTRUCTIVE_ACTION"}
_WORKER_CODES = {"LOCAL_REASONING", "VALIDATION_FAILURE"}
_ENVIRONMENT_CODES = {"CTX_MISSING", "ENV_FAILURE"}


def escalation_route(code: str) -> str:
    if code in _ARCHITECT_CODES:
        return "architect"
    if code in _HUMAN_CODES:
        return "human"
    if code in _WORKER_CODES:
        return "higher-worker-effort"
    if code in _ENVIRONMENT_CODES:
        return "repair-context-or-environment"
    if code == "BUDGET_EXHAUSTED":
        return "architect"
    raise ValueError(f"unknown escalation code: {code}")
