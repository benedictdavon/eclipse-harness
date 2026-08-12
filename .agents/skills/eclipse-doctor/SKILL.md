---
name: eclipse-doctor
description: Diagnose Eclipse installation, skill and agent discovery, host-specific requested/configured/effective routes, permissions, recursion controls, adapter drift, and degraded/manual modes. Use before relying on native host routing or cost claims; the Python CLI is optional.
---

# Eclipse Doctor

Prefer deterministic, non-destructive inspection.

1. Inspect the active host and each installed adapter independently. If the optional CLI is available, run `eclipse --json doctor`; supply an observation file only when the host exposes reliable runtime metadata.
2. Verify `.agents/skills`, host/surface/version, native profiles, worker recursion controls, and requested permissions. Do not require Python tooling for the workflow itself.
3. Distinguish requested, configured, effective, and verified models/reasoning. Configuration and worker self-report cannot prove effective identity.
4. Surface parent/runtime overrides, unsupported options, permission gaps, policy mismatch, missing profiles, route inheritance, and manual/policy-only degradation per host. Never let a valid Copilot profile hide an invalid Codex profile or vice versa.
5. Write `.eclipse/capabilities.json` only when requested. Never persist credentials, environment values, private prompts, or session content.

Read [capabilities.md](references/capabilities.md) to interpret the snapshot and [host-probes.md](references/host-probes.md) for Codex/Copilot limitations.
