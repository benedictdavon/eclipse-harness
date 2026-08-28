# Result Contract — V02-FIX-01B.task-1

## Binding and outcome

| Field | Value |
|---|---|
| Schema version | `1.0` |
| Run | `V02-FIX-01B` |
| Task | `V02-FIX-01B.task-1` |
| Plan revision | `1` |
| Plan digest | `sha256:24e69bea05c4cdc09d139f68d1cd127991bfee4f4abbf4896ff4261c499ba78f` |
| Required base revision | `027f764ce1251403e5f42e0f5828f6560f49c769` |
| Observed HEAD before edit | `027f764ce1251403e5f42e0f5828f6560f49c769` |
| Status | `completed` |
| Attempts used | `1 of 2` |

The host confirmed the run/case, plan revision and digest, base revision, attempt budget, absence of dependencies, and mutable-checkout permission within the authorized scope. Effective model identity, cost route, and actual permission enforcement were not exposed as trusted host attestation and remain unverified.

## Pre-edit verification

The bounded preflight command completed with exit code `0`. `git rev-parse HEAD` returned the required base revision. The three authorized files matched the context-manifest digests:

| File | Observed SHA-256 |
|---|---|
| `src/pricing.py` | `7778fcb076aa300e8a947c7306db21e8c88b1dffda443b371adf75b37a85e347` |
| `src/__init__.py` | `0d017f2d11599269f6bfa06360a3974b60fd2f4cf747faa8755f317881afe88e` |
| `tests/test_pricing.py` | `3b888fcf3043c1c74c13684d92b964671a83442d0da7c792561784ed70839790` |

Pre-edit `git status --short` showed only the known host/user baseline material:

```text
?? task.md
```

The resolved paths of all three authorized files remained inside the pinned checkout.

## Changes

Task-produced versioned changes are limited to:

- `src/pricing.py` — added `format_total(cents: int) -> str` immediately after `calculate_total`, using a sign plus `divmod(abs(cents), 100)` and fixed two-digit fractional formatting.
- `src/__init__.py` — imported and exported `format_total`, retaining `calculate_total` as the first public name.
- `tests/test_pricing.py` — retained both existing calculation tests and added package-export tests for positive, zero, and negative formatting.

`calculate_total` was not modified. No dependency, localization, coercion, packaging, documentation, or other interface change was introduced.

## Required validation evidence

### `python -m unittest discover -s tests -v`

Exit code: `0` (`passed`)

```text
test_format_total_negative (test_pricing.PricingTests.test_format_total_negative) ... ok
test_format_total_positive (test_pricing.PricingTests.test_format_total_positive) ... ok
test_format_total_zero (test_pricing.PricingTests.test_format_total_zero) ... ok
test_negative_amount (test_pricing.PricingTests.test_negative_amount) ... ok
test_total (test_pricing.PricingTests.test_total) ... ok

----------------------------------------------------------------------
Ran 5 tests in 0.000s

OK
```

### `git diff --check -- src/pricing.py src/__init__.py tests/test_pricing.py`

Exit code: `0` (`passed`)

Output: empty; no whitespace errors.

### `git status --short`

Final invocation exit code: `0` (`passed`)

```text
 M src/__init__.py
 M src/pricing.py
 M tests/test_pricing.py
?? task.md
```

The three modified files are exactly the authorized write globs. `task.md` was present before implementation, remained unread and untouched, and is not task-produced drift.

## Criterion evidence

| Criterion | Result | Direct evidence |
|---|---|---|
| AC-01 | Satisfied | `PricingTests.test_format_total_positive` imports `format_total` from `src` and passed its `format_total(1234) == "$12.34"` assertion in the required suite. |
| AC-02 | Satisfied | `PricingTests.test_format_total_zero` passed its `format_total(0) == "$0.00"` assertion in the required suite. |
| AC-03 | Satisfied | `PricingTests.test_format_total_negative` passed its `format_total(-1) == "-$0.01"` assertion in the required suite. |
| AC-04 | Satisfied | The passing tests import `format_total` from `src`; the scoped diff adds it to both the `.pricing` import and `__all__`, after retained `calculate_total`. |
| AC-05 | Satisfied | The unchanged `test_total` and `test_negative_amount` both passed; the scoped source diff contains no change to `calculate_total`. |
| AC-06 | Satisfied | The scoped source diff uses `divmod(abs(cents), 100)` and `:02d`, with no floating-point, locale, dependency, or out-of-scope versioned change. |

## Additional command and scope evidence

- `git diff -- src/pricing.py src/__init__.py tests/test_pricing.py` exited `0` and showed only the implementation, export, and test additions summarized above.
- The first post-test status audit exited `0` and revealed `src/__pycache__/` and `tests/__pycache__/`, which the required Python command created after the clean baseline check.
- `find src/__pycache__ tests/__pycache__ -maxdepth 1 -type f -print` exited `0` and identified only three generated `.pyc` files.
- Cleanup command `rm -r -- src/__pycache__ tests/__pycache__` exited `0`. It removed only those newly generated, non-source bytecode caches; the subsequent final status audit is recorded above.
- A later fresh-process status reconfirmation recreated the same cache paths as an execution-environment side effect. The same exact cleanup command was run a second time and exited `0`; the immediately subsequent final `git status --short` audit exited `0` with exactly the output recorded above. No further checkout command was run.

## Decisions, deviations, blockers, and escalation

- Implementation decisions followed all fixed contract decisions; no architecture or public-interface decision was improvised.
- Validation side-effect deviation: the contract classified the unittest command as non-mutating, but Python emitted bytecode caches. The exact task-created caches were removed to restore the contracted final scope. Source and tests were not changed after the passing suite.
- Blockers: none.
- Remaining risks: none beyond the contract's already-fixed public export and `-$` negative-sign convention.
- Escalation: none required.
