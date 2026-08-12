"""Domain-specific failures with stable CLI classifications."""

from dataclasses import dataclass
from typing import Iterable


@dataclass(frozen=True)
class ValidationIssue:
    path: str
    message: str
    code: str = "invalid"

    def __str__(self) -> str:
        return f"{self.path}: {self.message} [{self.code}]"


class EclipseError(Exception):
    """Base class for expected harness failures."""

    exit_code = 2


class ContractValidationError(EclipseError):
    """A structured contract failed deterministic validation."""

    def __init__(self, issues: Iterable[ValidationIssue]):
        self.issues = tuple(issues)
        super().__init__("; ".join(str(issue) for issue in self.issues))


class ConfigurationError(EclipseError):
    """Configuration is invalid or unsafe."""


class StateTransitionError(EclipseError):
    """A requested lifecycle transition is invalid."""


class StaleWorkError(EclipseError):
    """A task or result belongs to an obsolete plan revision."""


class AuthorizationError(EclipseError):
    """Requested writes or effects exceed the task authorization."""


class ConcurrencyError(EclipseError):
    """Tasks cannot safely execute concurrently."""


class RecoveryError(EclipseError):
    """Persisted run state is incomplete or corrupted."""


class AdapterError(EclipseError):
    """A host adapter could not be rendered or verified."""
