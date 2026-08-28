# V02-SUP-REAL-003 recorded role evidence

Repository pin: `itsdangerous` `672971d66a2ef9f85151e53283113f33d642dabd`.
All stored patches apply cleanly to that exact source state.

## Baseline v0.1 review

- Round 1 rejected deletion of the malformed-base64 regression test.
- Round 2 rejected a leaked `UnicodeEncodeError`; the task requires the public
  `BadData` exception for non-ASCII `str` input.
- The bounded final correction wraps the encoding error as `BadData` and keeps
  valid URL-safe decoding intact.

## Final v0.2 review

The final candidate review observed both frozen candidate regressions from
patch/test evidence and accepted the final correction only after the direct
behavior probe passed.

```text
$ python evals/v0.2/supplemental/probe_real.py V02-SUP-REAL-003 <candidate-source-root>
ECLIPSE_ACCEPTANCE_EVIDENCE: PASS
exit_code: 0
```
