from __future__ import annotations

from pathlib import Path

import pytest

from eclipse_harness.jsonutil import DuplicateKeyError, load_json


def test_duplicate_json_keys_are_rejected(tmp_path: Path) -> None:
    path = tmp_path / "duplicate.json"
    path.write_text('{"authorization": false, "authorization": true}', encoding="utf-8")
    with pytest.raises(DuplicateKeyError, match="duplicate"):
        load_json(path)
