"""Typed, strict task, result, and review contracts."""

from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from typing import Any, Iterable, Mapping, Sequence

from .authorization import authorize_changed_files
from .constants import CONTRACT_SCHEMA_VERSION
from .errors import AuthorizationError, ContractValidationError, ValidationIssue
from .jsonutil import digest_json
from .security import assess_command
from .usage import UsageRecord

_ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]{0,127}$")


class ResultStatus(str, Enum):
    COMPLETE = "complete"
    BLOCKED = "blocked"
    FAILED = "failed"
    ESCALATED = "escalated"


class ReviewOutcome(str, Enum):
    ACCEPTED = "accepted"
    CHANGES_REQUESTED = "changes_requested"
    ESCALATED = "escalated"
    REJECTED = "rejected"


class _Validator:
    def __init__(self) -> None:
        self.issues: list[ValidationIssue] = []

    def issue(self, path: str, message: str, code: str = "invalid") -> None:
        self.issues.append(ValidationIssue(path, message, code))

    def object(
        self,
        value: Any,
        path: str,
        required: Iterable[str],
        allowed: Iterable[str],
    ) -> Mapping[str, Any]:
        if not isinstance(value, dict):
            self.issue(path, "must be an object", "type")
            return {}
        required_set, allowed_set = set(required), set(allowed)
        for key in sorted(required_set - set(value)):
            self.issue(f"{path}.{key}", "is required", "required")
        for key in sorted(set(value) - allowed_set):
            self.issue(f"{path}.{key}", "is not allowed", "unknown")
        return value

    def string(self, value: Any, path: str, *, nonempty: bool = True) -> None:
        if not isinstance(value, str):
            self.issue(path, "must be a string", "type")
        elif nonempty and not value.strip():
            self.issue(path, "must not be empty", "empty")

    def strings(self, value: Any, path: str, *, nonempty: bool = False) -> None:
        if not isinstance(value, list):
            self.issue(path, "must be an array", "type")
            return
        if nonempty and not value:
            self.issue(path, "must not be empty", "empty")
        for index, item in enumerate(value):
            self.string(item, f"{path}[{index}]")

    def identifier(self, value: Any, path: str) -> None:
        self.string(value, path)
        if isinstance(value, str) and not _ID.fullmatch(value):
            self.issue(path, "must match the portable identifier format", "format")

    def positive_int(self, value: Any, path: str) -> None:
        if not isinstance(value, int) or isinstance(value, bool) or value < 1:
            self.issue(path, "must be a positive integer", "range")

    def finish(self) -> None:
        if self.issues:
            raise ContractValidationError(self.issues)


TASK_FIELDS = {
    "schema_version",
    "run_id",
    "plan_revision",
    "plan_digest",
    "task_id",
    "parent_task_id",
    "dependencies",
    "objective",
    "rationale",
    "context_manifest",
    "decisions",
    "invariants",
    "non_goals",
    "scope",
    "required_capabilities",
    "execution_profile",
    "implementation_instructions",
    "acceptance_criteria",
    "validation",
    "expected_evidence",
    "stop_conditions",
    "risk",
    "complexity",
    "budgets",
    "authorization",
    "provenance",
    "metadata",
}
TASK_REQUIRED = TASK_FIELDS - {"parent_task_id", "metadata"}


def _validate_context(v: _Validator, value: Any, path: str = "$.context_manifest") -> None:
    context = v.object(
        value,
        path,
        {"schema_version", "summary", "references", "trusted_sources"},
        {"schema_version", "summary", "references", "trusted_sources"},
    )
    if context.get("schema_version") != CONTRACT_SCHEMA_VERSION:
        v.issue(
            f"{path}.schema_version",
            f"must equal {CONTRACT_SCHEMA_VERSION!r}",
            "version",
        )
    v.string(context.get("summary"), f"{path}.summary", nonempty=False)
    references = context.get("references")
    if not isinstance(references, list):
        v.issue(f"{path}.references", "must be an array", "type")
    else:
        for index, reference in enumerate(references):
            ref = v.object(
                reference,
                f"{path}.references[{index}]",
                {"path", "purpose", "trust"},
                {"path", "symbol", "purpose", "digest", "trust"},
            )
            v.string(ref.get("path"), f"{path}.references[{index}].path")
            v.string(ref.get("purpose"), f"{path}.references[{index}].purpose")
            if ref.get("trust") not in {
                "user",
                "harness",
                "project-config",
                "repository",
                "external",
            }:
                v.issue(
                    f"{path}.references[{index}].trust",
                    "has an invalid trust class",
                    "enum",
                )
    v.strings(context.get("trusted_sources"), f"{path}.trusted_sources")


def validate_context_manifest_data(data: Mapping[str, Any]) -> None:
    """Validate a standalone context manifest without requiring Python at runtime."""

    v = _Validator()
    _validate_context(v, data, "$")
    v.finish()


def _validate_scope(v: _Validator, value: Any) -> None:
    fields = {
        "write_globs",
        "read_globs",
        "forbidden_globs",
        "shared_interfaces",
        "exclusive_resources",
        "parallel_safe",
        "isolation",
    }
    scope = v.object(value, "$.scope", fields, fields)
    v.strings(scope.get("write_globs"), "$.scope.write_globs", nonempty=True)
    for field in ("read_globs", "forbidden_globs", "shared_interfaces", "exclusive_resources"):
        v.strings(scope.get(field), f"$.scope.{field}")
    if not isinstance(scope.get("parallel_safe"), bool):
        v.issue("$.scope.parallel_safe", "must be boolean", "type")
    if scope.get("isolation") not in {"shared-readonly", "branch", "worktree", "manual"}:
        v.issue("$.scope.isolation", "has an invalid isolation strategy", "enum")


def _validate_criteria(v: _Validator, value: Any) -> None:
    if not isinstance(value, list) or not value:
        v.issue("$.acceptance_criteria", "must be a non-empty array", "empty")
        return
    seen: set[str] = set()
    fields = {"id", "statement", "evidence_required"}
    for index, criterion in enumerate(value):
        item = v.object(criterion, f"$.acceptance_criteria[{index}]", fields, fields)
        criterion_id = item.get("id")
        v.identifier(criterion_id, f"$.acceptance_criteria[{index}].id")
        if isinstance(criterion_id, str) and criterion_id in seen:
            v.issue(f"$.acceptance_criteria[{index}].id", "must be unique", "duplicate")
        if isinstance(criterion_id, str):
            seen.add(criterion_id)
        v.string(item.get("statement"), f"$.acceptance_criteria[{index}].statement")
        v.string(item.get("evidence_required"), f"$.acceptance_criteria[{index}].evidence_required")


def _validate_commands(v: _Validator, value: Any, path: str = "$.validation") -> None:
    if not isinstance(value, list):
        v.issue(path, "must be an array", "type")
        return
    fields = {"command", "purpose", "mutating", "required"}
    for index, command in enumerate(value):
        item = v.object(command, f"{path}[{index}]", fields, fields)
        v.string(item.get("command"), f"{path}[{index}].command")
        v.string(item.get("purpose"), f"{path}[{index}].purpose")
        for field in ("mutating", "required"):
            if not isinstance(item.get(field), bool):
                v.issue(f"{path}[{index}].{field}", "must be boolean", "type")


def validate_task_data(data: Mapping[str, Any]) -> None:
    v = _Validator()
    v.object(data, "$", TASK_REQUIRED, TASK_FIELDS)
    if data.get("schema_version") != CONTRACT_SCHEMA_VERSION:
        v.issue("$.schema_version", f"must equal {CONTRACT_SCHEMA_VERSION!r}", "version")
    for field in ("run_id", "task_id"):
        v.identifier(data.get(field), f"$.{field}")
    v.positive_int(data.get("plan_revision"), "$.plan_revision")
    v.string(data.get("plan_digest"), "$.plan_digest")
    if data.get("parent_task_id") is not None:
        v.identifier(data.get("parent_task_id"), "$.parent_task_id")
    v.strings(data.get("dependencies"), "$.dependencies")
    v.string(data.get("objective"), "$.objective")
    v.string(data.get("rationale"), "$.rationale", nonempty=False)
    _validate_context(v, data.get("context_manifest"))

    decisions = v.object(
        data.get("decisions"),
        "$.decisions",
        {"fixed", "assumptions"},
        {"fixed", "assumptions"},
    )
    v.strings(decisions.get("fixed"), "$.decisions.fixed")
    v.strings(decisions.get("assumptions"), "$.decisions.assumptions")
    for field in ("invariants", "non_goals", "required_capabilities", "implementation_instructions"):
        v.strings(data.get(field), f"$.{field}")
    _validate_scope(v, data.get("scope"))

    profile_fields = {
        "role",
        "capability_tier",
        "cost_tier",
        "reasoning_effort",
        "preferred_model",
        "fallback_profiles",
    }
    profile = v.object(
        data.get("execution_profile"),
        "$.execution_profile",
        profile_fields - {"preferred_model"},
        profile_fields,
    )
    for field in ("role", "capability_tier", "cost_tier", "reasoning_effort"):
        v.string(profile.get(field), f"$.execution_profile.{field}")
    if profile.get("preferred_model") is not None:
        v.string(profile.get("preferred_model"), "$.execution_profile.preferred_model")
    v.strings(profile.get("fallback_profiles"), "$.execution_profile.fallback_profiles")
    _validate_criteria(v, data.get("acceptance_criteria"))
    _validate_commands(v, data.get("validation"))
    v.strings(data.get("expected_evidence"), "$.expected_evidence", nonempty=True)
    v.strings(data.get("stop_conditions"), "$.stop_conditions", nonempty=True)

    risk = v.object(data.get("risk"), "$.risk", {"level", "flags"}, {"level", "flags"})
    if risk.get("level") not in {"low", "medium", "high", "critical"}:
        v.issue("$.risk.level", "has an invalid risk level", "enum")
    v.strings(risk.get("flags"), "$.risk.flags")
    if data.get("complexity") not in {"trivial", "bounded", "complex", "architectural"}:
        v.issue("$.complexity", "has an invalid complexity class", "enum")

    budgets = v.object(
        data.get("budgets"),
        "$.budgets",
        {"max_attempts", "max_review_rounds"},
        {"max_attempts", "max_review_rounds"},
    )
    for field in ("max_attempts", "max_review_rounds"):
        value = budgets.get(field)
        if not isinstance(value, int) or isinstance(value, bool) or not 0 <= value <= 10:
            v.issue(f"$.budgets.{field}", "must be an integer from 0 to 10", "range")

    auth_fields = {
        "network",
        "credentials",
        "external_side_effects",
        "destructive_actions",
        "targets",
    }
    authorization = v.object(data.get("authorization"), "$.authorization", auth_fields, auth_fields)
    for field in ("network", "credentials", "external_side_effects", "destructive_actions"):
        if not isinstance(authorization.get(field), bool):
            v.issue(f"$.authorization.{field}", "must be boolean", "type")
    v.strings(authorization.get("targets"), "$.authorization.targets")
    commands = data.get("validation")
    if isinstance(commands, list):
        for index, command in enumerate(commands):
            if not isinstance(command, dict) or not isinstance(command.get("command"), str):
                continue
            assessment = assess_command(
                command["command"],
                network_authorized=authorization.get("network") is True,
                destructive_authorized=authorization.get("destructive_actions") is True,
            )
            for reason in assessment.reasons:
                v.issue(f"$.validation[{index}].command", reason, "unauthorized-command")

    provenance = v.object(
        data.get("provenance"),
        "$.provenance",
        {"base_revision", "created_by", "created_at"},
        {"base_revision", "created_by", "created_at", "source_requirement_digest"},
    )
    for field in ("base_revision", "created_by", "created_at"):
        v.string(provenance.get(field), f"$.provenance.{field}")
    base_revision = provenance.get("base_revision")
    if isinstance(base_revision, str) and not re.fullmatch(r"[0-9a-fA-F]{40,64}", base_revision):
        v.issue("$.provenance.base_revision", "must be a full hexadecimal Git object id", "format")
    if data.get("metadata") is not None and not isinstance(data.get("metadata"), dict):
        v.issue("$.metadata", "must be an object", "type")
    v.finish()


RESULT_FIELDS = {
    "schema_version",
    "run_id",
    "plan_revision",
    "plan_digest",
    "task_id",
    "task_contract_digest",
    "attempt",
    "status",
    "worker_identity",
    "files_changed",
    "implementation_summary",
    "decisions",
    "commands",
    "criteria_evidence",
    "unresolved_issues",
    "blockers",
    "deviations",
    "observed_risks",
    "requested_escalation",
    "git",
    "usage",
    "started_at",
    "finished_at",
    "metadata",
}
RESULT_REQUIRED = RESULT_FIELDS - {"metadata"}


def _validate_identity(v: _Validator, value: Any, path: str, *, reviewer: bool = False) -> None:
    required = {"role", "requested_model", "effective_model", "verification"}
    allowed = set(required)
    if not reviewer:
        required.add("configured_model")
        allowed.add("configured_model")
    identity = v.object(value, path, required, allowed)
    expected_role = "reviewer" if reviewer else "executor"
    if identity.get("role") != expected_role:
        v.issue(f"{path}.role", f"must equal {expected_role!r}", "invariant")
    for field in ("requested_model", "configured_model", "effective_model"):
        if field in allowed and identity.get(field) is not None:
            v.string(identity.get(field), f"{path}.{field}")
    if identity.get("verification") not in {"host-observed", "unverified", "unavailable"}:
        v.issue(f"{path}.verification", "has an invalid verification state", "enum")
    if identity.get("verification") == "host-observed":
        v.issue(
            f"{path}.verification",
            "host attestation must arrive through a trusted envelope, not worker/reviewer JSON",
            "unsupported-claim",
        )
    if identity.get("verification") != "host-observed" and identity.get("effective_model") is not None:
        v.issue(
            f"{path}.effective_model",
            "must be null unless verification is host-observed",
            "unsupported-claim",
        )


def _validate_command_evidence(v: _Validator, value: Any) -> None:
    if not isinstance(value, list):
        v.issue("$.commands", "must be an array", "type")
        return
    required = {"command", "purpose", "exit_code", "outcome", "summary"}
    allowed = required | {"duration_ms"}
    for index, command in enumerate(value):
        item = v.object(command, f"$.commands[{index}]", required, allowed)
        for field in ("command", "purpose", "summary"):
            v.string(item.get(field), f"$.commands[{index}].{field}", nonempty=field != "summary")
        exit_code = item.get("exit_code")
        outcome = item.get("outcome")
        if exit_code is not None and (
            not isinstance(exit_code, int) or isinstance(exit_code, bool)
        ):
            v.issue(f"$.commands[{index}].exit_code", "must be integer or null", "type")
        if outcome not in {"passed", "failed", "not-run"}:
            v.issue(f"$.commands[{index}].outcome", "has an invalid outcome", "enum")
        elif outcome == "passed" and exit_code != 0:
            v.issue(
                f"$.commands[{index}]",
                "passed command evidence requires exit_code 0",
                "inconsistent-command-evidence",
            )
        elif outcome == "failed" and (
            not isinstance(exit_code, int) or isinstance(exit_code, bool) or exit_code == 0
        ):
            v.issue(
                f"$.commands[{index}]",
                "failed command evidence requires a non-zero exit_code",
                "inconsistent-command-evidence",
            )
        elif outcome == "not-run" and exit_code is not None:
            v.issue(
                f"$.commands[{index}]",
                "not-run command evidence requires a null exit_code",
                "inconsistent-command-evidence",
            )


def _validate_criterion_evidence(v: _Validator, value: Any) -> None:
    if not isinstance(value, list):
        v.issue("$.criteria_evidence", "must be an array", "type")
        return
    fields = {"criterion_id", "status", "evidence"}
    seen: set[str] = set()
    for index, record in enumerate(value):
        item = v.object(record, f"$.criteria_evidence[{index}]", fields, fields)
        criterion_id = item.get("criterion_id")
        v.identifier(criterion_id, f"$.criteria_evidence[{index}].criterion_id")
        if isinstance(criterion_id, str) and criterion_id in seen:
            v.issue(f"$.criteria_evidence[{index}].criterion_id", "must be unique", "duplicate")
        if isinstance(criterion_id, str):
            seen.add(criterion_id)
        if item.get("status") not in {"satisfied", "unsatisfied", "not-tested"}:
            v.issue(f"$.criteria_evidence[{index}].status", "has invalid status", "enum")
        v.string(item.get("evidence"), f"$.criteria_evidence[{index}].evidence")


def validate_result_data(data: Mapping[str, Any]) -> None:
    v = _Validator()
    v.object(data, "$", RESULT_REQUIRED, RESULT_FIELDS)
    if data.get("schema_version") != CONTRACT_SCHEMA_VERSION:
        v.issue("$.schema_version", f"must equal {CONTRACT_SCHEMA_VERSION!r}", "version")
    for field in ("run_id", "task_id"):
        v.identifier(data.get(field), f"$.{field}")
    for field in ("plan_digest", "task_contract_digest", "implementation_summary"):
        v.string(data.get(field), f"$.{field}")
    for field in ("plan_revision", "attempt"):
        v.positive_int(data.get(field), f"$.{field}")
    if data.get("status") not in {status.value for status in ResultStatus}:
        v.issue("$.status", "has an invalid result status", "enum")
    _validate_identity(v, data.get("worker_identity"), "$.worker_identity")
    for field in (
        "files_changed",
        "decisions",
        "unresolved_issues",
        "blockers",
        "deviations",
        "observed_risks",
    ):
        v.strings(data.get(field), f"$.{field}")
    _validate_command_evidence(v, data.get("commands"))
    _validate_criterion_evidence(v, data.get("criteria_evidence"))
    escalation = data.get("requested_escalation")
    if escalation is not None:
        fields = {"code", "reason", "route_to"}
        item = v.object(escalation, "$.requested_escalation", fields, fields)
        for field in fields:
            v.string(item.get(field), f"$.requested_escalation.{field}")
    git = v.object(
        data.get("git"),
        "$.git",
        {"base_revision", "changed_files_digest"},
        {"base_revision", "changed_files_digest"},
    )
    for field in ("base_revision", "changed_files_digest"):
        v.string(git.get(field), f"$.git.{field}")
    if not isinstance(data.get("usage"), dict):
        v.issue("$.usage", "must be an object", "type")
    else:
        try:
            UsageRecord.from_dict(data["usage"])
        except (TypeError, ValueError) as error:
            v.issue("$.usage", str(error), "invalid-usage")
    for field in ("started_at", "finished_at"):
        v.string(data.get(field), f"$.{field}")
    if data.get("metadata") is not None and not isinstance(data.get("metadata"), dict):
        v.issue("$.metadata", "must be an object", "type")
    v.finish()


REVIEW_FIELDS = {
    "schema_version",
    "run_id",
    "plan_revision",
    "plan_digest",
    "task_id",
    "task_contract_digest",
    "result_digest",
    "review_round",
    "outcome",
    "reviewer_identity",
    "permissions",
    "findings",
    "criteria_verdicts",
    "validation_summary",
    "residual_risk",
    "started_at",
    "finished_at",
    "metadata",
}
REVIEW_REQUIRED = REVIEW_FIELDS - {"metadata"}


def _validate_findings(v: _Validator, value: Any) -> None:
    if not isinstance(value, list):
        v.issue("$.findings", "must be an array", "type")
        return
    required = {
        "id",
        "severity",
        "type",
        "path",
        "evidence",
        "impact",
        "correction",
        "disposition",
    }
    allowed = required | {"symbol", "criterion_id"}
    seen: set[str] = set()
    for index, finding in enumerate(value):
        item = v.object(finding, f"$.findings[{index}]", required, allowed)
        finding_id = item.get("id")
        v.identifier(finding_id, f"$.findings[{index}].id")
        if isinstance(finding_id, str) and finding_id in seen:
            v.issue(f"$.findings[{index}].id", "must be unique", "duplicate")
        if isinstance(finding_id, str):
            seen.add(finding_id)
        if item.get("severity") not in {"low", "medium", "high", "critical"}:
            v.issue(f"$.findings[{index}].severity", "has invalid severity", "enum")
        if item.get("type") not in {
            "bounded-correction",
            "architecture-escalation",
            "invalid-contract",
            "insufficient-evidence",
            "acceptance-failure",
            "security-concern",
            "unauthorized-change",
        }:
            v.issue(f"$.findings[{index}].type", "has invalid type", "enum")
        if item.get("disposition") not in {"worker", "architect", "human"}:
            v.issue(f"$.findings[{index}].disposition", "has invalid disposition", "enum")
        for field in ("path", "evidence", "impact", "correction"):
            v.string(item.get(field), f"$.findings[{index}].{field}")


def _validate_verdicts(v: _Validator, value: Any) -> None:
    if not isinstance(value, list):
        v.issue("$.criteria_verdicts", "must be an array", "type")
        return
    fields = {"criterion_id", "status", "evidence"}
    seen: set[str] = set()
    for index, verdict in enumerate(value):
        item = v.object(verdict, f"$.criteria_verdicts[{index}]", fields, fields)
        criterion_id = item.get("criterion_id")
        v.identifier(criterion_id, f"$.criteria_verdicts[{index}].criterion_id")
        if isinstance(criterion_id, str) and criterion_id in seen:
            v.issue(
                f"$.criteria_verdicts[{index}].criterion_id", "must be unique", "duplicate"
            )
        if isinstance(criterion_id, str):
            seen.add(criterion_id)
        if item.get("status") not in {"satisfied", "unsatisfied", "unverified"}:
            v.issue(f"$.criteria_verdicts[{index}].status", "has invalid status", "enum")
        v.string(item.get("evidence"), f"$.criteria_verdicts[{index}].evidence")


def validate_review_data(data: Mapping[str, Any]) -> None:
    v = _Validator()
    v.object(data, "$", REVIEW_REQUIRED, REVIEW_FIELDS)
    if data.get("schema_version") != CONTRACT_SCHEMA_VERSION:
        v.issue("$.schema_version", f"must equal {CONTRACT_SCHEMA_VERSION!r}", "version")
    for field in ("run_id", "task_id"):
        v.identifier(data.get(field), f"$.{field}")
    for field in ("plan_digest", "task_contract_digest", "result_digest", "validation_summary"):
        v.string(data.get(field), f"$.{field}")
    for field in ("plan_revision", "review_round"):
        v.positive_int(data.get(field), f"$.{field}")
    if data.get("outcome") not in {outcome.value for outcome in ReviewOutcome}:
        v.issue("$.outcome", "has an invalid review outcome", "enum")
    _validate_identity(v, data.get("reviewer_identity"), "$.reviewer_identity", reviewer=True)
    permissions = v.object(
        data.get("permissions"),
        "$.permissions",
        {"desired", "effective", "enforcement"},
        {"desired", "effective", "enforcement"},
    )
    if permissions.get("desired") != "read-only":
        v.issue("$.permissions.desired", "reviewer must desire read-only access", "invariant")
    for field in ("effective", "enforcement"):
        v.string(permissions.get(field), f"$.permissions.{field}")
    _validate_findings(v, data.get("findings"))
    _validate_verdicts(v, data.get("criteria_verdicts"))
    v.strings(data.get("residual_risk"), "$.residual_risk")
    for field in ("started_at", "finished_at"):
        v.string(data.get(field), f"$.{field}")
    if data.get("metadata") is not None and not isinstance(data.get("metadata"), dict):
        v.issue("$.metadata", "must be an object", "type")
    v.finish()


@dataclass(frozen=True)
class ContextManifest:
    data: Mapping[str, Any]

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "ContextManifest":
        validate_context_manifest_data(data)
        return cls(dict(data))

    @property
    def digest(self) -> str:
        return digest_json(self.data)


@dataclass(frozen=True)
class TaskContract:
    data: Mapping[str, Any]

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "TaskContract":
        validate_task_data(data)
        return cls(dict(data))

    @property
    def run_id(self) -> str:
        return str(self.data["run_id"])

    @property
    def task_id(self) -> str:
        return str(self.data["task_id"])

    @property
    def plan_revision(self) -> int:
        return int(self.data["plan_revision"])

    @property
    def plan_digest(self) -> str:
        return str(self.data["plan_digest"])

    @property
    def dependencies(self) -> tuple[str, ...]:
        return tuple(str(item) for item in self.data["dependencies"])

    @property
    def scope(self) -> Mapping[str, Any]:
        value = self.data["scope"]
        assert isinstance(value, Mapping)
        return value

    @property
    def acceptance_ids(self) -> tuple[str, ...]:
        criteria = self.data["acceptance_criteria"]
        assert isinstance(criteria, Sequence)
        return tuple(str(item["id"]) for item in criteria)

    @property
    def digest(self) -> str:
        return digest_json(self.data)


@dataclass(frozen=True)
class ResultContract:
    data: Mapping[str, Any]

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "ResultContract":
        validate_result_data(data)
        return cls(dict(data))

    @property
    def status(self) -> ResultStatus:
        return ResultStatus(str(self.data["status"]))

    @property
    def task_id(self) -> str:
        return str(self.data["task_id"])

    @property
    def digest(self) -> str:
        return digest_json(self.data)


@dataclass(frozen=True)
class ReviewContract:
    data: Mapping[str, Any]

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "ReviewContract":
        validate_review_data(data)
        return cls(dict(data))

    @property
    def outcome(self) -> ReviewOutcome:
        return ReviewOutcome(str(self.data["outcome"]))

    @property
    def task_id(self) -> str:
        return str(self.data["task_id"])

    @property
    def digest(self) -> str:
        return digest_json(self.data)


def validate_result_against_task(result: ResultContract, task: TaskContract) -> None:
    issues: list[ValidationIssue] = []
    expected_fields: tuple[tuple[str, object], ...] = (
        ("run_id", task.run_id),
        ("task_id", task.task_id),
        ("plan_revision", task.plan_revision),
        ("plan_digest", task.plan_digest),
        ("task_contract_digest", task.digest),
    )
    for field, expected in expected_fields:
        if result.data.get(field) != expected:
            issues.append(ValidationIssue(f"$.{field}", f"must equal {expected!r}", "stale"))
    provenance = task.data["provenance"]
    assert isinstance(provenance, Mapping)
    git = result.data["git"]
    assert isinstance(git, Mapping)
    if git.get("base_revision") != provenance.get("base_revision"):
        issues.append(
            ValidationIssue("$.git.base_revision", "must match task provenance", "stale")
        )
    reported_files = tuple(sorted(str(item) for item in result.data["files_changed"]))
    try:
        authorize_changed_files(task, reported_files)
    except AuthorizationError as error:
        issues.append(
            ValidationIssue("$.files_changed", str(error), "unauthorized-scope")
        )
    if git.get("changed_files_digest") != digest_json(list(reported_files)):
        issues.append(
            ValidationIssue(
                "$.git.changed_files_digest",
                "must bind the sorted reported file list",
                "digest-mismatch",
            )
        )
    evidence = result.data["criteria_evidence"]
    assert isinstance(evidence, Sequence)
    evidence_by_id = {str(item["criterion_id"]): item for item in evidence}
    validations = task.data["validation"]
    assert isinstance(validations, Sequence)
    command_evidence = result.data["commands"]
    assert isinstance(command_evidence, Sequence)
    command_outcomes = {
        str(item["command"]): item.get("outcome") for item in command_evidence
    }
    if len(command_outcomes) != len(command_evidence):
        issues.append(ValidationIssue("$.commands", "command evidence must be unique", "duplicate"))
    authorization = task.data["authorization"]
    assert isinstance(authorization, Mapping)
    for index, item in enumerate(command_evidence):
        assessment = assess_command(
            str(item["command"]),
            network_authorized=authorization.get("network") is True,
            destructive_authorized=authorization.get("destructive_actions") is True,
        )
        for reason in assessment.reasons:
            issues.append(
                ValidationIssue(
                    f"$.commands[{index}].command",
                    reason,
                    "unauthorized-command",
                )
            )
    if result.status is ResultStatus.COMPLETE:
        for criterion_id in task.acceptance_ids:
            record = evidence_by_id.get(criterion_id)
            if record is None:
                issues.append(
                    ValidationIssue(
                        "$.criteria_evidence",
                        f"missing evidence for {criterion_id}",
                        "missing-evidence",
                    )
                )
            elif record.get("status") != "satisfied":
                issues.append(
                    ValidationIssue(
                        f"$.criteria_evidence[{criterion_id}]",
                        "complete result requires satisfied evidence",
                        "acceptance-failure",
                    )
                )
        required_commands = {
            str(item["command"]) for item in validations if bool(item.get("required"))
        }
        for command in sorted(required_commands):
            if command_outcomes.get(command) != "passed":
                issues.append(
                    ValidationIssue(
                        "$.commands",
                        f"required command did not pass: {command}",
                        "validation-failure",
                    )
                )
        if result.data["blockers"]:
            issues.append(
                ValidationIssue("$.blockers", "complete result cannot contain blockers", "invariant")
            )
    if issues:
        raise ContractValidationError(issues)


def validate_review_against_result(
    review: ReviewContract, result: ResultContract, task: TaskContract
) -> None:
    issues: list[ValidationIssue] = []
    expected: Mapping[str, object] = {
        "run_id": task.run_id,
        "task_id": task.task_id,
        "plan_revision": task.plan_revision,
        "plan_digest": task.plan_digest,
        "task_contract_digest": task.digest,
        "result_digest": result.digest,
    }
    for field, value in expected.items():
        if review.data.get(field) != value:
            issues.append(ValidationIssue(f"$.{field}", f"must equal {value!r}", "stale"))
    verdicts = review.data["criteria_verdicts"]
    assert isinstance(verdicts, Sequence)
    verdict_by_id = {str(item["criterion_id"]): item for item in verdicts}
    if review.outcome is ReviewOutcome.ACCEPTED:
        permissions = review.data["permissions"]
        assert isinstance(permissions, Mapping)
        if permissions.get("effective") not in {"read-only", "unverified"}:
            issues.append(
                ValidationIssue(
                    "$.permissions.effective",
                    "accepted review requires read-only or explicitly unverified permissions",
                    "review-independence",
                )
            )
        if review.data["findings"]:
            issues.append(
                ValidationIssue("$.findings", "accepted review cannot contain findings", "invariant")
            )
        for criterion_id in task.acceptance_ids:
            if verdict_by_id.get(criterion_id, {}).get("status") != "satisfied":
                issues.append(
                    ValidationIssue(
                        "$.criteria_verdicts",
                        f"accepted review must satisfy {criterion_id}",
                        "acceptance-failure",
                    )
                )
    if issues:
        raise ContractValidationError(issues)
