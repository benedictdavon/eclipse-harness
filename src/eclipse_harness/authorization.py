"""Repository-bounded write and effect authorization."""

from __future__ import annotations

import fnmatch
from pathlib import Path, PurePosixPath
from typing import TYPE_CHECKING, Iterable, Mapping

from .errors import AuthorizationError

if TYPE_CHECKING:
    from .contracts import ResultContract, TaskContract

def normalize_repo_path(value: str) -> str:
    normalized = value.replace("\\", "/")
    candidate = PurePosixPath(normalized)
    if candidate.is_absolute() or not candidate.parts or ".." in candidate.parts:
        raise AuthorizationError(f"path escapes repository boundary: {value!r}")
    if candidate.parts[0].endswith(":"):
        raise AuthorizationError(f"drive-qualified path is not portable: {value!r}")
    # PurePosixPath already removes a syntactic leading ``./``.  Using
    # ``lstrip`` here would also strip meaningful leading dots from names such
    # as ``.git`` and ``.eclipse`` and could redirect a containment check to a
    # different path.
    return candidate.as_posix()


def glob_matches(path: str, pattern: str) -> bool:
    normalized_path = normalize_repo_path(path)
    normalized_pattern = normalize_repo_path(pattern)
    if fnmatch.fnmatchcase(normalized_path, normalized_pattern):
        return True
    if normalized_pattern.endswith("/**"):
        root = normalized_pattern[:-3].rstrip("/")
        return normalized_path == root or normalized_path.startswith(root + "/")
    return False


def ensure_repository_bounded(root: Path, relative: str) -> Path:
    normalized = normalize_repo_path(relative)
    root_resolved = root.resolve()
    candidate = (root_resolved / normalized).resolve(strict=False)
    try:
        candidate.relative_to(root_resolved)
    except ValueError as error:
        raise AuthorizationError(f"resolved path escapes repository: {relative!r}") from error
    return candidate


def authorize_changed_files(task: TaskContract, changed_files: Iterable[str]) -> tuple[str, ...]:
    scope = task.scope
    write_globs = tuple(str(item) for item in scope["write_globs"])
    forbidden = tuple(str(item) for item in scope["forbidden_globs"])
    normalized: list[str] = []
    violations: list[str] = []
    for path in changed_files:
        item = normalize_repo_path(path)
        normalized.append(item)
        if any(glob_matches(item, pattern) for pattern in forbidden):
            violations.append(f"{item}: explicitly forbidden")
        elif not any(glob_matches(item, pattern) for pattern in write_globs):
            violations.append(f"{item}: outside authorized write_globs")
    if violations:
        raise AuthorizationError("unauthorized file changes: " + "; ".join(violations))
    return tuple(normalized)


def authorize_result(task: TaskContract, result: ResultContract) -> None:
    files = result.data["files_changed"]
    assert isinstance(files, list)
    authorize_changed_files(task, (str(item) for item in files))
    authorization = task.data["authorization"]
    assert isinstance(authorization, Mapping)
    escalation = result.data["requested_escalation"]
    if escalation and escalation.get("code") == "AUTH_REQUIRED":
        return
    if result.data["deviations"] and not authorization.get("external_side_effects", False):
        # Deviations are permitted as disclosures, but never treated as implied authorization.
        return
