# ADR 0004: Skills-first product with host-owned execution

Status: accepted for v0.1

## Original implementation

The first PR implemented a canonical run store, lifecycle ingestion, interprocess locking, event journaling, generated plan/handoff views, recovery behavior, a worktree manager, a legacy migration runtime, usage utilities, and a broad runtime-oriented configuration.

## Issue

Those components made Eclipse responsible for workflow execution infrastructure even though the product's portable value is its skills, contracts, policy, adapters, and evals. They also made the core skills depend on Python commands and exposed configuration fields that did not consistently control behavior.

## Decision

Eclipse v0.1 is skills-first. The host or user owns agent execution, workflow state, filesystem mutation, git, sandboxing, scheduling, retry/recovery, and integration.

The Python package is optional and limited to:

- contract and security validation;
- pure plan-revision lifecycle semantics;
- dependency DAG and execution-wave checks;
- routing-policy evaluation;
- adapter generation and host-specific diagnostics;
- deterministic evaluation aggregation.

Canonical run persistence, locking, journals, generated workflow views, worktree operations, runtime migration, and the broad `.eclipse/config.json` are removed.

## Consequences

The skills remain substantially usable without Python. Hosts may store workflow state in their own native systems. Eclipse cannot automatically resume or schedule work, but it no longer claims runtime responsibilities or enforcement it does not control.
