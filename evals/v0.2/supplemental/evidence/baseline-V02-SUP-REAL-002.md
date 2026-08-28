# V02-SUP-REAL-002 baseline evidence

Against pinned `itsdangerous` `672971d66a2ef9f85151e53283113f33d642dabd`,
the frozen v0.1 reviewer rejected truncation in round 1 and the wrong public
message plus generic assertion in round 2. It accepted the final bounded
correction only after the direct probe passed.

```text
$ python evals/v0.2/supplemental/probe_real.py V02-SUP-REAL-002 <candidate-source-root>
ECLIPSE_ACCEPTANCE_EVIDENCE: PASS
exit_code: 0
```
