from __future__ import annotations

from pathlib import Path

import pytest

from eclipse_harness.authorization import (
    authorize_changed_files,
    ensure_repository_bounded,
    normalize_repo_path,
)
from eclipse_harness.errors import AuthorizationError
from eclipse_harness.security import assess_command, redact_text, scan_for_secrets


def test_changed_files_are_authorized(task) -> None:  # type: ignore[no-untyped-def]
    files = authorize_changed_files(
        task,
        ["tests/fixtures/simple-python/src/simple/greeting.py"],
    )
    assert files == ("tests/fixtures/simple-python/src/simple/greeting.py",)


def test_task_declared_forbidden_path_is_rejected(task) -> None:  # type: ignore[no-untyped-def]
    with pytest.raises(AuthorizationError, match="forbidden"):
        authorize_changed_files(task, [".eclipse/runs/example/run.json"])


@pytest.mark.parametrize("path", ["../secret", "/etc/passwd", "C:/Windows/system.ini"])
def test_path_traversal_is_rejected(path: str) -> None:
    with pytest.raises(AuthorizationError):
        normalize_repo_path(path)


def test_leading_dot_path_is_preserved() -> None:
    assert normalize_repo_path("./.github/agents/worker.md") == ".github/agents/worker.md"


def test_symlink_escape_is_rejected(tmp_path: Path) -> None:
    outside = tmp_path.parent / "outside-target"
    outside.mkdir(exist_ok=True)
    link = tmp_path / "link"
    try:
        link.symlink_to(outside, target_is_directory=True)
    except OSError:
        pytest.skip("symlinks unavailable")
    with pytest.raises(AuthorizationError, match="escapes"):
        ensure_repository_bounded(tmp_path, "link/file.txt")


def test_secret_scanning_and_redaction() -> None:
    value = {"token": "ghp_abcdefghijklmnopqrstuvwxyz1234567890"}
    assert scan_for_secrets(value)[0].kind == "github-token"
    assert "REDACTED" in redact_text(value["token"])


def test_command_assessment_requires_boundaries() -> None:
    network = assess_command("pip install package", network_authorized=False, destructive_authorized=False)
    assert not network.allowed
    destructive = assess_command(
        "git reset --hard HEAD", network_authorized=False, destructive_authorized=False
    )
    assert not destructive.allowed and destructive.requires_human
