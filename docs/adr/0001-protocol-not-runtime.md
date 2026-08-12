# ADR 0001: Protocol and skill suite, not provider runtime

Status: accepted for v0.1

The research found that skills/contracts are portable while model routing, spawning, sandboxes, and tools are host-owned. Building another provider runtime would add credentials, billing, execution, and supply-chain surface without improving the distinctive contract layer.

Eclipse v0.1 therefore owns vendor-neutral roles, contracts, evidence semantics, validation guidance, policy, adapters, and diagnostics. Codex, Copilot, compatible hosts, or humans own execution and workflow state. External provider execution is outside v0.1.

This keeps manual fallback complete and makes unsupported host capabilities explicit rather than simulated.
