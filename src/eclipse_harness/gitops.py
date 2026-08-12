"""Cross-platform git/worktree isolation primitives."""

from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

from .authorization import normalize_repo_path
from .errors import EclipseError, StaleWorkError
from .process import run_bounded

_REVISION = re.compile(r"^[0-9a-fA-F]{40,64}$")
_BRANCH = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._/-]{0,254}$")


@dataclass(frozen=True)
class CommandResult:
    command: tuple[str, ...]
    exit_code: int
    stdout: str
    stderr: str


@dataclass(frozen=True)
class WorktreeSpec:
    task_id: str
    base_revision: str
    branch: str
    path: Path


class GitError(EclipseError):
    """Git operation failed without mutating outside the requested scope."""


class GitRepository:
    def __init__(self, root: Path):
        self.root = root.resolve()

    def run(self, arguments: Sequence[str], *, check: bool = True) -> CommandResult:
        command = ("git", *arguments)
        completed = run_bounded(command, cwd=self.root, timeout=60)
        result = CommandResult(command, completed.returncode, completed.stdout, completed.stderr)
        if check and result.exit_code != 0:
            raise GitError(f"{' '.join(command)} failed: {result.stderr.strip()[:65536]}")
        return result

    def current_revision(self) -> str:
        return self.run(("rev-parse", "HEAD")).stdout.strip()

    def verify_base(self, expected: str) -> None:
        observed = self.current_revision()
        if observed != expected:
            raise StaleWorkError(f"repository HEAD {observed} does not match task base {expected}")

    def resolve_revision(self, revision: str) -> str:
        if not _REVISION.fullmatch(revision):
            raise GitError("git revision must be a full hexadecimal object id")
        return self.run(("rev-parse", "--verify", "--end-of-options", f"{revision}^{{commit}}")).stdout.strip()

    def changed_files(self, base_revision: str) -> tuple[str, ...]:
        base = self.resolve_revision(base_revision)
        tracked = self.run(("diff", "--name-only", "-z", base, "--")).stdout
        untracked = self.run(("ls-files", "--others", "--exclude-standard", "-z", "--")).stdout
        paths = {
            normalize_repo_path(item)
            for item in (tracked + untracked).split("\0")
            if item
        }
        return tuple(sorted(paths))

    def is_clean(self) -> bool:
        return not self.run(("status", "--porcelain")).stdout.strip()

    def supports_worktrees(self) -> bool:
        return self.run(("worktree", "list", "--porcelain"), check=False).exit_code == 0

    def prepare_worktree(self, spec: WorktreeSpec) -> CommandResult:
        if spec.path.exists():
            raise GitError(f"worktree path already exists: {spec.path}")
        if (
            not _BRANCH.fullmatch(spec.branch)
            or ".." in spec.branch
            or "@{" in spec.branch
            or spec.branch.endswith(("/", "."))
        ):
            raise GitError("branch name is not portable or safe")
        base = self.resolve_revision(spec.base_revision)
        return self.run(
            ("worktree", "add", "-b", spec.branch, str(spec.path), base)
        )

    def merge_base(self, left: str, right: str) -> str:
        return self.run(("merge-base", left, right)).stdout.strip()

    def conflict_probe(self, base: str, left: str, right: str) -> CommandResult:
        return self.run(("merge-tree", base, left, right), check=False)
