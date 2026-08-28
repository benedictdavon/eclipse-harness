# V02-SUP-FIX-01 recorded role evidence

The frozen candidates apply to `controlled/fixtures/repeated-correction-loop`
at `fixture-v1`. The host supplied both patches and ran the declared unittest
command after each application.

## Baseline v0.1 review

- Round 1 rejected `candidate-round-1.patch`: attempt 3 returns `3`, not `4`.
- Round 2 rejected `candidate-round-2.patch`: the `attempt > 8` guard is gone.
- The reviewer made no third dispatch. The host recorded an architect escalation
  at the fixed two-round budget.

## Final v0.2 review

- Round 1 identified the same wrong third retry value from actual patch evidence.
- Round 2 identified the missing upper-bound invariant and required test.
- The final outcome was an architect escalation after exactly two rejected
  corrections; no worker was given a third correction cycle.

`predeclared_expected_findings_missed` is zero for this fixed oracle. Reviewer
independence is still unverified, so `reviewer_misses` is unavailable rather
than asserted to be zero.
