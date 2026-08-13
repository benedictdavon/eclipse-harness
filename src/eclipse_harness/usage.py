"""Measured, estimated, and unavailable usage records."""

from __future__ import annotations

import math
from dataclasses import dataclass
from enum import Enum
from typing import Any, Mapping


class UsageQuality(str, Enum):
    MEASURED = "measured"
    ESTIMATED = "estimated"
    UNAVAILABLE = "unavailable"


_USAGE_FIELDS = {
    "quality",
    "input_tokens",
    "output_tokens",
    "cost",
    "currency",
    "source",
}


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
        unknown = sorted(set(data) - _USAGE_FIELDS)
        if unknown:
            raise ValueError("unsupported usage field(s): " + ", ".join(unknown))
        quality = UsageQuality(str(data.get("quality")))
        input_tokens = _optional_nonnegative_int(data.get("input_tokens"), "input_tokens")
        output_tokens = _optional_nonnegative_int(data.get("output_tokens"), "output_tokens")
        cost_value = data.get("cost")
        if cost_value is not None:
            if isinstance(cost_value, bool) or not isinstance(cost_value, (int, float)):
                raise ValueError("cost must be numeric or null")
            if not math.isfinite(cost_value) or cost_value < 0:
                raise ValueError("cost must be a non-negative finite number or null")
        currency = data.get("currency")
        if currency is not None and not isinstance(currency, str):
            raise ValueError("currency must be a string or null")
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
            currency=currency,
            source=source,
        )


def _optional_nonnegative_int(value: Any, field: str) -> int | None:
    if value is None:
        return None
    if not isinstance(value, int) or isinstance(value, bool) or value < 0:
        raise ValueError(f"{field} must be a non-negative integer or null")
    return value
