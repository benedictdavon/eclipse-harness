from __future__ import annotations

import copy

import pytest

from eclipse_harness.config import DEFAULT_CONFIG, validate_config
from eclipse_harness.errors import ConfigurationError


def test_default_config_is_valid() -> None:
    assert validate_config(DEFAULT_CONFIG).max_parallel_writers == 2


def test_config_rejects_unknown_fields() -> None:
    value = copy.deepcopy(DEFAULT_CONFIG)
    value["unknown"] = True
    with pytest.raises(ConfigurationError, match="unknown"):
        validate_config(value)


def test_config_rejects_boolean_integer() -> None:
    value = copy.deepcopy(DEFAULT_CONFIG)
    value["concurrency"]["max_parallel_writers"] = True
    with pytest.raises(ConfigurationError, match="1..16"):
        validate_config(value)
