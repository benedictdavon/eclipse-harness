# V02-SUP-REAL-003 baseline evidence

Against pinned `itsdangerous` `672971d66a2ef9f85151e53283113f33d642dabd`,
the frozen v0.1 reviewer rejected the deleted malformed-input regression in
round 1 and the leaked `UnicodeEncodeError` in round 2. It accepted only the
final `BadData` correction.

```text
$ python evals/v0.2/supplemental/probe_real.py V02-SUP-REAL-003 <candidate-source-root>
ECLIPSE_ACCEPTANCE_EVIDENCE: PASS
exit_code: 0
```
