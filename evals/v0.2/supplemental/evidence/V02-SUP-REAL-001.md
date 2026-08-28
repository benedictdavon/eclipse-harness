# V02-SUP-REAL-001 recorded role evidence

Repository pin: `itsdangerous` `672971d66a2ef9f85151e53283113f33d642dabd`.
Both supplied candidates and the final correction apply with `git apply --check`
to that commit.

## Baseline v0.1 review

- Round 1 rejected `num must be nonnegative`: the frozen contract requires the
  exact message `num must be non-negative`.
- Round 2 rejected deletion of the uint64 boundary parameter and the
  non-specific exception assertion.
- The final bounded correction restored the boundary and passed the frozen
  dependency-free behavior probe.

## Final v0.2 review

The final candidate bundle again found both predeclared regressions from patch
and test evidence, then accepted only the final patch. The reviewer was not an
independently verified oracle; the known-finding metric is recorded separately.

```text
$ python evals/v0.2/supplemental/probe_real.py V02-SUP-REAL-001 <candidate-source-root>
ECLIPSE_ACCEPTANCE_EVIDENCE: PASS
exit_code: 0
```
