# Host-owned failure handling

Eclipse classifies failures so the host or user can choose the correct action. It does not retry, resume, or persist recovery state.

| Failure | Guidance |
|---|---|
| Worker crash or incomplete result | Host retries within the task budget or delegates again. |
| Invalid or incomplete evidence | Return a bounded correction request. |
| Validation failure | Worker repairs within scope and attempt budget. |
| Stale plan or result | Reject it and issue a task from the current plan revision. |
| Missing dependency | Keep the task undispatched until dependencies complete. |
| Merge conflict | Host stops integration and resolves or re-plans. |
| Bounded review finding | Return a correction contract to a worker. |
| Architecture or scope conflict | Return to the architect. |
| New credentials, destructive action, or external authority | Require a human decision. |
| Requested model/capability unavailable | Use a documented fallback or manual mode; never claim parity. |

Hosts may store their own status, attempts, and artifacts. Eclipse requires only that the current task/result/review bindings remain explicit and that obsolete nonterminal tasks are not executed after a plan revision.
