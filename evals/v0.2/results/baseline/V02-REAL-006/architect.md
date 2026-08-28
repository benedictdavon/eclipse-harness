# V02-REAL-006 — Architecture and Dispatch Plan

## Outcome

Plan revision 1 is executable as two disjoint task contracts. No implementation was performed. The pinned checkout was inspected read-only, was clean, and matched base revision `672971d66a2ef9f85151e53283113f33d642dabd`.

The machine-readable contracts are:

- `task.json` — `V02-REAL-006-T01`, owner of `tests/test_itsdangerous/test_encoding.py`
- `task-02.json` — `V02-REAL-006-T02`, owner of `docs/encoding.rst`

Each file is a complete Eclipse Task Contract v1.0 containing context, fixed decisions, assumptions, invariants, non-goals, exact write/read/forbidden scope, acceptance criteria with required evidence, validation commands, budgets, authorizations, and stop conditions.

## Plan identity

| Field | Value |
|---|---|
| Run | `V02-REAL-006` |
| Plan revision | `1` |
| Base revision | `672971d66a2ef9f85151e53283113f33d642dabd` |
| Requirement digest | `sha256:5109ffc4a1c59980e30fc27a2ecf1613ad5fa5320a623d97e555251690c99952` |
| Plan digest | `sha256:9ad88fd343a14118432e21b09a2364a152913c6f292f43adf647c99d3fc79d5b` |
| Routing policy | `sol-luna-v0.1` |

The plan digest is SHA-256 over the exact UTF-8 bytes of this canonical, sorted, compact JSON value, with no trailing newline:

```json
{"base_revision":"672971d66a2ef9f85151e53283113f33d642dabd","fixed_decisions":["add decimal 256 as the one-to-two-byte length boundary in the existing parametrized round-trip test","document the RFC 4648 URL-safe alphabet and unpadded encoding behavior without changing runtime code","use two disjoint contracts in one concurrent wave only with host-provided isolated worktrees"],"plan_revision":1,"run_id":"V02-REAL-006","task_ids":["V02-REAL-006-T01","V02-REAL-006-T02"],"waves":[["V02-REAL-006-T01","V02-REAL-006-T02"]]}
```

## Frozen architecture decisions

1. `V02-REAL-006-T01` adds exactly one tuple to the existing `test_int_bytes` parametrization: decimal `256` with expected minimal big-endian bytes `b"\x01\x00"`. This is the first value requiring two encoded bytes. The existing three cases and both exact-output and round-trip assertions remain unchanged.
2. `V02-REAL-006-T02` adds one concise paragraph between the `Encoding Utilities` heading and the existing autofunction directives. It identifies the RFC 4648 URL-safe 64-character alphabet as ASCII letters and digits plus `-` and `_` in place of `+` and `/`; it distinguishes `=` as padding and explains that the encoder strips trailing padding while the decoder restores the padding needed for decoding.
3. No runtime source, API, behavior, dependency, configuration, lockfile, changelog, or unrelated formatting change is authorized.
4. The documentation must not claim strict rejection of every representation outside the helper's documented emitted form; the current decoder implementation does not establish that guarantee.
5. Neither worker may revisit the boundary choice, documentation semantics, scope split, or concurrency design. Any such change requires return to the architect, a new plan revision, and supersession of both nonterminal revision-1 contracts.

## Task summary

| Task | Dependencies | Sole write ownership | Complexity / risk | Required task validation | Budget |
|---|---|---|---|---|---|
| `V02-REAL-006-T01` | none | `tests/test_itsdangerous/test_encoding.py` | trivial / low | packet's focused pytest; `git diff --check`; repository-wide `git diff --name-only` | 2 attempts, 1 review round |
| `V02-REAL-006-T02` | none | `docs/encoding.rst` | trivial / low | `git diff --check`; repository-wide `git diff --name-only`; direct diff/source semantic evidence | 2 attempts, 1 review round |

The contracts use exact-file write globs and authorization targets. `T01` forbids documentation and source writes. `T02` forbids test and source writes. Both have empty `shared_interfaces` and `exclusive_resources` lists.

## Execution waves and concurrency decision

### Wave 1

Run `V02-REAL-006-T01` and `V02-REAL-006-T02` concurrently only when the host provides a separate isolated worktree or equivalent isolated branch workspace to each executor.

This same-wave authorization is justified because:

- both tasks have no dependencies, so the DAG is valid;
- write ownership is exact and disjoint: one test file versus one documentation file;
- neither task changes a shared interface, production source, manifest, migration, lockfile, generated file, or shared exclusive resource;
- task-local validation does not require the other task's change;
- deterministic Eclipse concurrency checking accepts both tasks in one wave with `--max-writers 2`.

If isolated worktrees are unavailable, the host must conservatively serialize the unchanged contracts in integration order `T01` then `T02`; a shared mutable checkout is not authorized for concurrent writers.

### Integration gate

After both task results satisfy their contract evidence, the host integrates `T01` first and `T02` second. The ordering is deterministic for auditability, not a semantic dependency. Then verify the combined tree:

1. `git diff --name-only` lists exactly `docs/encoding.rst` and `tests/test_itsdangerous/test_encoding.py`.
2. `git diff --check -- tests/test_itsdangerous/test_encoding.py docs/encoding.rst` passes.
3. `PYTHONPATH=src python -m pytest tests/test_itsdangerous/test_encoding.py -q` passes exactly as required by the packet.
4. Review the combined diff against all `T01-AC*` and `T02-AC*` criteria, including the documentation claims' correspondence to the unchanged `base64_encode` and `base64_decode` implementations.

Any conflict, extra path, stale base, missing criterion evidence, or contradictory command evidence stops integration and returns to the owning worker or architect within the recorded review budget.

## Evidence expectations

Each worker result must include base-revision verification, an exact `files_changed` list, a focused patch, every required command with exit status and concise output, criterion-by-criterion evidence, and explicit deviations/blockers/observed risks. A result is incomplete if any acceptance criterion lacks direct evidence or any required command lacks passing evidence.

For `T01`, the focused pytest output and retained assertions prove the round trip. For `T02`, the focused prose diff, unchanged directives, repository-wide path list, whitespace check, and direct comparison with the unchanged implementation prove documentation correctness without relying on network access or optional documentation tooling.

## Risk and routing assumptions

Both changes are tiny, deterministic, local, and low risk. Under the configured `sol-luna-v0.1` policy, each contract selects the `worker-lite` profile: executor role, bounded-routine capability tier, low cost tier, medium reasoning effort, and preferred model `gpt-5.6-luna`. The bounded-complex worker profile or manual execution under the identical contract is an allowed fallback.

These are configuration preferences only. The manual adapter supplies no trusted observation of the effective model, permissions, or cost, so none is claimed as verified. Missing tools, dependencies, isolation, or permissions are environment blockers, not reasons to silently increase reasoning or widen scope.

## Human and host boundaries

No human clarification is required to dispatch revision 1 under the fixed decisions above. The host owns scheduling, worktree/branch isolation, git operations, result collection, integration, and final validation. The contracts do not authorize workers to commit, push, install dependencies, access the network, use credentials, create external effects, or perform destructive actions.

Stop and ask the human before granting credentials, destructive actions, external effects, new targets, or expanded authority. Return to the architect for a base-revision mismatch, a changed boundary or documentation meaning, any production/interface/configuration edit, a shared-file requirement, a concurrency redesign, or an unrelated required-validation failure. A verified effective-route guarantee also requires trusted host evidence; it cannot be inferred from the configured policy.

## Architect validation evidence

- Both contract JSON files passed `eclipse validate --kind task`.
- Their canonical Eclipse contract digests are `sha256:b68ec385e2976f8aa71845b0be0be55122de0e33a29fb460faf3d55a1f693406` for `task.json` and `sha256:00f454d0f63f0951cf00080e689970d16ea9c64db08ee4a65f3fce9ed4908310` for `task-02.json`.
- The shared plan digest recomputed from each contract's exact `metadata.plan_digest_input` and matched the declared plan digest.
- The deterministic checker returned one ownership-safe wave: `[["V02-REAL-006-T01", "V02-REAL-006-T02"]]`.

The final contract digests and concurrency output are established by the post-write validation run; no checkout implementation or test execution occurred during architecture.
