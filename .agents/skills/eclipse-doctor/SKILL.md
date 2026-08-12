---
name: eclipse-doctor
description: Diagnose Eclipse installation, skill and agent discovery, requested/configured/effective model routes, reasoning settings, permissions, recursion controls, concurrency, git worktrees, schemas, adapter drift, and degraded/manual modes. Use before relying on native host routing or cost claims.
---

# Eclipse Doctor

Prefer deterministic, non-destructive inspection.

1. Run `eclipse --json doctor`; supply a host-observed route file only when the host exposes reliable runtime metadata.
2. Verify the Eclipse version, `.agents/skills` source, host/surface/version, native profiles, current configuration fields, worker recursion controls, requested permissions, worktree support, and required tools.
3. Distinguish requested, configured, effective, and verified models/reasoning. Configuration and worker self-report cannot prove effective identity.
4. Surface parent/runtime overrides, unsupported options, permission gaps, policy mismatch, missing profiles, route inheritance, and manual/policy-only degradation.
5. Write `.eclipse/capabilities.json` only when requested. Never persist credentials, environment values, private prompts, or session content.

Read [capabilities.md](references/capabilities.md) to interpret the snapshot and [host-probes.md](references/host-probes.md) for Codex/Copilot limitations.
