# Known limitations

- Eclipse v0.1 is not an autonomous multi-provider runtime. It prepares and validates contracts; the host or human runs agents.
- Effective model, reasoning, permission, and sandbox attestation depends on trustworthy host metadata. Configuration and self-report remain unverified.
- Codex app/CLI and Copilot surfaces may apply runtime overrides or differ in available features.
- Copilot profiles inherit host model selection and do not offer claimed Sol/Luna parity.
- Glob overlap detection is conservative and cannot prove arbitrary semantic independence; planners must declare shared interfaces/resources.
- Command recognition cannot prove the effects of arbitrary shell scripts or encoded/interpreter-based commands; host sandboxing and human authorization remain required.
- Runtime state and evidence use strict parsing, atomic writes, and digests, but are not cryptographically signed against an actor who can directly rewrite `.eclipse/runs` despite the worker write prohibition.
- Existing symlink escapes are rejected, but portable path checks cannot eliminate a same-account attacker replacing a parent directory between check and open; host filesystem isolation remains the control for that race.
- Worktree preparation exists, but automatic multi-branch integration and rollback orchestration are outside v0.1.
- Secret scanning is pattern based and cannot replace host secret isolation.
- JSON Schema covers structural interoperability; Python validators add cross-field semantics.
- Legacy Markdown plans are preserved for semantic human conversion rather than guessed automatically.
- Evaluation infrastructure ships representative cases and recorded fixtures, not live benchmark results or cost-saving claims.
- No external providers, provider credentials, billing probes, MCP routing, GUI, autopilot, or arbitrary agent marketplace is included.
