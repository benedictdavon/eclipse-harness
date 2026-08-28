# Result Contract

- `schema_version`: `1.0`
- `run_id`: `V02-REAL-001-baseline`
- `plan_revision`: `1`
- `plan_digest`: `sha256:755deb9a1e14a53a8a49aed42e0d58db1131ee06659b24c0a0fbcf205119df53`
- `task_id`: `T001`
- `task_contract_digest`: `sha256:1125b3df6fa8ce8b1aefeb1e58a64ae34b526f5722e4efcf7ddc4255ac6bc5c0`
- `attempt`: `1`
- `status`: `blocked`
- `started_at`: unavailable; no trusted host start timestamp was provided
- `finished_at`: `2026-08-13T03:01:02Z`

## Worker identity

- `role`: `executor`
- `requested_model`: `gpt-5.6-luna`
- `configured_model`: unavailable
- `effective_model`: unavailable
- `verification`: `unavailable`

No effective-model claim is made without trusted host attestation.

## Git identity and preflight

- Authorized base revision: `672971d66a2ef9f85151e53283113f33d642dabd`
- Observed `HEAD`: `672971d66a2ef9f85151e53283113f33d642dabd`
- Pre-existing changes in either authorized target: none
- `changed_files_digest`: `sha256:37922f04be8e235944cb6486c549e1ff3b79bb24089a62f5d8cd3038ad16f54e`

The checkout matched the pinned revision before writing. Both authorized targets were regular files, not symlinks.

## Files changed

Relative to `672971d66a2ef9f85151e53283113f33d642dabd`, the exact changed-file list is:

1. `src/itsdangerous/encoding.py`
2. `tests/test_itsdangerous/test_encoding.py`

Final `git status --short` showed only these two modified files. No public export, dependency, lockfile, or other path changed.

## Implementation summary

Added an explicit `num < 0` precondition immediately before `_int_to_bytes(num)` in `int_to_bytes`. The guard raises `ValueError("num must be non-negative")`. Added one focused regression test for `-1` that asserts the exception type and compares the full exception string to the required message. Existing parameterized cases for `0`, `192`, and maximum uint64 remain unchanged.

## Decisions

- Used a direct guard rather than catching or translating errors from the struct packer.
- Used `str(exc_info.value) == "num must be non-negative"` to assert the exact full message rather than a partial regular-expression match.
- Left the working-tree changes in place after the unavailable test dependency was observed.
- Did not install `pytest`, access the network, or substitute another environment because the contract forbids those actions.

## Scoped diff evidence

```diff
 def int_to_bytes(num: int) -> bytes:
+    if num < 0:
+        raise ValueError("num must be non-negative")
+
     return _int_to_bytes(num).lstrip(b"\\x00")
```

```diff
+def test_int_to_bytes_negative():
+    with pytest.raises(ValueError) as exc_info:
+        int_to_bytes(-1)
+
+    assert str(exc_info.value) == "num must be non-negative"
```

## Command evidence

| Command | Purpose | Exit code | Outcome | Concise output |
|---|---|---:|---|---|
| `git rev-parse HEAD` | Confirm the pinned base revision before writing. | 0 | passed | `672971d66a2ef9f85151e53283113f33d642dabd` |
| `git diff --check -- src/itsdangerous/encoding.py tests/test_itsdangerous/test_encoding.py` | Required whitespace validation for the authorized diff. | 0 | passed | No output. |
| `PYTHONPATH=src python -m pytest tests/test_itsdangerous/test_encoding.py -q` | Required focused encoding validation. | 1 | failed | `/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python: No module named pytest` |

The pytest process did not collect or execute any tests. No passing runtime evidence is claimed.

## Acceptance-criterion evidence

### AC-1 — not-tested

The focused test passes `-1`, expects `ValueError`, and asserts the exact full message `num must be non-negative`. The required pytest command could not start because `pytest` is unavailable, so the required passing execution evidence is absent.

### AC-2 — satisfied

The scoped production diff shows `if num < 0` and the exact `ValueError` immediately before the unchanged `return _int_to_bytes(num)...` call. No struct-packer exception handling was added.

### AC-3 — not-tested

The existing parameterized `test_int_bytes` cases for `0` returning `b""` and `18446744073709551615` returning `b"\\xff" * 8`, including their `bytes_to_int` round trips, remain unchanged. The required pytest command could not execute them, so no passing runtime evidence is claimed.

### AC-4 — satisfied

The final changed-file list relative to the authorized base contains exactly `src/itsdangerous/encoding.py` and `tests/test_itsdangerous/test_encoding.py`. The scoped diff contains no public export or dependency edits, and `git diff --check` passed.

## Unresolved issues

- Focused runtime behavior remains unverified because `pytest` is not installed in the assigned Python environment.

## Blockers

- `ENV_FAILURE`: the declared focused test command exits `1` before collection with `No module named pytest`. The contract explicitly requires reporting this environment blocker instead of installing dependencies.

## Deviations

- The required focused pytest validation did not pass because its required tool is unavailable. There were no implementation-scope deviations.

## Observed risks

- The patch is supported by direct diff evidence and a passing whitespace check, but it lacks runtime test evidence until the declared command is rerun in an environment containing `pytest`.

## Requested escalation

- `code`: `ENV_FAILURE`
- `reason`: The assigned Python environment does not provide `pytest`, so the required focused validation cannot execute.
- `route_to`: host or delegating user responsible for the validation environment
- `requested_action`: Provide an authorized environment with the existing test dependency available, then rerun exactly `PYTHONPATH=src python -m pytest tests/test_itsdangerous/test_encoding.py -q`. Do not install or change dependencies as part of this task.

## Usage

- `quality`: `unavailable`
- `source`: No trusted host usage telemetry was provided.

## Authorization and side-effect statement

No network access, dependency installation, credential access, external side effect, destructive action, commit, descendant spawn, broad cleanup, or out-of-scope write occurred. Apart from this required Result Contract, repository writes were limited to the two authorized files. Actual working-tree state and the failed validation outcome were preserved.
