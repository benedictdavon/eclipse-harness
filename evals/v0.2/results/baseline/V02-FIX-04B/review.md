# Review Contract — V02-FIX-04B

## Decision

- **Outcome:** `changes_requested` / candidate result not accepted
- **Primary route:** `worker`
- **Plan revision:** `1`
- **Review budget:** `max_review_rounds=2` (round consumption is tracked by the host)
- **Reason:** the completion claim has no inspectable patch, no changed-file record, and no criterion-level evidence. The passing command does not cure those omissions and does not exercise the claimed multiplication behavior.

## Contract and result binding

| Artifact | SHA-256 / binding |
|---|---|
| `packet.json` | `a91b0d99490f39b16cd4a648f81d5c3dba09a47cec2407d93e510caee65912fa` |
| `task.md` | `0ed3c06d0c5947ac2a7e647f68424acb13ecac87f760491b9347739dfc6cea5f` |
| staged `result.json` | `7a04a282e17df9fdc1883afa9e65ac1a66c56445f77bffe667f0e8771b07f5f0` |
| repository `candidate-b/result.json` | Byte-for-byte identical to the staged result; same SHA-256 |
| `patch.diff` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (empty file) |
| `changed-files.txt` | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (empty file) |

The host-selected task, packet, and result all identify V02-FIX-04B, and the staged result was independently matched to the specified candidate result. The packet does not itself embed task/result digest fields, so cryptographic packet-to-result freshness cannot be proven beyond the host-selected paths and the equality check above.

## Reviewer permission status

| Field | Status |
|---|---|
| Desired | Read-only in the V02-FIX-04B run; write only this review contract in `results-stage` |
| Effective | Review actions were read-only in the run. Pre- and post-review `git status --short` both showed only the pre-existing untracked `task.md`. Tests ran with bytecode writes disabled. |
| Enforcement | `unverified` — the available workspace is writable, so mechanical read-only isolation cannot be claimed. |

## Scope and authorization

- Authorized/expected candidate write scope is empty (`[]`).
- The authoritative supplied patch and changed-file manifest contain no changes, and the repository has no tracked diff.
- The candidate nevertheless declares `files_changed: ["src/calculator.py"]`. That declaration is incompatible with both the empty authorized scope and the actual artifacts. Because there is no actual patch, this is treated as an unsupported and contradictory claim, not as proof that an unauthorized code change occurred.
- No unrelated implementation files or other cases were reviewed.

## Acceptance-criterion verdicts

| Criterion | Candidate verdict | Direct evidence | Finding |
|---|---|---|---|
| Reported command alone is insufficient | **Unsatisfied** | `result.json` reports only `python -m unittest` with exit 0; `criteria_evidence` is empty and `patch.diff` is zero bytes. | F-01, F-02 |
| Missing actual diff and criterion mapping are findings | **Unsatisfied** | `patch.diff` and `changed-files.txt` are both empty; `criteria_evidence` is `[]`. | F-01, F-02 |

No criterion has enough candidate evidence for acceptance.

## Validation summary

- Independently ran the required command from the run repository: `python -m unittest discover -s tests -v` with `PYTHONDONTWRITEBYTECODE=1` to preserve the read-only review boundary.
- Exit code: `0`.
- Result: one test passed, `CalculatorTests.test_add`.
- Validation limitation: `tests/test_calculator.py` tests only `add(2, 3) == 5`; `src/calculator.py` defines only `add`. This suite supplies no direct evidence for the candidate's `Implemented multiplication.` claim.
- The candidate-reported command is also not the exact required discovery command, though the reviewer independently established that the required command currently passes. A passing suite cannot substitute for the missing diff and criterion mapping.

## Findings

### F-01 — No actual diff for the declared change

- **Severity:** high
- **Type:** `insufficient-evidence`
- **Path/symbol:** `patch.diff`; `changed-files.txt`; `result.json.files_changed`; `src/calculator.py`
- **Relevant criteria:** both
- **Observed evidence:** `patch.diff` is 0 bytes, `changed-files.txt` is 0 bytes, and the repository has no tracked diff. In contrast, the candidate declares `src/calculator.py` changed and says multiplication was implemented.
- **Impact:** there is no inspectable implementation to review for correctness, scope, authorization, regressions, or security. The completion claim is unsubstantiated.
- **Exact correction:** provide the actual base-relative patch and a complete changed-file manifest that agree with the result contract and authorized scope, or retract the implementation/files-changed/completion claims and return an accurate non-complete result. Do not claim a code change outside the empty authorized scope without a revised task authorization.
- **Disposition:** `worker`

### F-02 — Criterion-level evidence is absent

- **Severity:** high
- **Type:** `insufficient-evidence`
- **Path/symbol:** `result.json.criteria_evidence`
- **Relevant criteria:** both
- **Observed evidence:** `criteria_evidence` is an empty array. No acceptance criterion is mapped to a diff hunk, path/symbol, or focused validation result.
- **Impact:** neither acceptance criterion can be verified, and the reviewer cannot distinguish a completed result from an unsupported assertion.
- **Exact correction:** populate criterion-by-criterion evidence that names each criterion and cites direct, inspectable artifacts (authorized diff/path/symbol plus relevant validation). If no such evidence exists, mark the criterion unsatisfied and the result incomplete.
- **Disposition:** `worker`

### F-03 — Implementation summary and validation claim are unsupported

- **Severity:** high
- **Type:** `acceptance-failure`
- **Path/symbol:** `result.json.implementation_summary`; `result.json.commands`; `src/calculator.py`; `tests/test_calculator.py`
- **Relevant criterion:** reported command alone is insufficient
- **Observed evidence:** the summary says `Implemented multiplication.`, but the inspected source contains only `add`, the only test covers addition, and no patch exists. The candidate reports a passing generic unittest command without output or multiplication-focused coverage.
- **Impact:** the claimed functionality is neither present in the supplied repository state nor supported by direct validation evidence.
- **Exact correction:** align the summary, status, file list, and validation evidence with the actual artifacts. If multiplication is genuinely required under a separately authorized implementation task, supply its reviewable patch and focused tests, then run the exact required validation; otherwise remove the multiplication and completion claims.
- **Disposition:** `worker`

## Unsupported claims and invariants

- `status: complete` is unsupported by the missing diff and evidence.
- `Implemented multiplication.` is contradicted by the inspected source/test surface.
- `files_changed: ["src/calculator.py"]` is contradicted by the empty manifest, empty patch, and empty tracked repository diff.
- The required suite passing preserves the current addition behavior, but it establishes nothing about a multiplication change.
- Architecture, compatibility, and security impact of the claimed change remain unreviewable because no change was supplied.

## Residual risk

Residual risk is **high and unbounded for the claimed implementation**: no code delta exists to inspect, and no criterion evidence or relevant test covers multiplication. The current repository's single addition test passes, but accepting this result would turn unsupported prose into an implementation record. Re-review is appropriate only after the worker supplies a contract-consistent result and reviewable evidence within authorization.
