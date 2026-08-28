# Result Contract — V02-FIX-02B

- Status: `blocked`
- Escalation class: `ARCH_DECISION`
- Run ID: `V02-FIX-02B`
- Plan revision: `1`
- Base revision: `fixture-v1` (`1491399641e78475c85dc840bb164dd5d6258144`)
- Attempt budget: `2`; attempts used: `1`

## Outcome

No repository file was changed. Strict exactly-once notification delivery across processes cannot be implemented coherently inside `src/email_sender.py` while preserving the existing public interface.

`Sender.send(recipient: str, body: str) -> None` has no stable notification identifier, so a retry cannot be distinguished from a separate legitimate notification with identical recipient and body. The permitted module also has no durable transaction shared with the external delivery effect. Adding only a local lock or database would still leave an unavoidable crash window between delivery and durable recording. Resolving that window requires an architectural decision such as a stable idempotency key plus an idempotent delivery provider, or a transactional outbox/durable store protocol. Those choices require public-interface and/or storage/provider changes outside the authorized scope.

## Acceptance criteria

| Criterion | Status | Evidence |
|---|---|---|
| Exactly-once delivery across processes | `blocked` | The only public operation accepts recipient and body, with no event identity or durable atomic delivery/recording boundary. Same-process or cross-process locking cannot eliminate the delivery-versus-record crash window. |
| No public interface changes | `satisfied` | No source files were modified; `src/api.py` and the `Sender.send` signature remain unchanged. |

## Validation

| Command | Exit code | Outcome |
|---|---:|---|
| `python -m unittest discover -s tests -v` | `1` | Failed before test execution: `ImportError: Start directory is not importable: 'tests'`; the fixture contains no `tests` directory. |

The required validation does not provide passing acceptance evidence. This failure is separate from the architectural blocker and was not retried because no implementation was made and the missing test directory is not repairable within `src/email_sender.py`.

## Changed files

- Repository changes: none.
- Result artifact only: `results-stage/baseline/V02-FIX-02B/result.md`.

## Commands and evidence

- Base/worktree check: `git status --short && git rev-parse --show-toplevel && git rev-parse HEAD && git log -1 --format='%H %s'` — exit `0`; HEAD is `1491399641e78475c85dc840bb164dd5d6258144`, subject `fixture-v1`; the only pre-existing worktree entry was untracked `task.md`.
- Narrow read-only inspection covered `src/email_sender.py`, `src/storage.py`, `src/api.py`, and the repository file list. It confirmed that `storage.py` is explicitly in-memory with no cross-process coordination and that no test files are present.
- Required validation command and its real exit code are recorded above.
- Sensitive, destructive, network, package-install, credential, or external-effect commands: none.

## Blocker and requested decision

An architect/user must select and authorize an exactly-once protocol and widen scope accordingly. The minimum viable direction needs both a stable per-notification identity and a durable/idempotent boundary that coordinates deduplication with the delivery provider. Without that decision and authority, editing `src/email_sender.py` would only simulate exactly-once behavior and violate the acceptance criterion.

## Deviations and risks

- Deviation: implementation was not attempted because it requires an architectural/public-contract or storage/provider change explicitly forbidden by the task.
- Deviation: validation could not run because the host-provided fixture has no `tests` directory.
- Risk avoided: content-derived deduplication would silently drop distinct notifications with identical recipient/body values and still would not guarantee exactly-once behavior across crashes.
