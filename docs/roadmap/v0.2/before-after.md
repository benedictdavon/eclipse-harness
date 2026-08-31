# v0.2 Candidate Before/After Evaluation

## Comparison basis

The original campaign uses the unchanged frozen definitions in `evals/v0.2/`:
the same prompts, task wording, criteria, policy, host configuration, and
pinned commits. Its baseline is `v0.1.0-alpha.1` at
`8a674fafe1f1d03c34e27c7a875752a0138f5e2b`.

The final candidate is evaluated with one post-fix skill revision. Its full,
public SHA is recorded in `release-evidence.md` and in every final-candidate
record; the corpus schema rejects shortened revisions. The separate
supplemental campaign is frozen in `evals/v0.2/supplemental/` and was also run
against both v0.1 and that same final candidate.

The original five flawed cases remain intact and incomparable:
`V02-FIX-09A/B`, `V02-REAL-018`, `V02-REAL-024`, and `V02-REAL-030`. They do
not satisfy correction-loop or real review/correction category requirements.

## Evidence-derived aggregate results

The scorer reads terminal outcome, authorization/acceptance checks, and the
recorded evidence artifact. It intentionally ignores the legacy
`metrics.task_success` and `metrics.acceptance_success` flags.

| Measure | v0.1 baseline | final candidate | Change |
|---|---:|---:|---:|
| Executed terminal records | 55 | 55 | 0 |
| Evidence-supported outcomes | 5 | 8 | +3 |
| Original campaign, evidence-supported | 0/50 | 3/50 | +3 |
| Supplemental correction cases | 5/5 | 5/5 | 0 |
| Structural-only real acceptance claims | 4 | 18 | +14 classified inconclusive |
| Acceptance evidence unavailable/inconclusive | 5 | 21 | +16 classified honestly |
| Predeclared expected findings missed | 0 | 0 | 0 |
| Unknown reviewer misses | unavailable | unavailable | not inferred |
| Supplemental correction cycles | 10 | 10 | 0 |
| Measured token/cost records | 0 | 0 | unavailable |

The three deliberately unauthorized controlled candidates remain detected.
No real candidate with an observed out-of-scope change was accepted. The two
supplemental non-convergence loops reached the declared two-review-round bound
and escalated instead of silently continuing.

## Category and case status

| Classification | Count | Cases |
|---|---:|---|
| Valid supplemental repeated correction | 2 | `V02-SUP-FIX-01/02` |
| Valid supplemental real review/correction | 3 | `V02-SUP-REAL-001/002/003` |
| Regressed evidence-supported behavior | 0 | None observed |
| Preserved invalid/incomparable original cases | 5 | `V02-FIX-09A/B`, `V02-REAL-018`, `024`, `030` |

The 30 qualifying real-run requirement is now supported by 27 valid original
real runs plus the 3 supplemental real correction runs. The frozen task-category
minimum is satisfied only with those supplemental records; the three original
unseeded review/correction cases are explicitly excluded from the count.

## Evidence-backed effects and limits

- Canonical identity, host-proven patch/status evidence, required-versus-
  supplemental validation, compact task context, and architecture review remain
  the only production skill changes attributed to the original baseline.
- `V02-REAL-014` now has a dependency-free Node probe that executes the
  recorded candidate's retry-normalization behavior. Other real candidates
  whose frozen commands merely compile files or assert non-empty content are
  not scored as behavioral successes.
- Every run record is schema-validated; all final records name one full,
  reachable candidate SHA. Unknown reviewer misses are null. Only the narrower
  `predeclared_expected_findings_missed` metric is zero where a fixed oracle
  exists.
- The host exposed no token/cost telemetry, so quality-adjusted cost is not
  calculated. Reviewer/evaluator mechanical isolation remains unverified; this
  is reported as a limitation rather than a zero-miss claim.
