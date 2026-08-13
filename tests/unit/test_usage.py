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


@pytest.mark.parametrize("cost", [-0.01, float("nan"), float("inf"), float("-inf")])
def test_usage_rejects_negative_or_non_finite_cost(cost: float) -> None:
    with pytest.raises(ValueError, match="non-negative finite"):
        UsageRecord.from_dict(
            {
                "quality": "measured",
                "cost": cost,
                "currency": "USD",
                "source": "host",
            }
        )


def test_usage_rejects_unsupported_fields() -> None:
    with pytest.raises(ValueError, match="unsupported usage field.*provider_request_id"):
        UsageRecord.from_dict(
            {
                "quality": "measured",
                "source": "host",
                "provider_request_id": "request-123",
            }
        )
