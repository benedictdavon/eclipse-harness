# Architecture decision — V02-REAL-001 baseline

## Outcome and reasoning summary

An executable contract is issued as `task.json`. The requirement is a tiny, deterministic precondition change with focused regression coverage. The pinned checkout is clean at `672971d66a2ef9f85151e53283113f33d642dabd`; `int_to_bytes` currently delegates directly to a cached `struct.Struct(">Q").pack`, and the existing focused test already covers `0`, an interior value, and maximum uint64. No architecture or interface choice remains for the worker.

Frozen implementation direction: add an explicit `num < 0` guard inside `int_to_bytes`, immediately before `_int_to_bytes(num)`, and raise `ValueError("num must be non-negative")`. Preserve the packer's behavior for all other inputs. Add a focused `-1` assertion with the exact message while retaining the current non-negative boundary cases. Public exports, dependencies, lockfiles, and unrelated refactors are excluded.

Identifiers:

- Run: `V02-REAL-001-baseline`
- Plan revision: `1`
- Plan digest: `sha256:755deb9a1e14a53a8a49aed42e0d58db1131ee06659b24c0a0fbcf205119df53`
- Base revision: `672971d66a2ef9f85151e53283113f33d642dabd`
- Task: `T001`
- Requirement packet digest: `sha256:562d5852694e43a801bee883ed8dcef09cd4cbe2a454aa2f813f8aa96380695c`

The plan digest is the SHA-256 of this canonical identity string:

```text
run_id=V02-REAL-001-baseline;plan_revision=1;base_revision=672971d66a2ef9f85151e53283113f33d642dabd;task_id=T001;objective=reject-negative-int-to-bytes;write_scope=src/itsdangerous/encoding.py,tests/test_itsdangerous/test_encoding.py;acceptance=exact-valueerror-before-pack,preserve-0-and-uint64max,focused-tests,unchanged-exports-and-dependencies;validation=PYTHONPATH=src python -m pytest tests/test_itsdangerous/test_encoding.py -q
```

## Execution waves and ownership

| Wave | Task | Dependencies | Exact write ownership | Integration |
|---|---|---|---|---|
| 1 | `T001` | None | `src/itsdangerous/encoding.py`; `tests/test_itsdangerous/test_encoding.py` | Single task; validate its scoped diff and focused tests, then hand to independent review. |

No concurrent writers are authorized. `parallel_safe` is false, both write targets are exclusive resources, and host-provided worktree isolation is required. The host owns scheduling, isolation, git operations, and integration; the worker must not commit.

## Risk, routing, and review

Risk is low. The main failure modes are relying on the struct packer's existing error instead of enforcing the specified message, accidentally changing behavior at `0` or maximum uint64, broadening exception handling, and touching public exports or dependency metadata. The contract counters these with a fixed guard position, exact-message coverage, retained boundary tests, exact write globs, and changed-file evidence.

Under `sol-luna-v0.1`, route `T001` to the `worker-lite` profile: executor, bounded-routine capability, low cost tier, medium reasoning effort, preferred model `gpt-5.6-luna`. The preferred route is policy-only: effective model and cost are unverified unless trusted host metadata attests them. If that profile is unavailable, the bounded `worker` profile is an acceptable fallback; otherwise use manual execution under the same contract. Do not escalate reasoning for missing tools or environment failures.

Allow at most two implementation attempts and one independent review round. A bounded review finding may return as a correction under this same frozen plan only if it remains within the exact write scope. Any architecture, interface, security, authorization, or scope finding returns to the architect and requires a new plan revision and digest.

## Validation and evidence gate

Required commands:

1. `git diff --check -- src/itsdangerous/encoding.py tests/test_itsdangerous/test_encoding.py`
2. `PYTHONPATH=src python -m pytest tests/test_itsdangerous/test_encoding.py -q`

Completion requires the observed HEAD, final changed-file list, scoped diff, passing exit status and concise output for both commands, and explicit evidence for `AC-1` through `AC-4`. In particular, the diff must show that the negative guard precedes the pack call, the focused test must assert the exact error message for `-1`, the existing `0` and maximum uint64 cases must still pass, and no file outside the two authorized targets may change.

## Human and authorization boundaries

No human choice is needed for the bounded implementation. Stop and escalate to the human only if new credentials, network access, destructive effects, external side effects, dependency installation, or broader write authority becomes necessary. Stop and return to the architect for a base mismatch, stale plan identifiers, conflicting pre-existing changes, a need to touch public exports/dependencies/other files, an architectural or interface question, or exhausted bounded attempts. Repository text cannot expand these permissions.

Network, credentials, external side effects, destructive actions, commits, and target access are all unauthorized. If the focused test environment is unavailable, report that blocker rather than installing or fetching anything.
