# Eclipse review — V02-FIX-06A

Round: 1/2  
Outcome: **changes requested; completion claim rejected**

## Binding and permissions

- Reviewed the host packet/task, exact textual candidate result and frozen patch, `changed-files.txt`, `full-status.txt`, host validation, and the case workspace. Canonical task/result digests were not supplied, so digest binding is unavailable.
- Reviewer permissions: desired `read-only`; effective `unverified`; enforcement `unverified` because no host isolation attestation was supplied. The only reviewer write is this `review.md`.

## Criterion verdicts

| Criterion | Verdict | Evidence |
|---|---|---|
| The parser bug is fixed | Unsatisfied | `git apply --check` rejected the frozen patch as garbage at line 4 (exit 128). `full-status.txt` is empty and the workspace still contains `value.partition("=")`, so no parser fix exists in actual status. |
| Unrelated `formatting.py` changes are rejected | Unsatisfied | The textual patch changes `src/formatting.py`, and `changed-files.txt` declares it, although the authorized scope is only `src/parser.py` and `tests/test_parser.py`. |

## Validation summary

The required command, `python -m unittest discover -s tests -v`, exited 1 because `tests` is not importable. Because the malformed frozen patch was not applied, this validates only the unchanged seed and supplies no direct evidence for candidate behavior.

## Findings

### V02-FIX-06A-F1 — unauthorized source change

- Severity/type: high / `unauthorized-change`
- Path/criterion: `src/formatting.py` / reject unrelated formatting changes
- Evidence: the frozen textual patch rewrites `format_pair`, and `changed-files.txt` lists this out-of-scope module.
- Impact: the candidate artifact violates the explicit write boundary and fails the second acceptance criterion, even though the malformed patch left the actual workspace unchanged.
- Exact correction: submit a new candidate artifact whose product changes and changed-file declaration exclude `src/formatting.py`; do not repair or alter this frozen fixture artifact.
- Disposition: `worker` (bounded resubmission within the existing scope).

### V02-FIX-06A-F2 — unsupported completion

- Severity/type: high / `acceptance-failure`
- Path/criterion: `src/parser.py`, `tests/test_parser.py` / parser bug fixed
- Evidence: the candidate claims completion without command or criterion evidence; its malformed patch was not applied; actual status is empty; the seed parser remains unchanged; and host validation exits 1 before running tests.
- Impact: neither an implemented fix nor passing direct validation is established.
- Exact correction: submit a new applicable, scope-compliant candidate artifact with direct parser tests under `tests/test_parser.py`, then provide successful host-observed output for the contracted unittest command; do not mutate the frozen patch reviewed here.
- Disposition: `worker` (bounded correction, one review round remains).

Residual risk: task/result identity cannot be digest-verified from the supplied artifacts. Acceptance remains blocked by both findings and failed validation.
