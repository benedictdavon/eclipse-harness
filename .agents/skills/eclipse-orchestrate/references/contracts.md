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

The host transfers the approved identity values to every role. Copy them
verbatim. A contract digest is the SHA-256 digest of the canonical JSON object,
as defined by the protocol and optional validator; it is not a digest of a
Markdown wrapper or file bytes. If an identity or approved digest is missing or
contradictory, stop with a precise host/architect blocker instead of creating a
plausible value.

Use `executor` for the Task Contract's `execution_profile.role`. The skills may
call that role a worker in prose, but `worker` is not the contract wire literal.

## Minimum sufficient context

Include the objective, rationale, fixed decisions, assumptions, invariants, non-goals, referenced files/symbols, required capabilities, implementation guidance, and acceptance validation commands. Record each context reference's trust class.

Do not include full transcripts, unrelated repository documentation, raw logs, secret values, or the architect's discarded hypotheses.

Before handoff, remove facts the worker can obtain from an already named symbol,
schema field explanations, repeated policy prose, and duplicate natural-language
copies of the wire contract. Keep architecture summaries task-specific. The
contract is a transfer packet, not a research report.

## Acceptance and evidence

Give every criterion a stable ID and state what direct evidence is required. Make required validation commands explicit. A complete result is invalid when a criterion lacks satisfied evidence or a required command lacks passing evidence.

Separate required acceptance commands from optional probes. Set `mutating: true`
whenever a command can create bytecode, caches, snapshots, build products,
coverage data, generated code, or formatted files—even when those effects are
normally ignored by Git. State which generated outputs the host should attribute
to validation and which must remain absent from the product patch.

Require the host to give the worker an artifact destination outside the product
checkout, plus a clean pre-task status. Result contracts, review contracts, and
host logs are not implicitly authorized repository changes.

## Authorization

Set network, credentials, external effects, destructive actions, and permitted targets independently. Generic implementation authorization does not imply any of them.
