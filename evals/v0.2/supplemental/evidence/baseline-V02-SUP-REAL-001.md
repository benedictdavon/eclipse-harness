# V02-SUP-REAL-001 baseline evidence

Against pinned `itsdangerous` `672971d66a2ef9f85151e53283113f33d642dabd`,
the frozen v0.1 reviewer rejected the wrong negative-input message in round 1
and the removed uint64 boundary plus non-specific assertion in round 2. It
accepted only the bounded final correction.

```text
$ python evals/v0.2/supplemental/probe_real.py V02-SUP-REAL-001 <candidate-source-root>
ECLIPSE_ACCEPTANCE_EVIDENCE: PASS
exit_code: 0
```
