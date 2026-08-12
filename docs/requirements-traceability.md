# v0.1 requirements traceability

This checklist maps the supplied research/design plan to implementation. The research recommended a protocol-and-skill suite, not a provider runtime.

| Research requirement | v0.1 disposition |
|---|---|
| Portable `.agents/skills` source | Implemented: four Eclipse skills with one-level references. |
| Vendor-neutral protocol | Implemented in `contracts`, `state`, `routing`, `authorization`, `concurrency`, `security`, `usage`, and `evaluation`. |
| Sol/Luna reference strategy | Implemented as `policies/sol-luna.json`; no core model coupling. |
| Task/result schemas and validators | Implemented with JSON Schemas, typed models, digests, and semantic validation. |
| Independent structured review | Implemented with review schema/model, read-only intent, verdicts/findings, and bounded rounds. |
| Requested/configured/effective identity | Implemented; effective requires host-observed source. |
| Codex model-inheritance detection | Implemented through observed route mismatch in doctor; live probe requires host metadata. |
| Plan revision/stale result prevention | Implemented through revision/digest binding and superseded states. |
| Canonical run state/generated views | Implemented with atomic JSON state, event log, renderer, and ignored runtime data. |
| DAG and parallel ownership | Implemented with dependency cycles, glob overlap, interfaces, exclusive resources, isolation, and waves. |
| Git/worktree isolation | Implemented for explicit task worktree preparation and merge/conflict primitives. |
| Security/trust boundaries | Implemented/documented: trust classes, secrets/redaction, bounded paths/symlinks, command classification, least privilege, human boundaries. |
| Recovery/failure classification | Implemented in states, store validation, budgets, escalation taxonomy, and recovery docs. |
| Cost/usage instrumentation | Implemented as measured/estimated/unavailable records; no invented prices. |
| Codex adapter | Implemented against verified current official fields and limitations. |
| Copilot adapter | Implemented with current agent profile/tool syntax and explicit degraded parity. |
| Generic/manual fallback | Implemented/documented. |
| Doctor | Implemented for host, versions, skills, profiles, recursion, concurrency, desired/effective permissions, git/worktrees, and route mismatches. |
| Configuration/CLI/bootstrap | Implemented with strict JSON config, stable commands/exit behavior, dry-run/idempotent adapter installation. |
| soluna-workflow migration | Implemented conservatively with dry-run/report and no destructive source edits. |
| Observability | Implemented with structured state/events, routing rationale primitives, attempts/reviews/escalations, validation, and usage. |
| Evaluation/benchmarks | Methodology, runner, fixtures, and result schemas implemented; live conclusions deliberately absent. |
| CI/cross-platform | Implemented for Python 3.10+ on Linux, Windows, and macOS plus security/adapter checks. |
| External providers/credentials, GUI, autopilot, general team runtime | Explicitly outside researched v0.1 boundary. |
| Optional Codex-Orchestration/Rune adapters | Research priority P2; documented interoperability, deferred beyond v0.1. |

No material v0.1 architecture deviation was required. Product naming and canonical runtime directory changed from the research placeholder (`Soluna`/`.soluna`) to the approved `Eclipse`/`.eclipse` naming without changing semantics.
