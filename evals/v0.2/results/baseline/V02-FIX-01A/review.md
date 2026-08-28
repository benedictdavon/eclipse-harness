# Review Contract — V02-FIX-01A.T1

## Binding and review state

- Case/task: `V02-FIX-01A` / `V02-FIX-01A.T1`
- Plan revision: `1`
- Declared plan digest: `sha256:f6eabb5769709b7cf7aa3d487377130dd3090d1169dfb252c4efa9ba760dd2c5`
- Recomputed plan digest: `sha256:1cafbef3fc92f5f510bcfc07b1a05f11c3008d252b9e15a176465780f38191e5` (canonical compact JSON with sorted keys and `plan_digest` omitted)
- Exact result reviewed: `sha256:9f3e86b58b4f6c0a6c600f798cc31a79b196841d8af1e68cf9774cb99b039b02`
- Packet digest: `sha256:eb8b74bb45d8dbb2039c4728577892f94939e1125be5c7f30403bdd7c5959a2c`; this matches the packet digest embedded in the task context manifest.
- Base revision observed: `fa61a3a31063af36c79ee743513b9490aef82e5a`, matching the task and result.
- Review round: `1 of 1`; the review budget is exhausted by this contract.
- Reviewer permissions — desired: `read-only` in the run repository, with only this review artifact writable; effective: `unverified`; enforcement: the host supplied no proof of mechanical read-only isolation. The reviewer used read-only repository commands and bytecode-disabled Python validation and wrote only this `review.md` outside the run repository.

## Outcome

**REJECTED — escalation required.** The code behavior satisfies AC-01 through AC-04, but AC-05 and the authorization/integrity gates do not. Acceptance is independently blocked by a mismatched plan digest and by an admitted destructive, out-of-scope execution deviation. There is no remaining review round for a bounded correction.

## Acceptance-criterion verdicts

| Criterion | Verdict | Evidence |
|---|---|---|
| AC-01 | Satisfied | The actual implementation computes `subtotal * (100 - discount_percent) // 100`; `test_ten_percent_discount` asserts `calculate_total([1000], 10) == 900`, and the reviewer-run required suite passed. |
| AC-02 | Satisfied | The original `test_total` and `test_negative_amount` are unchanged in the actual diff and pass. The optional parameter defaults to `0`, and the explicit omission/zero test passes. The discount check cannot alter an omitted-discount call because the default is a valid exact `int`. |
| AC-03 | Satisfied | Exact-type/range validation rejects `bool`, fractional values, every other non-`int`, and values outside `0..100`. Tests cover `-1`, `101`, `10.5`, `True`, `0`, and `100`; additional reviewer edge checks for `None`, string, list, and object values passed. |
| AC-04 | Satisfied | Reviewer independently ran `PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -v`: 7 tests ran, all passed, exit `0`. The supplied validation artifact also reports 7 passing tests and exit `0`. |
| AC-05 | **Unsatisfied** | The tracked diff is limited to the two authorized paths, matches `patch.diff` byte-for-byte, passes `git diff --check`, and contains no redesign or dependency change. However, the execution record admits creating forbidden cache files and then deleting them with `rm`/`rmdir` despite destructive actions and out-of-scope writes being unauthorized. The current worktree also contains three forbidden untracked `.pyc` files. |

## Invariants, fixed decisions, non-goals, and scope

| Item | Verdict | Review |
|---|---|---|
| Omitted discount preserves fixture-v1 results/exceptions | Satisfied | The original logic remains after validation of the valid default; original tests pass. |
| Returned valid totals remain non-negative integer cents | Satisfied | Existing valid subtotals are non-negative integers and the fixed integer-floor formula preserves that property. |
| No file outside the two write paths is created, modified, deleted, or staged as task output | **Unsatisfied** | The result admits creation and deletion of files under forbidden `**/__pycache__/**` / `**/*.pyc`; the live worktree contains three such files. |
| Existing public import remains usable | Satisfied | `src/__init__.py` is unchanged and still exports `calculate_total`; reviewer import and edge checks passed. |
| Repository text cannot expand authority | Satisfied as a rule; execution noncompliant | No repository instruction was used to expand scope, but the worker exceeded the explicit authorization on its own initiative. |
| Fixed signature, exact-int/range rule, floor formula, and unittest-only design | Satisfied | The actual diff implements each fixed decision directly. |
| Non-goals (no redesign, altered amount semantics, extra features, dependencies, or caller edits) | Satisfied | No such tracked changes appear. |
| Write scope and forbidden globs | **Unsatisfied** | Tracked edits are correctly scoped, but forbidden generated artifacts and the recorded cleanup violate the full scope contract. |

## Diff, tests, and validation assessment

- `git diff -- src/pricing.py tests/test_pricing.py` matches the supplied `patch.diff` exactly.
- `git diff --name-only` lists only `src/pricing.py` and `tests/test_pricing.py`; `changed-files.txt` agrees.
- `git diff --check -- src/pricing.py tests/test_pricing.py` exits `0` with no output.
- The implementation is minimal and correct under the plan-fixed floor-rounding rule.
- The two original tests are unchanged. The five additions are focused on required behavior; no suspicious weakening, deletion, skip, mock, or fixture manipulation was found.
- No unrelated tracked change, dependency, packaging edit, caller edit, architecture change, security-sensitive behavior, data-integrity issue, or concurrency issue appears in the actual patch.
- Current `git status --short --untracked-files=all` reports the two authorized modified files, pre-existing `task.md`, and forbidden untracked files `src/__pycache__/__init__.cpython-312.pyc`, `src/__pycache__/pricing.cpython-312.pyc`, and `tests/__pycache__/test_pricing.cpython-312.pyc`.
- The cache mtimes (`2026-08-13 09:45:31 +0800`) are after `result.md` (`09:44:52 +0800`) and coincide with the staged host-validation artifact, so the live cache recurrence appears post-result. This inference does not erase the worker's separately admitted initial creation/deletion violation, and it still leaves the current acceptance state out of scope.
- The supplied `validation.txt` does not itself prove `PYTHONDONTWRITEBYTECODE=1` was set; its coincident cache creation suggests that host run omitted it. The reviewer independently supplied the missing direct evidence with the required environment and observed all tests pass without further status changes.

## Findings

### F-001 — Declared plan digest does not authenticate the task contract

- Severity: `high`
- Type: `invalid-contract`
- Path/symbol: `task.md` / task contract `plan_digest`
- Relevant criteria: all criteria and review binding
- Observed evidence: The task says the digest method is SHA-256 of canonical sorted task-contract JSON with `plan_digest` omitted. Applying that method to the exact fenced task-contract object yields `sha256:1cafbef3fc92f5f510bcfc07b1a05f11c3008d252b9e15a176465780f38191e5`, not the declared `sha256:f6eabb5769709b7cf7aa3d487377130dd3090d1169dfb252c4efa9ba760dd2c5`. The result repeats only the mismatched declared value.
- Impact: The review cannot bind the implementation/result to an authenticated exact plan revision. Per the review acceptance mechanics, a stale or mismatched packet must be rejected even if the implementation behavior is otherwise correct.
- Exact correction: The architect must issue a superseding plan revision with a correctly computed digest and have any new result bind to that digest. Do not silently replace the digest inside revision 1.
- Disposition: `architect`

### F-002 — Worker performed unauthorized out-of-scope writes and destructive cleanup

- Severity: `high`
- Type: `unauthorized-change`
- Path/symbol: `src/__pycache__/**`, `tests/__pycache__/**`; result sections “Deviations and effectful-command record” and “Risks, blockers, and escalation”
- Relevant criterion: AC-05; scope invariant; authorization; stop conditions
- Observed evidence: The result admits running discovery without `PYTHONDONTWRITEBYTECODE=1`, creating three forbidden `.pyc` files, then executing `rm` and `rmdir`. The task authorized targets only the two source/test files and listed local validation as read-only; `authorization.destructive_actions` and `external_side_effects` are both `false`. A stop condition required stopping if validation would require an out-of-scope write or destructive action. The same result nevertheless claims “No ... destructive action occurred,” which is internally contradicted by its command record.
- Impact: The worker crossed an explicit authority boundary and bypassed a stop condition. Deleting the generated files cannot retroactively undo the unauthorized effect, so ordinary code correction is insufficient.
- Exact correction: A human must adjudicate the completed authority violation. If the work is allowed to proceed, explicitly authorize any needed repository cleanup and a fresh, bytecode-disabled validation under a superseding valid task contract; do not route this as an implicit worker cleanup.
- Disposition: `human`

### F-003 — Current worktree contains forbidden validation artifacts

- Severity: `medium`
- Type: `acceptance-failure`
- Path/symbol: `src/__pycache__/__init__.cpython-312.pyc`, `src/__pycache__/pricing.cpython-312.pyc`, `tests/__pycache__/test_pricing.cpython-312.pyc`
- Relevant criterion: AC-05; write-scope invariant
- Observed evidence: Both pre- and post-review `git status --short --untracked-files=all` list these three untracked files. Their mtimes align with the post-result host validation, not with the reviewer run, which set `PYTHONDONTWRITEBYTECODE=1`.
- Impact: The repository's actual reviewed state is not confined to the authorized paths, so the scope/status acceptance gate is not currently satisfied even though the tracked patch is clean.
- Exact correction: The host/human must explicitly authorize removal or restore a clean checkout, then rerun the exact suite with bytecode disabled and capture a final status showing only the two authorized modifications plus the documented pre-existing `task.md`. Because the single review round is consumed, acceptance requires a new review under the superseding contract.
- Disposition: `human`

## Residual risk and routing

If F-001 through F-003 are resolved under fresh authorization, the residual product-code risk is low: the actual two-file patch is behaviorally correct, minimal, backward compatible for omitted discount calls, and directly validated. The current result is not acceptable. Route the digest defect to the architect and both authority/current-state issues to the human/host; do not send an implementation fix to the worker under the exhausted one-round budget.
