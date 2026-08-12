"""Structured, secret-safe run events."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Any, Mapping

from .constants import EVENT_SCHEMA_VERSION
from .security import redact_text


@dataclass(frozen=True)
class RunEvent:
    event_id: str
    run_id: str
    event_type: str
    timestamp: str
    task_id: str | None
    details: Mapping[str, Any]

    def to_dict(self) -> dict[str, Any]:
        return {
            "schema_version": EVENT_SCHEMA_VERSION,
            "event_id": self.event_id,
            "run_id": self.run_id,
            "event_type": self.event_type,
            "timestamp": self.timestamp,
            "task_id": self.task_id,
            "details": _redact(self.details),
        }


def _redact(value: Any) -> Any:
    if isinstance(value, str):
        return redact_text(value)
    if isinstance(value, list):
        return [_redact(item) for item in value]
    if isinstance(value, dict):
        return {str(key): _redact(item) for key, item in value.items()}
    return value
