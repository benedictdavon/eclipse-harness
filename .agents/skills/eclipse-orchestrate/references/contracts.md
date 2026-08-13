# Task contract construction

## Canonical identity

Bind every task to:

- `run_id`
- `plan_revision`
- `plan_digest`
- `provenance.base_revision`
- stable `task_id`

If architecture changes, revise the plan and supersede obsolete nonterminal tasks. Never ask a worker to finish a packet from the previous revision.

The host or user records which revision is current. Eclipse contract digests make stale packets detectable but do not create a workflow database.

## Minimum sufficient context

Include the objective, rationale, fixed decisions, assumptions, invariants, non-goals, referenced files/symbols, required capabilities, implementation guidance, and acceptance validation commands. Record each context reference's trust class.

Do not include full transcripts, unrelated repository documentation, raw logs, secret values, or the architect's discarded hypotheses.

## Acceptance and evidence

Give every criterion a stable ID and state what direct evidence is required. Make required validation commands explicit. A complete result is invalid when a criterion lacks satisfied evidence or a required command lacks passing evidence.

## Authorization

Set network, credentials, external effects, destructive actions, and permitted targets independently. Generic implementation authorization does not imply any of them.
