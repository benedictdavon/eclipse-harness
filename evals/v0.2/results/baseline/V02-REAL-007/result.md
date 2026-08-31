# Worker result — V02-REAL-007

## Outcome

Implemented the bounded change in the authorized worktree. `User.avatar` now raises `ValueError('size must be positive')` when `size <= 0`, while the existing valid-size digest and URL construction remain unchanged. The existing size-128 assertion was retained, and focused unittest coverage now checks both `0` and `-1` with the exact exception message.

Runtime unittest validation is blocked because the provided Python environment does not contain Flask. No dependencies were installed, as required by the task contract.

## Initial-state evidence

- `git rev-parse HEAD` -> exit 0; `a975ef64864354867c88e0ed3a17ba7d17dca752`
- Initial `git status --short` -> exit 0; no output
- `sha256sum app/models.py tests.py` -> exit 0:
  - `app/models.py`: `07534ea0df91817dc69aff5fb5c2ae5802a322b30cdc892517edf7955cd56bae`
  - `tests.py`: `15a002635f20396831bd523365f0939220fd958c72c48f1c0d3d05ae221aabcc`
- Contract identity matched revision 1 and plan digest `540f490db6d73ed72db7cf53d56367ef0c06e2b9b6bbf983cb053c6beff22afd` in `task.json` and `architect.md`.

## Changed files

- `app/models.py`: added the direct `size <= 0` guard at the start of `User.avatar`.
- `tests.py`: retained the exact size-128 URL assertion and added subtests for `0` and `-1` using an exact-message `assertRaisesRegex` assertion.

No template, SQLAlchemy declaration, migration, dependency, configuration, call-site, or public-signature change was made.

## Required validation

1. `python -m unittest tests.UserModelCase.test_avatar`
   - Exit status: 1
   - Result: blocked during test-module import with `ModuleNotFoundError: No module named 'flask'`; unittest reported `FAILED (errors=1)` before executing the test.
2. `python -m compileall -q app tests.py`
   - Exit status: 0
   - Output: none
3. `git diff --check`
   - Exit status: 0
   - Output: none
4. `git status --short`
   - Exit status: 0
   - Output:
     - ` M app/models.py`
     - ` M tests.py`

## Acceptance evidence

- AC-01: `tests.py` covers sizes `0` and `-1` and checks `ValueError` with exact message `size must be positive`; runtime execution is unverified because the declared unittest command is blocked by missing Flask.
- AC-02: the pre-existing exact URL assertion for `john@example.com` at size 128 remains unchanged; runtime execution is unverified for the same environment blocker.
- AC-03: satisfied by exit status 0 from `python -m compileall -q app tests.py`.
- AC-04: satisfied by the scoped diff and final status showing modifications only to `app/models.py` and `tests.py`.
