from __future__ import annotations

import subprocess
from pathlib import Path

from eclipse_harness.gitops import GitRepository, WorktreeSpec


def _git(path: Path, *arguments: str) -> str:
    return subprocess.run(
        ("git", *arguments),
        cwd=path,
        check=True,
        text=True,
        stdout=subprocess.PIPE,
    ).stdout.strip()


def test_prepare_isolated_worktree(tmp_path: Path) -> None:
    repository = tmp_path / "repository"
    repository.mkdir()
    _git(repository, "init", "-b", "main")
    _git(repository, "config", "user.name", "Test")
    _git(repository, "config", "user.email", "test@example.com")
    (repository / "README.md").write_text("fixture\n", encoding="utf-8")
    _git(repository, "add", "README.md")
    _git(repository, "commit", "-m", "initial")
    base = _git(repository, "rev-parse", "HEAD")
    target = tmp_path / "worktree"
    git = GitRepository(repository)
    assert git.is_clean() and git.supports_worktrees()
    git.prepare_worktree(WorktreeSpec("T001", base, "eclipse/task-T001", target))
    assert (target / ".git").exists()
    assert _git(target, "rev-parse", "HEAD") == base


def test_changed_files_include_tracked_and_untracked(tmp_path: Path) -> None:
    repository = tmp_path / "repository"
    repository.mkdir()
    _git(repository, "init", "-b", "main")
    _git(repository, "config", "user.name", "Test")
    _git(repository, "config", "user.email", "test@example.com")
    (repository / "tracked.txt").write_text("initial\n", encoding="utf-8")
    _git(repository, "add", "tracked.txt")
    _git(repository, "commit", "-m", "initial")
    base = _git(repository, "rev-parse", "HEAD")
    (repository / "tracked.txt").write_text("changed\n", encoding="utf-8")
    (repository / "untracked.txt").write_text("new\n", encoding="utf-8")
    assert GitRepository(repository).changed_files(base) == ("tracked.txt", "untracked.txt")
