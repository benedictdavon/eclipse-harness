# ADR 0002: Machine-readable canonical state

Status: accepted for v0.1

The prior workflow used multiple mutable Markdown files for task state and handoff. That created drift and required probabilistic agents to maintain deterministic bookkeeping.

Eclipse uses versioned JSON contracts and `.eclipse/runs/<id>/run.json` as canonical state. Markdown plans/handoffs are generated projections. State transitions, plan revisions, evidence completeness, ownership, and digests are validated by code.

The cost is a formal schema and migration obligation. The benefit is deterministic stale-work rejection, recovery, interoperability, and no contradictory canonical views.
