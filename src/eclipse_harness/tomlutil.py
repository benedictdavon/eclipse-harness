"""Typed compatibility wrapper for TOML parsing on Python 3.10+."""

from __future__ import annotations

import sys
from importlib import import_module
from typing import Any, BinaryIO, cast


def load_toml(handle: BinaryIO) -> dict[str, Any]:
    """Load TOML through the standard library or the Python 3.10 backport."""

    module_name = "tomllib" if sys.version_info >= (3, 11) else "tomli"
    module = import_module(module_name)
    value = module.load(handle)
    if not isinstance(value, dict):  # pragma: no cover - parser contract guard
        raise ValueError("TOML root must be a table")
    return cast(dict[str, Any], value)
