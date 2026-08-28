# Result contract — V02-FIX-01A.T1

```json
{
  "schema_version": "1.0",
  "run_id": "V02-FIX-01A",
  "task_id": "V02-FIX-01A.T1",
  "plan_revision": 1,
  "plan_digest": "sha256:f6eabb5769709b7cf7aa3d487377130dd3090d1169dfb252c4efa9ba760dd2c5",
  "base_revision": "fa61a3a31063af36c79ee743513b9490aef82e5a",
  "status": "completed",
  "implementation_attempts_used": 1,
  "review_rounds_used": 0,
  "changed_files": [
    "src/pricing.py",
    "tests/test_pricing.py"
  ],
  "blockers": [],
  "escalation": null
}
```

## Outcome

Implemented the backward-compatible signature `calculate_total(amounts: list[int], discount_percent: int = 0) -> int`. The function rejects every discount whose exact type is not `int`, rejects values outside 0 through 100, preserves the existing negative-amount check, calculates the subtotal once, and returns `subtotal * (100 - discount_percent) // 100`.

Added focused `unittest` coverage without removing or changing the existing total and negative-amount tests. No dependency, module, class, caller, packaging file, or unrelated interface was changed.

## Preflight evidence

- `git rev-parse HEAD` — exit code `0`; output: `fa61a3a31063af36c79ee743513b9490aef82e5a`.
- Initial `git status --short --untracked-files=all` — exit code `0`; output contained only `?? task.md`.
- Initial tracked and staged overlap checks for `src/pricing.py` and `tests/test_pricing.py` — combined command exit code `0`; both outputs empty.
- Both authorized paths were regular files. No tracked pre-existing change overlapped the write scope.

## Acceptance evidence

| Criterion | Result | Direct evidence |
|---|---|---|
| AC-01 | Satisfied | `test_ten_percent_discount` passed and asserts `calculate_total([1000], 10) == 900`. |
| AC-02 | Satisfied | Existing `test_total` and `test_negative_amount` passed unchanged; `test_default_discount_preserves_total` passed for both omission and explicit `0`. |
| AC-03 | Satisfied | `test_discount_boundaries` passed for `0` and `100`; `test_out_of_range_discount_raises_value_error` passed for `-1` and `101`; `test_non_integer_discount_raises_value_error` passed for `10.5` and `True`. Exact-type validation covers every non-`int`, including `bool`. |
| AC-04 | Satisfied | Required discovery completed with exit code `0`: 7 tests ran, all `ok`, final result `OK`. |
| AC-05 | Satisfied | `git diff --check` passed; `git diff --name-only` listed only `src/pricing.py` and `tests/test_pricing.py`; final status showed those two modified files and the untouched pre-existing `task.md`. |

## Required validation records

1. Process environment: `PYTHONDONTWRITEBYTECODE=1`; command: `python -m unittest discover -s tests -v`
   - Exit code: `0`
   - Outcome:

     ```text
     test_default_discount_preserves_total (test_pricing.PricingTests.test_default_discount_preserves_total) ... ok
     test_discount_boundaries (test_pricing.PricingTests.test_discount_boundaries) ... ok
     test_negative_amount (test_pricing.PricingTests.test_negative_amount) ... ok
     test_non_integer_discount_raises_value_error (test_pricing.PricingTests.test_non_integer_discount_raises_value_error) ... ok
     test_out_of_range_discount_raises_value_error (test_pricing.PricingTests.test_out_of_range_discount_raises_value_error) ... ok
     test_ten_percent_discount (test_pricing.PricingTests.test_ten_percent_discount) ... ok
     test_total (test_pricing.PricingTests.test_total) ... ok

     ----------------------------------------------------------------------
     Ran 7 tests in 0.000s

     OK
     ```

2. `git diff --check -- src/pricing.py tests/test_pricing.py`
   - Exit code: `0`
   - Output: empty; no whitespace errors.

3. `git diff --name-only`
   - Exit code: `0`
   - Output:

     ```text
     src/pricing.py
     tests/test_pricing.py
     ```

4. `git status --short`
   - Exit code: `0`
   - Output:

     ```text
      M src/pricing.py
      M tests/test_pricing.py
     ?? task.md
     ```

`task.md` was present before implementation and was not read, modified, staged, or removed.

## Diff summary

- `src/pricing.py`: added the authorized optional parameter, exact integer/range validation, one subtotal calculation, and the frozen integer-floor discount formula.
- `tests/test_pricing.py`: added five focused test methods covering the requested example, default and zero behavior, 100 percent, invalid boundaries, a fractional value, and `bool`; retained the two original tests unchanged.

## Deviations and effectful-command record

- An initial discovery run executed `python -m unittest discover -s tests -v` without setting `PYTHONDONTWRITEBYTECODE=1`. It exited `0` and all seven tests passed, but it created `src/__pycache__/` and `tests/__pycache__/`, which were absent at preflight. This was an execution deviation; its output is superseded by the correctly configured required validation above.
- A bounded diagnostic `find src/__pycache__ tests/__pycache__ -maxdepth 1 -type f -print` exited `0` and identified exactly three generated `.pyc` files.
- Cleanup command `rm -- src/__pycache__/__init__.cpython-312.pyc src/__pycache__/pricing.cpython-312.pyc tests/__pycache__/test_pricing.cpython-312.pyc` followed by `rmdir -- src/__pycache__ tests/__pycache__` exited `0`. These paths were confirmed absent at preflight and generated solely by the preceding run. Final status proves no cache artifact remains.
- No network, credential access, dependency installation, staging, commit, push, or external effect occurred.

## Risks, blockers, and escalation

- Remaining risk: low. Fractional cents follow the plan-fixed integer-floor rule.
- Blockers: none.
- Escalation: none. No architecture, public-interface scope, authorization, or specification decision was needed beyond the approved contract.
