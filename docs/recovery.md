# Failure and recovery

Failures are classified rather than retried uniformly.

| Failure | Default response |
|---|---|
| Worker crash/incomplete result | Resume or start another attempt within budget. |
| Invalid/incomplete evidence | Reject result; worker corrects within scope. |
| Validation failure | Worker repairs within attempt budget. |
| Stale plan/result | Reject and re-plan; do not integrate old work. |
| Missing dependency | Keep task planned/blocked until dependency accepts. |
| Merge conflict | Stop integration; resolve deterministically or re-plan. |
| Review finding | Bounded correction, architect escalation, or human boundary by type. |
| Budget exhausted | Architect decides decomposition/route/human action. |
| Requested model unavailable | Fallback only as configured and explicitly labelled. |
| Host capability unavailable | Policy-only/manual mode or fail closed. |
| Corrupt state/digest mismatch | Stop and reconstruct only from immutable trusted artifacts. |

The CLI never silently converts a failure into retry or model upgrade. Resume uses the canonical state, immutable contract files, attempt numbers, digests, and event history. Never edit generated plan/handoff files as a recovery mechanism.
