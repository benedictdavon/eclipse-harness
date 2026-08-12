from __future__ import annotations

from pathlib import Path

import pytest

from eclipse_harness.config import validate_config
from eclipse_harness.errors import ConfigurationError
from eclipse_harness.migration import inspect_soluna_workflow, write_migration


def test_legacy_migration_is_conservative(tmp_path: Path) -> None:
    fixture = Path(__file__).parents[1] / "fixtures" / "legacy-soluna"
    result = inspect_soluna_workflow(fixture)
    assert result.detected
    assert validate_config(result.config).max_parallel_writers == 2
    assert any(item.source.endswith("max_depth") and item.disposition == "not-mapped" for item in result.items)
    files = write_migration(fixture, tmp_path, result)
    assert ".eclipse/config.json" in files
    assert (tmp_path / "docs/ai/PROJECT_CONTEXT.legacy.md").is_file()
    assert (fixture / ".codex/config.toml").is_file()
    with pytest.raises(ConfigurationError, match="refuses to overwrite"):
        write_migration(fixture, tmp_path, result)


def test_migration_dry_run_writes_nothing(tmp_path: Path) -> None:
    fixture = Path(__file__).parents[1] / "fixtures" / "legacy-soluna"
    result = inspect_soluna_workflow(fixture)
    write_migration(fixture, tmp_path, result, dry_run=True)
    assert not any(tmp_path.iterdir())
