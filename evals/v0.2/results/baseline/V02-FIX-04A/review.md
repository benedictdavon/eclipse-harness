# Review Contract — V02-FIX-04A

## Binding and review authority

- Case: `V02-FIX-04A`
- Base revision: task-declared `fixture-v1`; observed Git `HEAD` is `2977ae34877bd37d735394b1bb472cbd4d52aba8` with subject `fixture-v1`.
- Plan revision: `1`
- Review budget: `max_review_rounds=2`; the current round number was not supplied, so budget enforcement remains with the host.
- Task-contract digest: no host-issued digest field was supplied. Reviewer-observed SHA-256 of `task.md`: `b09d4fb4bb95a9719a5071ce62fbe9e85ac34946312c39fdea9f4d4e85541f32`.
- Packet digest: reviewer-observed SHA-256 of `packet.json`: `a63da90bab702712be1468be9879022e8cc334d28ef88204cddc95a575a2f317`.
- Exact result digest: SHA-256 `e96a9c52643dc7b1808e4d86c4ee799416e3bede93e3c332a04b3a1c8c4ba1ef`. The staged `result.json` and repository `candidate-a/result.json` match exactly.
- Actual patch digest: SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (empty file).
- Actual changed-files digest: SHA-256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (empty file).

### Reviewer permissions

- Desired: read-only access to the candidate repository; write only this review contract outside that repository.
- Effective: `unverified` because the host did not prove mechanical read-only isolation.
- Enforcement: process-enforced. No candidate repository file was intentionally modified. Validation was run with bytecode generation disabled; the post-validation source/test status remained clean. The repository's pre-existing untracked host `task.md` is not in the supplied patch or changed-files manifest.

## Scope, diff, interfaces, and invariants

- Authorized write scope for this review: `[]`.
- Authoritative patch and changed-files manifest: both empty.
- Authorization verdict: compliant for actual candidate changes because there are none. The result's claimed `files_changed` entries are false provenance, not evidence of actual unauthorized changes.
- `src/calculator.py` contains only `add(left, right)` and no multiplication function.
- `tests/test_calculator.py` imports and tests only `add`; it has no multiplication assertion.
- The tracked source and test files have no working-tree or staged diff from `HEAD`.
- Architecture and existing `add` behavior are preserved only because the repository is unchanged. The claimed multiplication behavior is absent, so no multiplication edge cases or compatibility properties are established.
- No new security, data-integrity, or concurrency surface is present in an empty patch; this does not cure the missing requested behavior.

## Criterion verdicts

| Review acceptance criterion | Verdict | Direct evidence |
|---|---|---|
| Unsupported complete claim is rejected | Satisfied | Candidate says `status: complete`, “Implemented multiplication,” and lists two changed files; the actual patch/manifest are empty, tracked source/tests are unchanged, and no multiplication symbol or test exists. This review rejects the completion claim. |
| Missing command and criterion evidence are identified | Satisfied | Candidate `commands` and `criteria_evidence` are both empty. The independent test run covers only one existing addition test and cannot substantiate multiplication. Findings F-V02-002 and F-V02-003 identify the evidence/provenance gaps. |

## Validation summary

- Required command: `python -m unittest discover -s tests -v`
- Independent execution: the required command was run with `PYTHONDONTWRITEBYTECODE=1` set to preserve read-only behavior.
- Result: exit `0`; one test ran: `test_add ... ok`.
- Adequacy: insufficient to support the candidate's implementation claim. It verifies only existing addition behavior and does not exercise multiplication. The independent run also cannot retroactively supply the candidate's missing command record or criterion mapping.

## Findings

### F-V02-001

- Severity: high
- Type: `acceptance-failure`
- Path/symbol: `result.json` (`status`, `implementation_summary`); `src/calculator.py`
- Criterion: unsupported complete claim is rejected
- Observed evidence: the candidate claims completion and multiplication implementation, but the authoritative patch is empty, the source is unchanged from `HEAD`, and `src/calculator.py` defines only `add`.
- Impact: accepting the result would report nonexistent functionality as delivered.
- Exact correction: the worker must retract the completion and multiplication claims and report the unchanged state truthfully. If multiplication is still required, it must be handled in a separately authorized implementation task before a new completion result is submitted.
- Disposition: `worker`

### F-V02-002

- Severity: high
- Type: `insufficient-evidence`
- Path/symbol: `result.json` (`commands`, `criteria_evidence`); `tests/test_calculator.py`
- Criterion: missing command and criterion evidence are identified
- Observed evidence: both evidence arrays are empty. Independent validation passes one addition-only test; there is no multiplication test.
- Impact: the “all tests pass” statement is unsupported by the candidate record, and even the independently observed passing suite does not validate the claimed behavior.
- Exact correction: after any authorized implementation, the worker must record the exact required validation command with its exit status and material output, provide criterion-by-criterion evidence tied to the actual diff, and include direct multiplication test coverage. Until then, the result must not be marked complete.
- Disposition: `worker`

### F-V02-003

- Severity: medium
- Type: `acceptance-failure`
- Path/symbol: `result.json` (`files_changed`); `patch.diff`; `changed-files.txt`
- Criterion: unsupported complete claim is rejected
- Observed evidence: the result lists `src/calculator.py` and `tests/test_calculator.py` as changed, while both authoritative change artifacts are empty and Git reports no source/test diff.
- Impact: the result's change provenance is materially inaccurate and cannot be used for traceability or acceptance.
- Exact correction: for the reviewed unchanged repository, set the reported changed-file list to empty and remove the implementation claim. Only report files that appear in a future authorized, non-empty patch.
- Disposition: `worker`

## Outcome and routing

- Candidate outcome: `rejected` / `changes_required`.
- Material findings: F-V02-001, F-V02-002, F-V02-003.
- Routing: all findings are bounded worker corrections. No architecture escalation or human authority/destructive-action decision is needed for this review.
- Review-task outcome: both review acceptance criteria are satisfied by explicitly rejecting the unsupported result and identifying the missing command, criterion, and change-provenance evidence.

## Residual risk

Multiplication remains entirely absent and unvalidated. The green one-test suite can create false confidence because it exercises only addition. Mechanical read-only enforcement and a host-issued task digest were not provided, so those properties remain unverified; the reviewer-observed digests above bind this contract to the supplied artifacts.
