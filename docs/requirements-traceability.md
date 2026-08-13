# v0.1 requirements traceability

| Requirement | v0.1 disposition |
|---|---|
| Skills-first product | Implemented: core workflow remains usable from `.agents/skills` and `protocol/` without Python. |
| Architect/executor/reviewer separation | Preserved in focused skills and host wrappers. |
| Bootstrap and diagnostics | Implemented as portable setup guidance plus optional host-specific doctor checks. |
| Task/context/result/review contracts | Implemented as JSON Schemas, Python validators, examples, and protocol documents. |
| Plan revision and stale work | Implemented through contract bindings and pure lifecycle semantics; the host owns current state. All nonterminal states can be superseded. |
| Dependency DAG and concurrency | DAG validation, wave construction, and same-wave ownership checks are separate. |
| Command evidence consistency | `passed/failed/not-run` is bound to `0/non-zero/null` exit codes in schema and Python validation. |
| Exploration command semantics | Additional bounded commands are allowed; acceptance commands remain required and sensitive commands remain authorized/disclosed. |
| Sol/Luna policy | Implemented as a consumed reference policy; core roles contain no provider identity. |
| Requested/configured/effective identity | Preserved; effective identity requires trusted host observation. |
| Codex adapter | Generated current role/config intent with honest host/runtime limitations. |
| Copilot adapter | Generated host-default profiles with no false model parity. |
| Manual fallback | Complete contract-transfer workflow documented. |
| Doctor isolation | Codex and Copilot profile/permission diagnostics are independent. |
| Configuration surface | Broad runtime configuration removed; every retained CLI flag/policy input has a direct consumer and tests. |
| Security boundaries | Trust classes, path scope, authorization, secret checks, command classification, and host-enforcement limits retained. |
| Evals | Recorded deterministic cases and methodology retained without fabricated conclusions. |
| CI/cross-platform | Python 3.10–3.14 and Linux/macOS/Windows matrix retained. |
| Runtime engine, canonical run state, journal, locks, scheduler | Removed/deferred; host-owned. |
| Worktree/git manager | Removed/deferred; host-owned. |
| Migration runtime | Removed/deferred; manual compatibility guidance remains. |
| Event/usage store | Removed; usage quality remains contract/evaluation data. |
