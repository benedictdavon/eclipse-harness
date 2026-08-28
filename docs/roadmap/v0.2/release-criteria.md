# v0.2 Release Criteria

| ID | Criterion | Status | Evidence |
|---|---|---|---|
| `02-G01` | 10 controlled fixture families implemented | Pass | 10 deterministic fixture directories; 2 frozen cases each |
| `02-G02` | At least 20 controlled cases executed | Pass | 20 baseline and 20 v0.2 terminal `run.json` records |
| `02-G03` | At least 5 real repositories tested | Pass | 5 repositories pinned to exact commits |
| `02-G04` | At least 30 real task runs | Pass | 30 baseline and 30 v0.2 qualifying terminal records |
| `02-G05` | All task-category minimums satisfied | Pass | Frozen distribution is 6/6/5/4/3/3/3 |
| `02-G06` | Zero open P0/P1 | **Fail** | `V02-FIX-09A/B` remain P1 evaluation-integrity gaps |
| `02-G07` | All baseline failures preserved/classified | Pass | No baseline case was removed; 5 comparisons are explicitly incomparable |
| `02-G08` | Frozen baseline rerun after fixes | Pass | Same 50 case IDs and frozen definitions were rerun |
| `02-G09` | Core skills remain useful without optional tooling | Pass | All role flows are documented as portable skill/contract handoffs |

The release is ineligible while a mandatory item is failed or blocked.
Therefore this branch is evidence-complete for the executed campaign but is not
eligible to be declared a completed v0.2 release.
