# Architecture

## Principle

Use expensive reasoning where judgment changes the outcome. Encode that judgment in explicit contracts. Delegate bounded execution to the most economical capable worker. Require evidence rather than trust. Reintroduce stronger reasoning at decision boundaries and independent review.

Eclipse began as `Sol + Luna -> Eclipse`, but its core semantics are provider-neutral. Model names live in policies and adapters.

## Skills-first layers

1. **Skills** define architect, executor, reviewer, bootstrap, and diagnostic behavior through progressive disclosure.
2. **Protocol** defines task, context, result, review, and routing semantics in human-readable documents and JSON Schemas.
3. **Policies** map vendor-neutral roles and capabilities to preferences such as the Sol/Luna reference ladder.
4. **Adapters** express those preferences using host-supported files and document native, emulated, manual, or unsupported capabilities.
5. **Evals** test role behavior and contract quality without claiming live benchmark results.
6. **Optional tools** validate contracts, DAG waves, adapter output, capability snapshots, and recorded eval cases.

## Ownership boundary

Eclipse owns guidance and protocol semantics. It does not own execution.

The host or user owns:

- model calls and agent/subagent spawning;
- filesystem writes and command execution;
- git branches, worktrees, merges, and conflict handling;
- sandbox and permission enforcement;
- scheduling, retries, cancellation, and recovery;
- storage of the current plan revision and workflow status.

The optional Python package has no daemon, run database, lock manager, worktree engine, journal, or provider executor.

## Contract flow

The architect returns an approved plan revision, task contracts, and execution waves. The host delegates a current task to a worker. The worker returns a result contract. The host assembles the original requirement, current plan, task, result, actual diff, and validation evidence for an independent reviewer.

Task lifecycle names and transition checks are protocol vocabulary. The small in-memory helper in `state.py` can validate plan-revision semantics, but it is not canonical state and performs no I/O.

## Portability boundary

Portable semantics include role responsibilities, contracts, stale-plan binding, evidence, routing intent, escalation, safe-wave guidance, and review outcomes.

Host-specific behavior includes actual model selection, effective reasoning effort, subagent topology, tool access, filesystem isolation, and permission enforcement. Adapter configuration is intent until the host proves the effective setting.
