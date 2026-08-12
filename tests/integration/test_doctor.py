from __future__ import annotations

import json
import shutil
from pathlib import Path

from eclipse_harness.adapters import CodexAdapter, CopilotAdapter, install_artifacts
from eclipse_harness.doctor import run_doctor
from eclipse_harness.routing import Policy


def _policy(root: Path) -> Policy:
    return Policy.from_dict(json.loads((root / "policies/sol-luna.json").read_text(encoding="utf-8")))


def test_doctor_never_infers_effective_model(tmp_path: Path) -> None:
    repository = Path(__file__).parents[2]
    snapshot = run_doctor(repository, _policy(repository))
    worker = snapshot.routes["worker"]
    assert worker["requested_model"] == "gpt-5.6-luna"
    assert worker["configured_by_host"]["codex"] == "gpt-5.6-luna"
    assert worker["effective_model"] is None
    assert worker["status"] == "unverified"


def test_doctor_detects_route_inheritance(tmp_path: Path) -> None:
    repository = Path(__file__).parents[2]
    observations = tmp_path / "observations.json"
    observations.write_text(
        json.dumps(
            {
                "routes": {
                    "worker": {
                        "source": "host-observed",
                        "effective_model": "gpt-5.6-sol"
                    }
                }
            }
        ),
        encoding="utf-8",
    )
    snapshot = run_doctor(
        repository,
        _policy(repository),
        observation_file=observations,
        trust_observations=True,
    )
    assert snapshot.routes["worker"]["status"] == "broken"


def test_doctor_does_not_trust_observation_label_by_default(tmp_path: Path) -> None:
    repository = Path(__file__).parents[2]
    observations = tmp_path / "observations.json"
    observations.write_text(
        '{"routes":{"worker":{"source":"host-observed","effective_model":"wrong"}}}',
        encoding="utf-8",
    )
    snapshot = run_doctor(repository, _policy(repository), observation_file=observations)
    assert snapshot.routes["worker"]["status"] == "unverified"
    assert any(item.check == "observations" for item in snapshot.diagnostics)


def test_doctor_reports_bad_codex_reviewer_even_with_valid_copilot_profile(
    tmp_path: Path,
    monkeypatch,
) -> None:
    repository = Path(__file__).parents[2]
    policy = _policy(repository)
    install_artifacts(
        tmp_path,
        (*CodexAdapter().render(policy), *CopilotAdapter().render(policy)),
    )
    shutil.copytree(repository / ".agents", tmp_path / ".agents")
    reviewer = tmp_path / ".codex/agents/eclipse_reviewer.toml"
    reviewer.write_text(
        reviewer.read_text(encoding="utf-8").replace(
            'sandbox_mode = "read-only"',
            'sandbox_mode = "workspace-write"',
        ),
        encoding="utf-8",
    )
    monkeypatch.setenv("ECLIPSE_HOST", "copilot-cli")

    snapshot = run_doctor(tmp_path, policy)

    assert snapshot.agents["active_host"] == "copilot-cli"
    assert snapshot.permissions["codex"]["reviewer"]["configured"] == "workspace-write"
    assert snapshot.permissions["copilot"]["reviewer"]["configured"] == "read/search only"
    assert any(
        item.check == "reviewer-permissions:codex" and item.level == "error"
        for item in snapshot.diagnostics
    )
    assert any(
        item.check == "reviewer-permissions:copilot" and item.level == "pass"
        for item in snapshot.diagnostics
    )
