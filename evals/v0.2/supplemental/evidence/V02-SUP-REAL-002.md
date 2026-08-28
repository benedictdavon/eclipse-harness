# V02-SUP-REAL-002 recorded role evidence

Repository pin: `itsdangerous` `672971d66a2ef9f85151e53283113f33d642dabd`.
Each candidate patch and the final correction applies cleanly to the pinned
checkout.

## Baseline v0.1 review

- Round 1 rejected silent truncation of a nine-byte input.
- Round 2 rejected `ValueError("too long")` and its generic assertion because
  the precise public error contract remained unverified.
- The final candidate used the exact message and preserved the normal uint64
  conversion behavior.

## Final v0.2 review

The final candidate review produced all three predeclared findings (truncation,
wrong message, weak assertion) before accepting the final patch.

```text
$ python evals/v0.2/supplemental/probe_real.py V02-SUP-REAL-002 <candidate-source-root>
ECLIPSE_ACCEPTANCE_EVIDENCE: PASS
exit_code: 0
```
