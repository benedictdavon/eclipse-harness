# Architecture

## Principle

Use expensive reasoning where judgment changes the outcome. Encode that judgment in explicit contracts. Delegate bounded execution to the most economical capable worker. Require evidence rather than trust. Reintroduce stronger reasoning at decision boundaries and independent review.

Eclipse's origin is `Sol + Luna → Eclipse`, but its core roles are `architect`, `executor`, `reviewer`, and `doctor`. Model/provider identity belongs to policy and adapters.

## Layers

The vendor-neutral core owns contracts, state transitions, routing abstractions, authorization, validation, evidence, recovery, concurrency, usage representation, and evaluation records.

The Sol/Luna policy maps those abstractions to a reference cost/quality strategy. It can be replaced by a homogeneous model policy, human architect policy, another provider policy, or host-default policy without changing task contracts.

Adapters translate role intent into current host files. They are generated outputs, not the semantic source of truth. Host runtimes still own model execution, spawning, tools, sandbox enforcement, and context behavior.

Skills under `.agents/skills` express the portable operational workflow with progressive disclosure.

## State ownership

- Root/CLI: persists and transitions run state.
- Architect: returns plan/task candidates; read-only.
- Executor: writes only contract-owned implementation paths; never run state.
- Reviewer: read-only; returns findings and verdicts.
- Doctor: non-destructive environment/configuration inspection.

Only `.eclipse/runs/<run-id>/run.json` is canonical runtime state. Task/result/review contracts are immutable evidence artifacts referenced by that state. `ACTIVE_PLAN.md` and `HANDOFF.md` are generated projections.

## Lifecycle

Tasks move through explicit states. A typical success path is:

`planned → ready → running → evidence_pending → review_pending → accepted`

A correction path is:

`review_pending → changes_requested → ready_for_correction → running`

Blocked work may become ready again, escalate, or fail. A plan revision supersedes obsolete nonterminal tasks. Invalid transitions raise deterministic errors.

## Protocol boundary

Eclipse validates contracts and prepares safe execution/review packets. It does not autonomously call provider APIs in v0.1. A host-native agent, CLI invocation, or human transfers the contract and returns evidence. This keeps the protocol useful when native subagents are unavailable.
