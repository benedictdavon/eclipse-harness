# V02-REAL-013 architecture plan

## Decision

Issue one bounded worker contract, `V02-REAL-013-negative-numeric-retry`, owning exactly `source/utils/normalize.ts` and `test/retry.ts`.

A second task is not warranted. The production guard and its focused assertions are one semantic unit, both changes are small, and splitting source from tests would create a dependency and an avoidable temporary interface/evidence mismatch. The single task is not parallel-safe with another writer to either owned file.

## Frozen plan identity

- Run: `V02-REAL-013-baseline`
- Revision: `1`
- Plan digest: `f132d47154c7343a44f87e1d233c2525645f0af57af8469d6832dcadf978bda4`
- Base revision: `3419113b48e034fdcf8fa6bd3be3da7b3d0d758f`
- Source requirement digest: `e661ca4c8639badfbb9ede2e45c8b5766aa3222b10d3eeeba05f325476d819e5`
- Complete machine-readable contract: `task.json`

Any architecture, option-type, or acceptance change requires a new plan revision and digest and supersedes this nonterminal contract.

## Frozen behavior and compatibility boundary

Inside only the existing `typeof retry === 'number'` branch, `retry < 0` must throw `new Error('retry limit must be non-negative')` before normalized options are constructed.

The guard deliberately does not apply to object-form `retry.limit`. Zero, negative zero, positive values, positive infinity, and `NaN` retain their existing numeric normalization because the requirement is limited to values for which JavaScript's `< 0` comparison is true. No integer or finite-number requirement is added.

The object branch, defaults, undefined filtering, method lowercasing, array checks, extension behavior, and public `number | RetryOptions`/`RetryOptions.limit?: number` types are fixed compatibility boundaries and must not change.

Focused tests directly exercise `normalizeRetryOptions` without HTTP or network activity:

- `-1`, `-0.5`, and `Number.NEGATIVE_INFINITY` each throw the exact error.
- `0` and a positive value normalize to the supplied limit.
- One representative object input retains its limit and option fields.

Existing positive numeric, numeric-zero, numeric-to-object extension, and object-option tests remain intact.

## Execution wave

### Wave 1 — single isolated worker

- Dispatch `task.json` from the clean base revision in a host-provided worktree.
- Verify run ID, revision, digest, base revision, and clean initial state before editing.
- Permit writes only to `source/utils/normalize.ts` and `test/retry.ts`.
- Run every required command in the contract and return criterion-indexed evidence.
- Do not install dependencies, use a package-manager fetch path, generate `distribution`, use the network, change types, weaken tests, or expand scope.

No merge ordering or concurrency check beyond the single task is needed. The host still owns isolation, scheduling, integration, and workflow state.

## Validation and evidence gate

The packet's exact dependency-free validation is required, as are Node syntax checks for both edited TypeScript files, `git diff --check`, and an unfiltered changed-path report.

The pinned checkout has no `node_modules`, dependency lockfile, or authorization to install packages. Therefore the local AVA command is conditional and non-required: run it only if the host separately preprovisions an executable `./node_modules/.bin/ava`; never fetch or install it. If a human or downstream gate requires executed AVA evidence, dependency provisioning or installation authority must be resolved outside this worker contract before dispatch/completion.

The result is acceptable only when:

- `RETRY-1` through `RETRY-5` each have direct satisfied evidence.
- Every required command has its exact command, exit status, and pass/fail summary recorded.
- The source diff shows the exact-error guard confined to the numeric branch.
- The test diff contains focused exact-message and preservation assertions and does not weaken existing coverage.
- Public types, object normalization, defaults, configuration, dependencies, and all other paths have no diff.

Missing criterion evidence, missing required command evidence, contradictory output, stale plan identity, base mismatch, or path expansion makes the result incomplete.

## Routing and budgets

Under `sol-luna-v0.1`, this is a normal bounded TypeScript implementation routed policy-only to Luna/high. No trusted host metadata proves the effective model, so this is a requested profile, not an effective-route or cost claim. An equivalent host-verified worker profile is acceptable if it provides the contract's TypeScript, numeric-edge-case, and AVA test-design capabilities.

The worker has at most two implementation attempts and one review round. A bounded defect may become a correction contract within that budget. Public-interface, scope, security, architecture, or validation-authority findings return to the architect.

## Risk and human boundaries

Risk is medium because a previously accepted public option now throws synchronously, while nearby numeric cases and object-form behavior must remain unchanged. The change is otherwise local and has no database, migration, external-service, secret, or destructive dimension.

Human authority is required before dependency installation, network access, credentials, external effects, destructive actions, generated distribution changes, writes outside the two authorized paths, or any modification to public types/object semantics. Missing local AVA dependencies are an environment boundary to report, not permission to install or broaden scope.
