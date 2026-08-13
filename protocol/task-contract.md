# Task Contract

A Task Contract is one bounded delegation unit. `schemas/task-contract.schema.json` is the wire format.

## Identity and freshness

`run_id`, `task_id`, `plan_revision`, `plan_digest`, dependencies, and `provenance.base_revision` bind the task to the host's current approved plan. When architecture changes, the architect issues a new revision and supersedes every obsolete nonterminal task. The host records which revision is current.

## Decisions and context

The packet includes a Context Manifest, fixed decisions, assumptions, invariants, non-goals, relevant files and symbols, required capabilities, and implementation instructions. Workers may make only local decisions permitted by those boundaries.

## Scope and concurrency

`scope` declares read/write/forbidden globs, shared interfaces, exclusive resources, parallel-safety intent, and requested isolation. Dependencies determine execution order. Pairwise ownership checks apply only to tasks in the same candidate wave. The host owns actual scheduling and isolation.

## Acceptance and validation

Each acceptance criterion has a stable ID and direct evidence requirement. `validation` lists the commands that contribute to acceptance. It is not a complete allowlist of every safe exploratory command a worker may use.

## Authority and budgets

Authorization for network, credentials, external effects, destructive actions, and targets is independent. Task budgets bound attempts and review rounds; the host tracks and applies them.

Stop conditions tell a worker when to return a blocker or escalation rather than improvise architecture or authority.
