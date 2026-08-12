# Codex adapter

Eclipse generates project-scoped `.codex/config.toml` plus standalone `.codex/agents/*.toml` roles for architect, worker, escalation worker, and reviewer.

The generated config uses the current canonical `agents.max_concurrent_threads_per_session` field. Every custom agent defines `name`, `description`, and `developer_instructions`; model and `model_reasoning_effort` express policy intent. Architect/reviewer request `read-only`; workers request `workspace-write` with network disabled and `[agents] enabled = false` to prevent descendant spawning.

Codex project config loads only when the project is trusted. Parent/live permission overrides can affect child agents. Consequently, a configured sandbox or model is not proof of effective runtime state. Doctor reports requested, configured, effective, and verification separately.

The adapter supports Codex CLI and the Codex app project model to the degree their common project configuration and skill discovery permit. It does not claim that every surface exposes the same approval controls or runtime attestation.

Generate without overwriting user-owned files:

```bash
eclipse adapters generate --host codex --dry-run
eclipse adapters generate --host codex
eclipse --json doctor
```

If native child identity is unverified, strict mode fails; standard mode labels it policy-only. A trusted observation file may be supplied to doctor only when produced from actual host runtime metadata. A worker saying “I am Luna” is not attestation.

Ordinary observation JSON remains untrusted even when it contains a `host-observed` label. The
operator must explicitly pass `--trust-observations` after verifying the file came from the host.
