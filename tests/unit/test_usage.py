from __future__ import annotations

import pytest

from eclipse_harness.usage import UsageQuality, UsageRecord


def test_measured_usage() -> None:
    record = UsageRecord.from_dict(
        {"quality": "measured", "input_tokens": 10, "output_tokens": 5, "cost": None, "currency": None, "source": "host"}
    )
    assert record.quality is UsageQuality.MEASURED


def test_unavailable_usage_cannot_contain_tokens() -> None:
    with pytest.raises(ValueError, match="cannot contain"):
        UsageRecord.from_dict(
            {"quality": "unavailable", "input_tokens": 10, "output_tokens": None, "cost": None, "currency": None, "source": "host"}
        )
