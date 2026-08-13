from __future__ import annotations

import json
from pathlib import Path

import pytest

from eclipse_harness.adapters import (
    AdapterArtifact,
    CodexAdapter,
    CopilotAdapter,
    install_artifacts,
)
from eclipse_harness.errors import AdapterError, AuthorizationError
from eclipse_harness.routing import Policy


def _policy() -> Policy:
    root = Path(__file__).parents[2]
    return Policy.from_dict(json.loads((root / "policies/sol-luna.json").read_text(encoding="utf-8")))


def test_codex_adapter_uses_current_fields() -> None:
    artifacts = CodexAdapter().render(_policy())
    config = artifacts[0].content
    assert "max_concurrent_threads_per_session" in config
    assert "max_threads" not in config
    assert "max_depth" not in config
    worker = next(item.content for item in artifacts if item.relative_path.endswith("eclipse_worker.toml"))
    assert "network_access = false" in worker
    assert "[agents]\nenabled = false" in worker
    reviewer = next(item.content for item in artifacts if item.relative_path.endswith("eclipse_reviewer.toml"))
    assert 'sandbox_mode = "read-only"' in reviewer


def test_codex_concurrency_input_controls_generated_field() -> None:
    config = CodexAdapter().render(_policy(), max_concurrency=7)[0].content
    assert "max_concurrent_threads_per_session = 7" in config


@pytest.mark.parametrize("value", [0, 17, True])
def test_codex_rejects_invalid_concurrency(value: object) -> None:
    with pytest.raises(AdapterError, match="max_concurrency"):
        CodexAdapter().render(_policy(), max_concurrency=value)  # type: ignore[arg-type]


def test_copilot_adapter_degrades_without_model_claim() -> None:
    artifacts = CopilotAdapter().render(_policy())
    worker = next(item.content for item in artifacts if "worker" in item.relative_path)
    assert 'tools: ["read", "search", "edit", "execute"]' in worker
    assert "\nmodel:" not in worker
    assert "disable-model-invocation: true" in worker


def test_install_is_idempotent_and_protects_user_files(tmp_path: Path) -> None:
    artifacts = CodexAdapter().render(_policy())
    first = install_artifacts(tmp_path, artifacts)
    second = install_artifacts(tmp_path, artifacts)
    assert any(item.action == "create" for item in first)
    assert all(item.action == "unchanged" for item in second)
    target = tmp_path / artifacts[0].relative_path
    target.write_text("user-owned\n", encoding="utf-8")
    with pytest.raises(AdapterError, match="refusing"):
        install_artifacts(tmp_path, artifacts)


def test_install_rejects_artifact_path_escape(tmp_path: Path) -> None:
    with pytest.raises(AuthorizationError, match="escapes"):
        install_artifacts(tmp_path, [AdapterArtifact("../outside", "content")])
