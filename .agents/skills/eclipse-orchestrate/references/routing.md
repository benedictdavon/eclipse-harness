# Routing and escalation

Route by role, capability, risk, complexity, cost tier, reasoning effort, tools, permissions, platform availability, and fallback behavior.

The Sol/Luna reference ladder is:

1. Use Luna medium for a tiny deterministic edit.
2. Use Luna high for normal bounded implementation.
3. Use Luna max only for a concrete, still-bounded local reasoning blocker.
4. Return architecture, interface, migration, concurrency design, security design, or scope decisions to Sol.
5. Return credentials, destructive effects, and new external authority to the human.

Do not buy more reasoning for missing context, broken tools, environment failures, unavailable credentials, permissions, or oversized logs. Repair the actual condition.

Distinguish requested, configured, effective, and verified model identity. If a task requires verified routing, do not dispatch until the host provides trusted observation; otherwise label the route policy-only or manual. Never claim a cost guarantee from configuration or agent self-report.

Keep review/fix loops within `max_review_rounds`. Convert bounded findings into correction contracts for the worker. Return architectural findings to the architect.
