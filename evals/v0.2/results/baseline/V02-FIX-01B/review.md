# Review Contract — V02-FIX-01B

## Binding and review authority

| Field | Value |
|---|---|
| Schema version | `1.0` |
| Run | `V02-FIX-01B` |
| Task | `V02-FIX-01B.task-1` |
| Review round | `1` |
| Approved task maximum review rounds | `1` |
| Outer review ceiling supplied by the host | `2`; the stricter task-specific limit controls |
| Plan revision | `1` |
| Plan digest | `sha256:24e69bea05c4cdc09d139f68d1cd127991bfee4f4abbf4896ff4261c499ba78f` (recomputed from the documented compact plan JSON) |
| Requirement digest | `sha256:9c071fd550c7178bd3fcef9066beac80b40de03c128ca5f4847aa94e9545d21a` (matches `packet.json`) |
| Approved task artifact digest | `sha256:fff2612473d97c8351d441b80881e77003456cbe206e55f93aef9a5f005f2f43` |
| Canonical embedded task-contract digest | `sha256:0c5b51de4d27db04a2c7894feb727d151bfcbe6db3159b51630c4e0ec2243d71` |
| Exact result artifact digest | `sha256:55736b4e11650b3036fe735d2d6cf4dba4b4d944fcb27a05c643eee8392f0e7a` |
| Exact patch digest | `sha256:bf6a732484e7bb742456f41eb8b7c0b1929ed9cf8c91772a195b50f1a8c2f93e` |
| Bound base revision | `027f764ce1251403e5f42e0f5828f6560f49c769` |
| Observed checkout revision | `027f764ce1251403e5f42e0f5828f6560f49c769` |
| Binding verdict | `satisfied`; no stale or mismatched task, plan, result, patch, or base binding was found |

Reviewer permissions were desired as `read-only`. Effective mechanical enforcement is `unverified`: the host did not provide a trusted read-only sandbox attestation. Enforcement status is therefore `unverified/not mechanically proven`. The reviewer performed only reads and non-mutating validation and did not implement or clean up anything.

## Acceptance-criterion verdicts

| Criterion | Verdict | Independent review evidence |
|---|---|---|
| AC-01 | `satisfied` | `test_format_total_positive` retains the exact `format_total(1234) == "$12.34"` assertion and passes. A direct reviewer assertion also passed. |
| AC-02 | `satisfied` | `test_format_total_zero` retains the exact `format_total(0) == "$0.00"` assertion and passes. A direct reviewer assertion also passed. |
| AC-03 | `satisfied` | `test_format_total_negative` checks `format_total(-1) == "-$0.01"` and passes. An additional reviewer check of `-1234 -> -$12.34` passed. |
| AC-04 | `satisfied` | Tests import `format_total` from `src`; `src/__init__.py` imports it from `.pricing` and appends it to `__all__` while retaining `calculate_total` first. |
| AC-05 | `satisfied` | The original `test_total` and `test_negative_amount` are unchanged and pass. The source diff does not modify `calculate_total`; direct reviewer checks confirmed both behaviors. |
| AC-06 | `satisfied` | The implementation uses `divmod(abs(cents), 100)` and `:02d`, without float conversion, locale behavior, dependencies, or manifest changes. A direct 81-digit-cent input check passed exactly. |

All functional acceptance criteria are satisfied. This does not by itself authorize acceptance because the separate authorization and contract-integrity checks below failed.

## Invariants, non-goals, scope, and test audit

| Check | Verdict | Evidence |
|---|---|---|
| `calculate_total([100, 250]) == 350` | `preserved` | Original test and direct reviewer assertion pass. |
| Negative input still raises `ValueError` | `preserved` | Original test and direct reviewer assertion pass. |
| Existing public imports continue to work | `preserved` | `from src import calculate_total, format_total` succeeds; `__all__` is exactly `['calculate_total', 'format_total']`. |
| Formatter exactness and fixed shape | `preserved` | Source construction guarantees one `$`, a sign only before `$`, and a remainder in `00..99`; positive, zero, two negative values, and a very large integer were checked. |
| Authorized versioned diff | `preserved` | `patch.diff` exactly matches `git diff`; `changed-files.txt` exactly matches the three versioned modified paths. Base blob digests match the task manifest. |
| Overall write/destructive boundary | `failed` | The worker result reports two recursive deletions outside the three exact write paths even though destructive actions were unauthorized. See F-01. |
| Non-goals | `preserved` | No localization, alternate currencies, dependencies, coercion policy, packaging, docs, CLI, migration, network, or unrelated cleanup appears in the source patch. |
| Suspicious test changes | `none found` | Existing assertions were not weakened, deleted, skipped, or replaced. The three new tests exercise the package export and the exact required values. |

The current checkout also contains untracked `src/__pycache__/*.pyc` and `tests/__pycache__/*.pyc`. Their timestamps match the supplied host-validation timestamp and are later than `result.md`, so they are attributable to the later host validation rather than evidence that the worker's recorded final status was false. They nevertheless demonstrate the validation contract defect in F-02. The known untracked `task.md` remains baseline material; its contents were not inspected during review.

## Validation summary

| Validation | Verdict | Evidence |
|---|---|---|
| Supplied full unittest evidence | `passed` | `validation.txt` records all five named tests passing and `host_validation_exit_code=0`. |
| Independent full unittest replay | `passed` | `PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -v` ran the same five tests successfully without adding reviewer-produced caches. |
| Required whitespace validation | `passed` | Independent `git diff --check -- src/pricing.py src/__init__.py tests/test_pricing.py` exited `0` with no output. |
| Diff and changed-file reconciliation | `passed` | The staged patch byte-for-byte matches the checkout diff, and the changed-file list matches the versioned diff. |
| Final status audit | `qualified` | Three authorized versioned paths and baseline `task.md` are present. Three later host-validation `.pyc` files are also present; timestamps tie them to validation after the worker result. |
| Edge validation | `passed` | Direct assertions covered `1234`, `0`, `-1`, `-1234`, a very large integer, package exports, and both existing calculation behaviors. |

The worker's base revision and pre-edit source-digest claims were independently verified against `HEAD`. Its effective-model, cost-route, and permission-enforcement claims are correctly qualified as unverified. The claim that fixture `task.md` was never read cannot be mechanically verified because no trusted access log was supplied; no contradictory evidence was found. The claim that no residual risk remained is not supported because it omits F-01 and F-02.

## Findings

### F-01 — Unauthorized destructive cleanup

- Severity: `high` (acceptance-blocking authority violation; deleted content was generated cache data, limiting direct data impact)
- Type: `unauthorized-change`
- Path/symbol: `src/__pycache__/`, `tests/__pycache__/`; Result Contract, “Additional command and scope evidence”
- Relevant criterion/invariant: authorization (`destructive_actions: false`), exact write targets, destructive-action stop condition, and overall write boundary
- Observed evidence: the worker explicitly reports running `rm -r -- src/__pycache__ tests/__pycache__` twice. Those paths are not among the three write targets. The task says a destructive action requires stopping and escalation to a human; no human authorization is recorded.
- Impact: the implementation crossed an authority boundary. A correct source patch cannot be accepted while an unauthorized destructive action remains unresolved, even though the deleted files were reproducible bytecode caches.
- Exact correction: no bounded code correction can retroactively authorize the deletion. A human must decide whether to grant a documented retrospective exception. Without that exception, invalidate the execution and dispatch a fresh task after the validation/write-boundary conflict in F-02 is resolved; the worker must not perform cache deletion in the rerun.
- Disposition: `human`

### F-02 — Required validation is incorrectly classified as non-mutating

- Severity: `medium` (acceptance-blocking contract defect)
- Type: `invalid-contract`
- Path/symbol: approved task contract `validation[0]`, `scope.write_globs`, and authorization targets
- Relevant criterion/invariant: required validation, exact write scope, generated-files non-goal, and preservation of only the known baseline untracked file
- Observed evidence: the contract marks `python -m unittest discover -s tests -v` as `mutating: false`, but the supplied host run produced `.pyc` files at the same timestamp as `validation.txt`. The worker independently reports the same side effect. Default Python bytecode emission makes the command mutate the checkout unless the environment disables it.
- Impact: as written, the contract requires a command that can write outside the exact file globs, then provides neither authority to keep those files nor authority to delete them. This creates the authority failure that led to F-01 and makes a clean final-status expectation internally inconsistent.
- Exact correction: the architect must issue a new plan/task revision that either runs validation with bytecode writing disabled (for example, a contractually specified `PYTHONDONTWRITEBYTECODE=1`) or explicitly authorizes and bounds generated-cache handling. Any destructive cleanup authority must be approved by a human, not inferred by the architect or worker.
- Disposition: `architect`

## Outcome and residual risk

Outcome: `not accepted — escalated`.

The code and tests satisfy AC-01 through AC-06, the versioned patch is correct and scoped, and no functional or security defect was found. Acceptance is nevertheless prohibited because material findings F-01 and F-02 remain. The task-specific single review round is exhausted; any rerun or further review requires a revised/renewed contract rather than an unbudgeted correction round.

Residual risks are limited to: unresolved human authority for the reported deletions; the architect's validation/scope inconsistency; unverified mechanical reviewer and worker permission enforcement; and the inherently unverifiable worker claim that fixture `task.md` was never read. No residual correctness, data-formatting, dependency, localization, concurrency, or public-import risk was identified in the versioned patch.
