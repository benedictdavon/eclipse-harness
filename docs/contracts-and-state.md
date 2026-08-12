# Contracts and state

## Task contract

The task contract binds one executable objective to an approved plan revision and base commit. It carries decisions, context references and trust classes, invariants, non-goals, capabilities, routing intent, write/forbidden scope, interface/resources, isolation, criteria, validation, evidence expectations, stop conditions, risk/complexity, budgets, authorization, and provenance.

JSON is canonical. Markdown is never parsed as the protocol. Validate with:

```bash
eclipse validate task.json --kind task
```

## Result contract

A worker result records exact changed files, implementation summary, local decisions, commands/exits/outcomes, criterion evidence, blockers, deviations, risks, escalation, git identifiers, timestamps, and usage quality.

A `complete` result is rejected unless every acceptance criterion has satisfied evidence and every required validation command has passing evidence. It is also rejected for stale plan/task digests or unauthorized files.

Requested, configured, and effective model identity are separate. Worker/reviewer JSON cannot
self-attest `host-observed`; trusted host identity belongs in a separate authenticated envelope.

## Review contract

Review binds to the same task and the exact result digest. It records desired/effective permission status, criterion verdicts, validation analysis, structured findings, outcome, and residual risk.

An accepted review requires no findings and a satisfied verdict for every criterion. Findings are classified as bounded correction, architecture escalation, invalid contract, insufficient evidence, acceptance failure, security concern, or unauthorized change.

## Revision and recovery

Every task, result, and review carries the plan revision/digest. Revising the plan increments the revision and supersedes active old tasks. An obsolete result is rejected even if its prose says it is complete.

State writes are atomic. Loading validates schema, task map identity, dependency references, and contract digests. Events append to `events.jsonl` with secret redaction. Corrupted or incomplete state fails closed; repair it from immutable contracts/evidence or require human intervention rather than guessing.

Every state transition is serialized with a per-run interprocess lock. Contracts, results, reviews,
and approval attestations use create-only evidence files. Result ingestion derives changed paths
from the task's full Git base revision (or requires an explicit trusted root observation outside a
Git worktree) and requires exact equality with the worker report. Accepted review ingestion is a
separate root-authority action requiring an explicit human or authenticated-host attestation;
review JSON cannot attest itself.

## Schema compatibility

Package, configuration, contract, state, capability, policy, and evaluation versions are explicit. Patch releases do not break existing schemas. Optional fields may be introduced in compatible minor evolution; required/semantic breakage requires a major schema migration.
