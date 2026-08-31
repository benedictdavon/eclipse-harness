# v0.2 Candidate Release Criteria

| ID | Criterion | Status | Evidence |
|---|---|---|---|
| `02-G01` | 10 controlled fixture families exist | Pass | 20 original frozen controlled cases across 10 families |
| `02-G02` | At least 20 controlled cases are executed | Pass | 20 original pairs plus 2 frozen supplemental correction loops |
| `02-G03` | At least 5 real repositories are evaluated | Pass | 5 original repositories pinned to exact commits |
| `02-G04` | At least 30 qualifying real task runs | Pass | 27 valid original real runs + 3 supplemental real correction runs, in each phase |
| `02-G05` | All task-category minimums are satisfied | Pass | 6/6/5/4/3/3 original coverage plus 3 valid supplemental review/correction runs |
| `02-G06` | Zero open P0/P1 evaluation-integrity issues | Pass | Frozen P1 correction-case defect is preserved but closed by the separately frozen executable supplement |
| `02-G07` | Baseline failures are preserved and classified | Pass | Original five flawed cases remain present and explicitly incomparable |
| `02-G08` | Frozen campaigns rerun after fixes | Pass | 55 baseline and 55 final-candidate schema-valid terminal records |
| `02-G09` | Core skills work without optional tooling | Pass | Portable skill/contract handoffs remain the primary workflow |
| `02-G10` | Evidence records are auditable | Pass | Full-corpus run-record schema gate, full reachable skill SHAs, raw-evidence scorer, and freeze hashes |

All implementation evidence gates are satisfied. This branch remains a
**v0.2 candidate/draft** until the draft PR receives a new review; no release
or merge is implied by these gate results.
