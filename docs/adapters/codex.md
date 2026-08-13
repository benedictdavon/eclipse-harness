# Codex adapter

Eclipse generates project-scoped `.codex/config.toml` plus standalone `.codex/agents/*.toml` roles for architect, worker, escalation worker, and reviewer.

The generated config uses the current canonical `agents.max_concurrent_threads_per_session` field. Every custom agent defines `name`, `description`, and `developer_instructions`; model and `model_reasoning_effort` express policy intent. Architect/reviewer request `read-only`; workers request `workspace-write` with network disabled and `[agents] enabled = false` to prevent descendant spawning.

`eclipse adapters generate --host codex --max-concurrency N` writes `N` to that field; values outside 1–16 are rejected.

Codex project config loads only when the project is trusted. Parent/live permission overrides can affect child agents. Consequently, a configured sandbox or model is not proof of effective runtime state. Doctor reports Codex configuration and permissions independently from every other adapter.

The adapter supports Codex CLI and the Codex app project model to the degree their common project configuration and skill discovery permit. It does not claim that every surface exposes the same approval controls or runtime attestation.

Generation is optional. The skills remain usable without generated profiles. Generate without overwriting user-owned files:

```bash
eclipse adapters generate --host codex --dry-run
eclipse adapters generate --host codex
eclipse --json doctor
```

If native child identity is unverified, use policy-only/manual labeling or require verified routing in the invoking workflow. A trusted observation file may be supplied to doctor only when produced from actual host runtime metadata. A worker saying “I am Luna” is not attestation.

Ordinary observation JSON remains untrusted even when it contains a `host-observed` label. The
operator must explicitly pass `--trust-observations` after verifying the file came from the host.

Codex owns spawning, commands, permissions, filesystem changes, git, and scheduling. Eclipse role files provide instructions and requested settings only.
