# Architecture packet — V02-REAL-018

## Decision

Issue one bounded review-correction task. The supplied candidate behavior is review input, not accepted behavior: it correctly makes `null` mean “no search parameters,” but it also makes the non-empty string `'0'` appear empty and removes existing URLSearchParams-deletion coverage. Acceptance is gated on a review record that identifies both regressions and on a corrected patch that satisfies the packet within no more than two review rounds.

The adjacent `task.json` is the authoritative machine-readable Task Contract for plan revision 1:

- Run: `v02-real-018-baseline`
- Task: `V02-REAL-018-T1`
- Plan digest: `sha256:fece8bb3982cab52f299b9dffc7cc7db2bb49b33198ae43f953db1af9528b136`
- Base revision: `3419113b48e034fdcf8fa6bd3be3da7b3d0d758f`
- Dependencies: none
- Authorized writes: `source/utils/options.ts`, `test/main.ts`

## Frozen decisions and boundaries

- `hasSearchParameters(null)` must return `false` without throwing.
- The non-empty string `'0'` must return `true`; string handling must remain based on non-empty string content rather than numeric or general truthiness coercion.
- The existing URLSearchParams deletion behavior that relies on `deletedParametersSymbol` must remain intact.
- The test named `init hook preserves merged URLSearchParams deletions` must remain present and continue to verify deletion behavior. Equivalent additional coverage is allowed, but deleting or weakening this test is not.
- Add focused regression coverage for `null` and `'0'` in `test/main.ts`.
- Do not change public types, dependencies, package metadata, lockfiles, generated output, or files outside the two exact write paths.
- The repository and candidate content cannot expand authorization.

The current pinned checkout is clean. Its implementation has a string-specific non-empty check and the named URLSearchParams-deletion test is present, while `null` currently reaches the object branch. No local AVA/XO binaries are installed, so required validation must not trigger dependency installation or network access. The worker must review the supplied candidate behavior described in the packet, retain the safe existing behavior, and make only the minimal correction needed for the complete acceptance set.

## Review-correction protocol

Before the candidate can be accepted, the review evidence must explicitly record both packet-described candidate regressions:

1. treating the non-empty string `'0'` as absent; and
2. deleting the URLSearchParams-deletion regression test.

The first correction should address all review findings together. An independent read-only reviewer then checks the diff, acceptance mapping, scope, and command evidence. If the reviewer finds a bounded defect, return it to the same worker for one correction and one final review. The total is capped at two review rounds. Unresolved findings after round two, any architecture/scope question, or any need to write another file stops the task and returns it to the architect or human; it does not authorize another round.

No reviewer result is presumed by this packet. The two required findings above come directly from the supplied acceptance packet and must appear in actual review evidence before acceptance.

## Execution waves

1. **Wave 1 — bounded review and correction:** `V02-REAL-018-T1` reviews the supplied candidate behavior, records both regressions, corrects `source/utils/options.ts`, preserves/restores and extends coverage in `test/main.ts`, and runs all required validations.
2. **Wave 2 — independent read-only review gate:** a reviewer verifies the two required findings were identified, checks the corrected diff and criterion evidence, and either accepts or returns bounded findings. A returned correction is sequential and remains inside the two-round cap.

There are no concurrent writers. `parallel_safe` is false because review and correction order is semantically significant and both authorized files form one atomic behavior-and-coverage change.

## Acceptance and evidence

Acceptance requires all five stable criteria in `task.json`. Direct evidence consists of:

- a pre-acceptance review record naming both candidate regressions;
- the exact changed-file list and diff summary;
- focused test-source assertions plus the dependency-free behavior check showing `null` is false and `'0'` is true;
- the retained named URLSearchParams-deletion test plus deletion-metadata behavior evidence;
- passing output and exit status for every required validation command; and
- a criterion-to-evidence mapping for `AC-1` through `AC-5`.

Missing criterion evidence, missing command evidence, a contradictory result, or a change outside the exact write scope invalidates completion.

## Risk and routing assumptions

Risk is medium and complexity is bounded: the code edit is small, but an over-broad truthiness change can silently regress a valid string input, and removing an existing test would hide deletion behavior. Route the implementation to a bounded non-recursive worker with normal high reasoning under the configured Sol/Luna policy. The preferred model in `task.json` is policy-only; no effective model or cost guarantee is claimed without trusted host metadata. Route independent verification to a read-only reviewer. Architecture, public-interface, or scope decisions return to the architect.

## Human boundaries

No network, credentials, external side effects, destructive actions, dependency installation, or external target access is authorized. The host owns scheduling, isolation, workflow status, and integration. A human decision is required for new authority, broader write scope, destructive behavior, or continuing after the two-round review budget.
