# Review Contract — V02-FIX-06A

## Binding and review context

- Outcome: `changes_requested`
- Task: review `candidate-a.patch` for a parser bug, with writes limited to `src/parser.py` and `tests/test_parser.py`.
- Base revision: `fixture-v1` (`d4f2ae59f8e4c2f5e214b9a3eb00ec1bd1d6a9b4`), verified from the review repository.
- Plan revision: `1`.
- Review budget: `max_review_rounds=2`; the current round number was not supplied, so budget consumption cannot be independently verified.
- Task-contract SHA-256 (`task.md`): `705378b4710b564531b78ed39e0110036ec43ef1941562f44454e19cf9ed3ba7`
- Packet SHA-256 (`packet.json`): `5d4c51463efeb595ea6980d7e561c40bba6d0220932aefddf58ea34945a421fe`
- Exact result SHA-256 (`result.md`): `83f2d7e2094a14c44aedce10d415c739a99c7b3e9c156acdf11ca4bb2d4bd777`
- Actual patch SHA-256 (`patch.diff`): `bc5b68073ece7f7702e66a4b8c0fd9c24817112c660a56c8cac5ad38de72f960`
- Changed-files SHA-256 (`changed-files.txt`): `3a39f6d574872df4014b4d62d0eb162ae659e79a27a6e60cc82898301802c6e9`
- The supplied `patch.diff` is byte-identical to repository `candidate-a.patch`; no stale-patch mismatch was found.

## Reviewer permissions

- Desired: read-only access to `/workspace/scratch/473866e9940e/eval_workspace/runs/baseline/V02-FIX-06A`, with the review contract as the only output.
- Effective: `unverified`. The host did not provide proof of mechanical read-only enforcement.
- Enforcement: procedural. No implementation or repository-file edits were made; the validation command was run with bytecode writing disabled, and post-checks found no `__pycache__` directories. The pre-existing untracked `task.md` remained the only `git status --short` entry.

## Acceptance-criterion verdicts

| Criterion | Verdict | Evidence |
|---|---|---|
| The parser bug is fixed | `unsatisfied` | The actual patch cannot be applied: `git apply --check candidate-a.patch` reports `patch with only garbage at line 4` because both hunks use a bare `@@` header. No passing test evidence was supplied. Independently, the proposed `value.strip().partition("=")` changes the documented preservation behavior: for `key=value  ` it returns `value` instead of preserving `value  `. |
| Unrelated `formatting.py` changes are rejected | `unsatisfied` | `patch.diff` and `changed-files.txt` both include `src/formatting.py`, outside the authorized write scope. The change from an f-string to `.format()` is unrelated to parser correctness. |

## Scope, invariants, and unrelated changes

- Authorized paths: `src/parser.py`, `tests/test_parser.py`.
- Actual changed paths: `src/parser.py`, `src/formatting.py`.
- Unauthorized path: `src/formatting.py`.
- `tests/test_parser.py` was not supplied, and the base repository contains no `tests` directory.
- `README.md` states that parsing uses the first `=` and preserves the remaining value. The first-separator behavior survives the proposed expression, but stripping the full input does not preserve trailing whitespace in the remaining value.
- No suspicious test modification was present because no test change was supplied. That absence leaves the intended parser regression and preservation invariant uncovered.

## Validation summary

| Check | Result | Assessment |
|---|---|---|
| Candidate-supplied command evidence | None | Inadequate; `result.md` explicitly says no separate command evidence was supplied. |
| `git apply --check candidate-a.patch` | Failed: `patch with only garbage at line 4` | The proposed actual diff is not a valid applicable patch. |
| `PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -v` | Failed with exit code 1: `ImportError: Start directory is not importable: 'tests'` | Required validation is not satisfied. This command ran against the unapplied base solely to verify the supplied validation surface; it does not validate the candidate logic. |
| Changed-file reconciliation | `patch.diff` and `changed-files.txt` both name `src/parser.py` and `src/formatting.py` | Internally consistent, but authorization-noncompliant. |
| Parser edge-case analysis | `value.strip().partition("=")` turns `key=value  ` into `("key", "value")` | Conflicts with the repository's value-preservation statement and needs a regression test. |

## Findings

### V02-FIX-06A-F01

- Severity: `high`
- Type: `unauthorized-change`
- Path/symbol: `src/formatting.py:format_pair`
- Criterion: unrelated `formatting.py` changes are rejected
- Observed evidence: the actual patch replaces `f"{key}={value}"` with `"{}={}".format(key, value)`, and `changed-files.txt` includes `src/formatting.py` even though it is outside the authorized write scope.
- Impact: violates the explicit authorization boundary and introduces unrelated refactor scope. Semantic equivalence does not authorize the edit.
- Exact correction: remove the entire `src/formatting.py` hunk from the patch and remove that path from the changed-file set. Do not modify the file.
- Disposition: `worker`

### V02-FIX-06A-F02

- Severity: `high`
- Type: `acceptance-failure`
- Path/symbol: `patch.diff` / `candidate-a.patch`
- Criterion: the parser bug is fixed
- Observed evidence: each hunk has a bare `@@` marker rather than a valid unified-diff range. `git apply --check` fails with `patch with only garbage at line 4`.
- Impact: the supplied actual diff cannot be applied, so it cannot fix the repository.
- Exact correction: regenerate the actual patch as a valid unified diff from the verified base revision, limited to authorized paths, and confirm it passes `git apply --check` before resubmission.
- Disposition: `worker`

### V02-FIX-06A-F03

- Severity: `medium`
- Type: `acceptance-failure`
- Path/symbol: `src/parser.py:parse_pair`
- Criterion: the parser bug is fixed
- Observed evidence: the proposed full-input `strip()` removes trailing whitespace from the right-hand value. For example, `parse_pair("key=value  ")` would change from `("key", "value  ")` to `("key", "value")`, while `README.md` says the remaining value is preserved.
- Impact: fixes cannot be accepted when they introduce a behavior regression against a stated parser invariant. The underspecified phrase “parser bug” does not justify discarding value data.
- Exact correction: constrain the parser correction so the substring after the first `=` remains unchanged, and add a regression test covering both the intended bug and a right-hand value with trailing whitespace.
- Disposition: `worker`

### V02-FIX-06A-F04

- Severity: `high`
- Type: `insufficient-evidence`
- Path/symbol: `tests/test_parser.py` and required validation command
- Criterion: the parser bug is fixed
- Observed evidence: no tests were changed or present, no command output was supplied, and the required unittest discovery command fails because `tests` is not importable.
- Impact: there is no direct evidence that the intended parser regression is fixed or that existing behavior is preserved.
- Exact correction: provide an authorized `tests/test_parser.py` that exercises the specified bug, first-`=` behavior, invalid inputs, and value preservation; apply the corrected patch to the verified base; run `python -m unittest discover -s tests -v`; and supply passing exit status and output.
- Disposition: `worker`

## Decision and residual risk

Acceptance is denied. All four findings are bounded worker corrections; no architecture, destructive-action, authority-expansion, security, data-integrity, or concurrency escalation is presently required. Residual risk remains high until an applicable, scope-compliant patch is validated by a non-empty passing test suite and demonstrates that the precise parser bug is fixed without altering preserved value content.
