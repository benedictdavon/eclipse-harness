# Host probes

## Codex

Current project profiles live under `.codex/agents/*.toml`; project configuration loads only for trusted projects. The canonical concurrency field is `agents.max_concurrent_threads_per_session`. Worker profiles set `[agents] enabled = false`; do not rely on legacy `max_depth` for V2 recursion prevention.

Codex parent/live permission overrides can affect children. A role's configured sandbox is intent until the running surface proves its effective policy. Custom-agent model fields likewise remain requested/configured until host-observed metadata attests the child. Check Codex profiles even when Copilot profiles are also installed.

## GitHub Copilot

Project profiles live under `.github/agents/*.agent.md`; shared skills live under `.agents/skills`. Tool aliases express capability intent, but exact enforcement and model availability vary by surface/account. Generated Eclipse profiles omit fixed model names and use manual invocation to avoid pretending native topology or model parity.

Copilot CLI can expose a selected model in non-silent output, but that observation must be captured by trusted host integration before it becomes an Eclipse attestation. A correct Copilot read-only tool profile cannot compensate for a writable Codex reviewer profile.
