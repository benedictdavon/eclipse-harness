"""Measured, estimated, and unavailable usage records."""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping


class UsageQuality(str, Enum):
    MEASURED = "measured"
    ESTIMATED = "estimated"
    UNAVAILABLE = "unavailable"


@dataclass(frozen=True)
class UsageRecord:
    quality: UsageQuality
    input_tokens: int | None
    output_tokens: int | None
    cost: float | None
    currency: str | None
    source: str

    @classmethod
    def from_dict(cls, data: Mapping[str, Any]) -> "UsageRecord":
        quality = UsageQuality(str(data.get("quality")))
        input_tokens = _optional_nonnegative_int(data.get("input_tokens"), "input_tokens")
        output_tokens = _optional_nonnegative_int(data.get("output_tokens"), "output_tokens")
        cost_value = data.get("cost")
        if cost_value is not None and not isinstance(cost_value, (int, float)):
            raise ValueError("cost must be numeric or null")
        source = data.get("source")
        if not isinstance(source, str) or not source:
            raise ValueError("usage source is required")
        if quality is UsageQuality.UNAVAILABLE and any(
            value is not None for value in (input_tokens, output_tokens, cost_value)
        ):
            raise ValueError("unavailable usage cannot contain measurements")
        if cost_value is not None and not data.get("currency"):
            raise ValueError("currency is required when cost is present")
        return cls(
            quality=quality,
            input_tokens=input_tokens,
            output_tokens=output_tokens,
            cost=None if cost_value is None else float(cost_value),
            currency=None if data.get("currency") is None else str(data["currency"]),
            source=source,
        )


def _optional_nonnegative_int(value: Any, field: str) -> int | None:
    if value is None:
        return None
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ValueError(f"{field} must be a non-negative integer or null")
    return value
