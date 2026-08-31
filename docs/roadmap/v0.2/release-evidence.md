# v0.2 Candidate Release Evidence

## Auditable chronology

This draft deliberately preserves an inspectable sequence rather than placing
the definition, baseline, changes, and rerun in one commit. All hashes below
are full, reachable Git objects in this draft branch (apart from the immutable
v0.1 tag).

| Stage | Public commit |
|---|---|
| v0.1 baseline tag | `8a674fafe1f1d03c34e27c7a875752a0138f5e2b` (`v0.1.0-alpha.1`) |
| Freeze original campaign | `598ce8325737e0e80acd96bf4e5b30aee772bef6` |
| Preserve original v0.1 baseline | `b765221b0fc7e4e07bae7e81942ca312ced19ab1` |
| Freeze supplemental correction campaign | `0286cad8f889cba4f02f6e01aca5d7b13d5655a4` |
| Preserve supplemental v0.1 baseline | `0db5c5c0291dde803b5e158415b4f632bf7d7a53` |
| Classify findings | `84415a4317c5ce1c22d201aeda132dd4bceeccd3` |
| Harden skills and evidence validation | `4438280c502e1e0d9e667e841206cc19b8e6521e` |

The final rerun records all name the last hash as `skill_commit`; the
run-record schema requires 40 hexadecimal characters. The branch history adds
the rerun and this evidence publication after that commit. The original freeze
manifest and supplemental freeze manifest store SHA-256 content hashes for
their definitions and candidate patches.

## Campaign and score

The original campaign remains frozen: 20 controlled cases in 10 fixture
families and 30 tasks across 5 repositories pinned to exact commits. Five
original cases remain flawed and incomparable: `V02-FIX-09A/B`,
`V02-REAL-018`, `V02-REAL-024`, and `V02-REAL-030`. They are preserved but
explicitly excluded from the correction/review category count.

The separately frozen supplement provides two executable repeated-correction
loops and three executable real `review-correction` cases, with two
patch-applicable candidate states per case and both v0.1 and final-candidate
records. The three real supplemental cases bring the valid real-run total to
30 (27 valid original runs plus 3 supplement runs).

`tools/score_v02_campaign.py` derives its aggregate from terminal state,
authorization/acceptance checks, and evidence artifacts. It does not trust
pre-populated task or acceptance success booleans. Across the combined corpus,
evidence-supported outcomes rise from 5/55 on v0.1 to 8/55 on the final
candidate. The 18 structural-only and 21 unavailable/inconclusive final
acceptance claims are not counted as behavioral successes. `V02-REAL-014` has
a dependency-free Node behavioral probe; other file-existence/compile-only
claims are scored conservatively.

Every one of the 110 `run.json` records is validated by the run-record JSON
Schema in the test suite. Supplemental task contracts, patch-bound worker
results, changed-file digests, and validation transcripts are checked against
the frozen cases and patches. Unknown reviewer misses are `null` because reviewer
independence is unverified. The narrower
`predeclared_expected_findings_missed` is zero only for cases with a fixed
oracle.

## Product and release boundary

The changes retain Eclipse as skills, portable contracts, reference policy,
adapters, evals, and optional validators. The host still owns execution,
filesystem mutation, git, sandboxing, scheduling, workflow state, retries,
dependency installation, and integration. No workflow engine or runtime state
infrastructure has been introduced.

All implementation evidence gates in `release-criteria.md` are satisfied, but
this remains a **v0.2 candidate/draft** pending this PR's next review. It is
not a merge or release declaration.

## Validation

The final local gate records the complete unit/integration/E2E suite, Ruff,
strict Mypy, JSON Schema and skill validation, security authorization tests,
adapter drift, self-check, packaging/resource audit, and clean-wheel bootstrap.
GitHub Actions run `33411078132` completed successfully for this draft after
the supplemental-evidence binding repair. Any later evidence-only documentation
commit receives its own PR check; the observed outcome belongs in the PR checks,
not in a fabricated release claim.
