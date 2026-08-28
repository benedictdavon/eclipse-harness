# Architecture plan — V02-REAL-023

## Plan identity

- Run: `V02-REAL-023`
- Revision: `1`
- Base revision: `bb2558441a6673ab76c89914c25018bffa27a2ba`
- Plan digest: `sha256:aeadfd362074d91a308f14247ef296f25b29cfbb135aa6afcf52ae65190de575`
- Task contracts: `task.json` (`V02-REAL-023-T1`) and `task-2.json` (`V02-REAL-023-T2`)

## Decomposition and frozen ownership

The requirement decomposes into two semantically independent tasks in different example trees:

| Task | Exclusive write ownership | Fixed outcome |
| --- | --- | --- |
| `V02-REAL-023-T1` | `dashboard/starter-example/app/lib/utils.test.ts` | Cover `generateYAxis([])` and preserve its current empty-input result: empty labels and `topLabel === Number.NEGATIVE_INFINITY` |
| `V02-REAL-023-T2` | `basics/typescript-final/components/date.tsx`, `basics/typescript-final/components/date.test.tsx` | Ensure and cover a semantic `time` element whose `dateTime` is the original `dateString` and whose visible text remains formatted as `LLLL d, yyyy` |

The pinned `date.tsx` already contains `<time dateTime={dateString}>`. T2 must retain that compliant implementation and add focused coverage; it should not create source churn merely to claim the semantic change. Both example packages lack a configured test runner, so each task uses dependency-free `node:test` source-contract coverage and must not modify manifests, lockfiles, or shared tooling.

## DAG, conditional parallel wave, and isolation

Both tasks have no dependencies. Their write globs, read trees, interfaces, generated build directories, and package-local validation resources are disjoint. They are therefore eligible for the same parallel wave only under all of these conditions:

1. The host creates a separate clean worktree for each task at the pinned base revision.
2. Each executor receives only its own contract and stays within its example tree.
3. No root-level formatter, package install, lockfile operation, or shared workspace command runs concurrently.
4. Existing dependencies, if needed for type-checking, are provisioned without task-authorized network access or repository mutation.
5. The host's deterministic ownership check confirms the globs remain disjoint.

| Wave | Tasks | Mode |
| --- | --- | --- |
| 1 | `V02-REAL-023-T1`, `V02-REAL-023-T2` | Parallel only when all five isolation conditions hold; otherwise execute sequentially in task order |
| Integration | T1 patch, then T2 patch | Host-controlled application to a clean checkout; reject any path outside the owning contract |

After integration, run T1's dashboard validation and T2's TypeScript-example validation separately and sequentially, then run the packet file-presence command once against the combined tree. A failure in one example does not authorize edits in the other example.

## Routing, risk, and human boundaries

- Route recommendation for each task: bounded executor, Luna high under `sol-luna-v0.1`. The manual adapter provides no trusted effective-model observation, so this is a policy recommendation rather than a verified route.
- Risk is low. The main risks are accidental source behavior changes in the test-only dashboard task, pointless churn in the already-compliant date component, and unsafe workspace-level validation during parallel execution.
- Executors are non-recursive. They may not coordinate edits, expand ownership, add test tooling, install dependencies, use the network, or write generated output.
- A required source-behavior change in `utils.ts`, a date API/format decision, a package/tooling change, a concurrency conflict, or any new authority returns to the architect or human rather than being improvised by a worker.
