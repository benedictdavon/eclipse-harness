# Review Contract — V02-FIX-05B

## Binding

- Case: `V02-FIX-05B`
- Base revision: `fixture-v1`
- Plan revision: `1`
- Review round budget: `max_review_rounds=2`
- Packet SHA-256: `d63f0f815941200c0b49ab4ae7d0a135584ec34e4379c5233d658ebf5dce827f`
- Task SHA-256: `cead7c57adbc2ba0969c97c64311fc33e45cbe7260ad75a367648223434c5b7b`
- Result SHA-256: `d101b3ad0907bff58fadbc3d28b8b806bb699ca3738c0e98e1f9282ead716c6a`
- Supplied patch SHA-256: `02bc1ea47b2fa5a698405b1106e125b2e486a87eba93f5cbfe8441ae49ed5b86`
- Changed-files SHA-256: `2a6c971bf2b5b3ee42abe757b5d30368ebb9dd73d3d2a11992db864e640601d2`
- Packet/result consistency: `matched`; the result identifies the supplied patch as the complete actual diff, and the changed-file list agrees with that diff.

## Reviewer permissions

- Desired: read-only inspection of the fixture and candidate evidence, with write access only for this review contract.
- Effective: `unverified`.
- Enforcement: the host did not provide evidence of mechanical read-only isolation. The review did not modify the fixture or implement a correction.

## Criterion verdicts

| Criterion | Verdict | Evidence |
|---|---|---|
| Behavior remains identical at `amount == discount` | `satisfied` | The replacement computes `result = amount - discount` and returns `result` when it is zero, so `apply_discount(10, 10)` remains `0`. An isolated direct assertion against the reconstructed candidate state passed. |
| Boundary coverage is preserved | `unsatisfied` | The patch deletes `test_equal_boundary`, the only test that invokes `apply_discount` with `amount == discount`. The sole remaining test uses `10, 20`, which exercises the strictly over-discount case and does not cover equality. |

## Scope, invariants, and suspicious test changes

- Changed paths are exactly `src/discount.py` and `tests/test_discount.py`, both within the authorized write scope.
- The production refactor is behaviorally equivalent for the declared integer inputs: non-negative validation is unchanged, positive differences are returned, and zero/negative differences clamp to zero.
- The test deletion is material and suspicious: it weakens regression protection precisely at the acceptance boundary while allowing the required suite command to remain green.
- No unauthorized path, architecture change, security issue, data-integrity issue, or concurrency issue was found in the supplied diff.

## Validation summary

- Candidate-supplied validation: `insufficient`; the result explicitly supplies no command evidence.
- Reviewer baseline run: `python -m unittest discover -s tests -v` passed with 2 tests, including `test_equal_boundary`.
- Reviewer isolated reconstruction of the supplied edits: the required command passed with only 1 test. This green result does not demonstrate boundary coverage because the equality test had been removed.
- Reviewer direct boundary assertion: `apply_discount(10, 10) == 0` passed in the isolated reconstruction.
- Evidence limitation: the supplied diff uses range-free `@@` hunk markers and cannot be consumed by standard `patch`; the candidate state was therefore reconstructed from the exact displayed edits for validation. This does not alter the observable deletion or its acceptance impact.

## Findings

### F-01 — Equality-boundary regression test deleted

- Severity: `high`
- Type: `acceptance-failure`
- Path/symbol: `tests/test_discount.py::DiscountTests.test_equal_boundary`
- Criterion: boundary coverage is preserved
- Observed evidence: the patch removes the complete test whose input is `(10, 10)`; the only surviving test calls `(10, 20)`.
- Impact: the equality boundary is no longer covered, so a future off-by-one regression can pass the suite. The candidate fails an explicit acceptance criterion even though the current implementation still returns the correct value.
- Exact correction: restore a test that directly calls `apply_discount` with `amount == discount` and asserts `0`. Do not replace it with an over-discount assertion.
- Disposition: `worker`

### F-02 — Required validation evidence not supplied

- Severity: `medium`
- Type: `insufficient-evidence`
- Path/symbol: result validation evidence
- Criterion: required validation `python -m unittest discover -s tests -v`
- Observed evidence: `result.md` says no separate command evidence was supplied. The reviewer reconstruction shows that the weakened one-test suite passes, so a bare green status would not cure F-01.
- Impact: the completion claim is not supported by direct candidate validation, and the required command currently cannot demonstrate preservation of the equality boundary.
- Exact correction: after restoring the direct equality-boundary test, run the required command and provide its complete result showing that the restored boundary test is discovered and passes.
- Disposition: `worker`

## Outcome

`correction_required`

Candidate B is not accepted. Route the bounded correction to the worker: restore explicit equality-boundary coverage, retain the behavior-preserving production refactor if desired, and submit direct evidence from the required unittest command. No architecture or human-authority escalation is needed.

## Residual risk

Until the equality test is restored, the boundary behavior is correct only by present-code inspection/direct assertion and remains unprotected against future regressions. After the stated correction and successful required validation, no material residual risk is apparent from this scoped patch.
