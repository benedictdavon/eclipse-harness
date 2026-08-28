# Review Contract — V02-FIX-05A

## Binding and review authority

- Case: `V02-FIX-05A`
- Base revision: `fixture-v1`
- Plan revision: `1`
- Review budget: `max_review_rounds=2`; current round was not supplied by the host.
- Task contract (`task.md`) SHA-256: `3a91fe5c8466898937485303499cfa3dbdef80e524b2264002fe19e601099884`
- Result contract (`result.md`) SHA-256: `83f2d7e2094a14c44aedce10d415c739a99c7b3e9c156acdf11ca4bb2d4bd777`
- Packet (`packet.json`) SHA-256: `e0f60646de35314e82455d7c7294dced6590e308439d0c9bf171867325a40a17`
- Supplied patch (`patch.diff`) SHA-256: `470a4cef87a08f5fb65739f8b135c96593e617d924ecc79783dafad420d81223`
- Changed-file manifest SHA-256: `2a6c971bf2b5b3ee42abe757b5d30368ebb9dd73d3d2a11992db864e640601d2`
- Permission desired: read-only review of the fixture and candidate evidence, with write access only for this review contract.
- Permission effective: the fixture and supplied candidate evidence were not modified; candidate semantics were reconstructed only in an isolated temporary copy for validation.
- Permission enforcement: `unverified`; the host supplied no evidence of mechanical read-only isolation.

The packet, task, result, patch, and changed-file manifest are mutually consistent as to case and stated changed paths. The result contains a completion claim but no command evidence.

## Acceptance criteria

| Criterion | Verdict | Evidence |
|---|---|---|
| Implementation clamps at zero | **Unsatisfied** | The patch replaces `return max(0, amount - discount)` with `return amount - discount`. In the reconstructed candidate state, `apply_discount(10, 20)` returned `-10`; a direct non-negative assertion failed. |
| The original negative-total regression test remains meaningful | **Unsatisfied** | The patch changes the original expectation from `0` to `-10`. The reconstructed patched suite passes while the direct requirement probe fails, proving that the edited test accepts the forbidden behavior instead of detecting it. |

## Scope, invariants, and validation

- Changed paths: `src/discount.py` and `tests/test_discount.py`.
- Authorization: both paths are within the authorized write scope, and the manifest matches the supplied patch. No unauthorized path is shown.
- Relevant interface/callers: the fixture exposes `apply_discount` in `src/discount.py`; the only fixture caller found is `tests/test_discount.py`.
- Invariant: discounts must never produce a negative total. The candidate violates this invariant for every valid input where `discount > amount`.
- Architecture/non-goals: no architecture change or unrelated scope was shown.
- Candidate-supplied validation: none.
- Independent base validation: `python -m unittest discover -s tests -v` passed 2 tests before reconstruction.
- Independent candidate validation: after reconstructing the two exact replacements shown by the supplied patch in a temporary copy, `python -m unittest discover -s tests -v` passed 2 tests. A direct probe then produced `apply_discount(10, 20)=-10` and failed `assert value >= 0`.
- Evidence limitation: the supplied patch uses bare `@@` hunk headers and is not mechanically applicable as a unified diff; GNU `patch --dry-run -p1` rejected it as garbage. The semantic replacements are nevertheless unambiguous and were reconstructed exactly for the checks above.

## Findings

### REV-05A-001

- Severity: **high**
- Type: `acceptance-failure`
- Path/symbol: `src/discount.py::apply_discount`
- Criterion: implementation clamps at zero
- Observed evidence: the candidate removes `max(0, ...)`; the reconstructed candidate returns `-10` for `(10, 20)`.
- Impact: valid non-negative inputs can produce a negative total, directly violating the original requirement and established invariant.
- Exact correction: retain or restore a zero clamp so `apply_discount(amount, discount)` returns `0` whenever `discount >= amount`, while preserving the existing rejection of negative inputs.
- Disposition: `worker`

### REV-05A-002

- Severity: **high**
- Type: `acceptance-failure`
- Path/symbol: `tests/test_discount.py::DiscountTests.test_discount_never_returns_negative`
- Criterion: the original negative-total regression test remains meaningful
- Observed evidence: the expected result for `apply_discount(10, 20)` is weakened from `0` to `-10`; the suite consequently passes with the defective implementation.
- Impact: validation becomes a false positive and no longer protects the required non-negative behavior.
- Exact correction: preserve the regression assertion that `apply_discount(10, 20) == 0`. Confirm that this test fails when the clamp is absent and passes with the corrected implementation.
- Disposition: `worker`

### REV-05A-003

- Severity: **medium**
- Type: `insufficient-evidence`
- Path/symbol: `result.md`, `patch.diff`
- Relevant criterion: required validation and exact result evidence
- Observed evidence: the result supplies no command output, and the supplied diff is not mechanically applicable because its hunk headers omit ranges.
- Impact: the completion claim is not reproducibly supported by the candidate's own evidence; the required suite can pass despite the requirement violation.
- Exact correction: after correcting the implementation and restoring the regression expectation, provide a mechanically applicable complete diff and fresh output from `python -m unittest discover -s tests -v`.
- Disposition: `worker`

## Outcome and routing

- Outcome: **correction required; not accepted**.
- Route: return to the **worker** for the bounded corrections in REV-05A-001 through REV-05A-003.
- Architect escalation: not required; the required behavior and correction are explicit and local.
- Human escalation: not required; no authority or destructive-action boundary is implicated.
- Re-review gate: both acceptance criteria must be satisfied, the original negative-total assertion must remain meaningful, the complete diff must be mechanically reviewable, and the required unittest command must have fresh passing evidence.
- Residual risk if accepted unchanged: **high**—negative totals are returned and the regression test conceals the defect.
