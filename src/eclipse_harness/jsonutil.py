"""Deterministic JSON and hashing helpers."""

from __future__ import annotations

import hashlib
import json
import os
import tempfile
from pathlib import Path
from typing import Any, Mapping

MAX_STRUCTURED_FILE_BYTES = 8 * 1024 * 1024
MAX_TEXT_FILE_BYTES = 1024 * 1024


class DuplicateKeyError(ValueError):
    """A JSON object used an ambiguous duplicate member name."""


def _unique_object(pairs: list[tuple[str, Any]]) -> dict[str, Any]:
    value: dict[str, Any] = {}
    for key, item in pairs:
        if key in value:
            raise DuplicateKeyError(f"duplicate JSON object key: {key!r}")
        value[key] = item
    return value


def canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def digest_json(value: object) -> str:
    return "sha256:" + hashlib.sha256(canonical_json(value).encode("utf-8")).hexdigest()


def load_json(path: Path) -> Any:
    size = path.stat().st_size
    if size > MAX_STRUCTURED_FILE_BYTES:
        raise ValueError(
            f"JSON file exceeds {MAX_STRUCTURED_FILE_BYTES} byte limit: {path}"
        )
    with path.open("r", encoding="utf-8") as handle:
        return json.load(handle, object_pairs_hook=_unique_object)


def read_text_bounded(path: Path, *, limit: int = MAX_TEXT_FILE_BYTES) -> str:
    size = path.stat().st_size
    if size > limit:
        raise ValueError(f"text file exceeds {limit} byte limit: {path}")
    return path.read_text(encoding="utf-8")


def write_json_atomic(path: Path, value: object) -> None:
    serialized = json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    write_text_atomic(path, serialized)


def write_text_atomic(path: Path, value: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(value)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    except BaseException:
        try:
            os.unlink(temporary)
        except FileNotFoundError:
            pass
        raise


def require_object(value: Any, label: str) -> Mapping[str, Any]:
    if not isinstance(value, dict):
        raise TypeError(f"{label} must be a JSON object")
    return value
