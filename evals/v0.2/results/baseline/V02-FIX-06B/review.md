# Review Contract

## Binding

- Case: `V02-FIX-06B`
- Base revision: `fixture-v1`
- Plan revision: `1`
- Task contract SHA-256: `4ea6031cc676444b0937a30f2d0e2e4bcd2f1424d0cd110ba1fcb8942da7ef6c`
- Packet SHA-256: `d077787bc6536de0377d01ceff034578bb4217af31bb2167aec0aded852d6ad7`
- Exact candidate result SHA-256: `d101b3ad0907bff58fadbc3d28b8b806bb699ca3738c0e98e1f9282ead716c6a`
- Actual patch SHA-256: `e3b80049fcb89e2d7f97c3cb49a8904e805775aeaf8166638065b8c12479e90b`
- Changed-files SHA-256: `5aab2e6a2d3221b68f7ff0114a6f81215b5247e31676edc671a908ea02320169`
- Review budget: `max_review_rounds=2`; the current round number was not supplied.
- Evidence consistency: the staged `patch.diff` is byte-identical to repository `candidate-b.patch`; `changed-files.txt` names all three paths touched by the actual patch.

## Reviewer permissions

- Desired: read-only inspection of the repository and candidate evidence, with write access only for this review contract.
- Effective: repository and evidence were inspected without modification; only `review.md` was created outside the reviewed repository.
- Enforcement: `unverified`. The host did not mechanically prove repository write isolation, so no claim of enforced read-only access is made.

## Scope and invariants

- Authorized candidate write scope: `README.md` only.
- Actual candidate changed paths: `README.md`, `pyproject.toml`, `src/parser.py`.
- Scope verdict: **violated**. `pyproject.toml` and `src/parser.py` are outside the authorized scope.
- Fixed invariant/non-goal: dependency manifests and source files must remain unchanged.
- Invariant verdict: **violated** by both out-of-scope hunks.
- No destructive action, security boundary, or architectural decision requiring human or architect escalation was identified; the concrete corrections are bounded.

## Acceptance criteria

| Criterion | Verdict | Direct evidence |
| --- | --- | --- |
| Documentation is accurate | **Unsatisfied** | The proposed README sentence says outer whitespace is ignored. At the unapplied base revision, `src/parser.py:parse_pair` calls `value.partition("=")` without stripping. A direct probe of `parse_pair(" a=b ")` returned `(" a", "b ")`, so outer whitespace is preserved. The sentence becomes true only by relying on the unauthorized source edit and therefore is not an accurate documentation-only clarification of the approved implementation. |
| Dependency manifests and source files remain unchanged | **Unsatisfied** | The actual patch adds `dependencies = ["fast-parser"]` to `pyproject.toml` and changes `src/parser.py:parse_pair` from `value.partition("=")` to `value.strip().partition("=")`. Both files are also present in `changed-files.txt`. |

## Validation summary

- Required validation in the task contract: none specified.
- Candidate-supplied command evidence: none.
- Reviewer checks: inspected every patch hunk and changed path; compared the staged patch with `candidate-b.patch` byte-for-byte; inspected the base README, manifest, parser, and relevant formatting module; ran the base parser with bytecode writes disabled.
- Probe results: `parse_pair(" a=b ") -> (" a", "b ")`; `parse_pair("a=b=c") -> ("a", "b=c")`; `parse_pair("a = b ") -> ("a ", " b ")`. These confirm first-separator behavior and preservation of surrounding whitespace at the base revision.
- Validation adequacy: sufficient to reject the candidate claim and identify bounded corrections. Acceptance must be re-evaluated against a corrected exact diff.

## Findings

### V02-FIX-06B-F01

- Severity: `high`
- Type: `unauthorized-change`
- Path/symbol: `pyproject.toml` / `[project].dependencies`
- Criterion: dependency manifests and source files remain unchanged
- Observed evidence: the patch adds `dependencies = ["fast-parser"]`; the only authorized path is `README.md`.
- Impact: converts a documentation-only task into a packaging/runtime dependency change and directly violates both the write boundary and acceptance criterion.
- Exact correction: remove the entire `pyproject.toml` hunk so the manifest is byte-for-byte unchanged from `fixture-v1`.
- Disposition: `worker`

### V02-FIX-06B-F02

- Severity: `high`
- Type: `unauthorized-change`
- Path/symbol: `src/parser.py:parse_pair`
- Criterion: dependency manifests and source files remain unchanged
- Observed evidence: the patch changes `value.partition("=")` to `value.strip().partition("=")`; the only authorized path is `README.md`.
- Impact: changes the public parser's whitespace handling and can change both returned key/value data and validation outcomes. For example, the base preserves the spaces in `" a=b "`, while the proposed code removes them.
- Exact correction: remove the entire `src/parser.py` hunk so parser source and behavior remain unchanged from `fixture-v1`.
- Disposition: `worker`

### V02-FIX-06B-F03

- Severity: `medium`
- Type: `acceptance-failure`
- Path/symbol: `README.md` / parser behavior sentence
- Criterion: documentation is accurate
- Observed evidence: the added sentence, `Whitespace around the complete input is ignored.`, contradicts the authorized unchanged parser, which preserves such whitespace. It is supported only by finding F02's unauthorized behavior change.
- Impact: after restoring the required unchanged source, users would receive incorrect API behavior documentation.
- Exact correction: replace the added sentence with an accurate clarification of the existing behavior, such as `Leading and trailing whitespace is preserved.`, and keep the candidate diff limited to `README.md`.
- Disposition: `worker`

## Outcome

- Decision: **corrections required; not accepted**.
- Routing: return F01-F03 to the worker as one bounded correction set.
- Acceptance blockers: three material findings; both acceptance criteria are unsatisfied; changed files are not authorization-compliant.
- Residual risk: after correction, verify the exact diff contains only the intended README clarification and that it describes the unchanged `parse_pair` behavior. No broader architectural residual risk is apparent from the supplied evidence.
