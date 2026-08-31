# Architecture plan — V02-REAL-022

## Plan identity

- Run: `V02-REAL-022`
- Revision: `1`
- Base revision: `bb2558441a6673ab76c89914c25018bffa27a2ba`
- Plan digest: `sha256:67f185f55eb073743e01fee877a73529b10fabfd7df03466657b217d8b1d9c6c`
- Task contract: `task.json` (`V02-REAL-022-T1`)

## Frozen architecture and scope

This is one bounded, behavior-preserving refactor. Keep the existing default export and the public prop type `{ status: string }`. Replace the duplicated pending/paid conditionals with one typed, internal status-to-presentation mapping. The mapping owns the label, pill classes, icon component, and icon classes for exactly `pending` and `paid`; it must not add a public status, change the prop type, or export a new API.

The observable contract is exact:

| Status | Label | Pill classes | Icon | Icon classes |
| --- | --- | --- | --- | --- |
| `pending` | `Pending` | `bg-gray-100 text-gray-500` | `ClockIcon` | `ml-1 w-4 text-gray-500` |
| `paid` | `Paid` | `bg-green-500 text-white` | `CheckIcon` | `ml-1 w-4 text-white` |

The shared base pill classes remain `inline-flex items-center rounded-full px-2 py-1 text-xs`. Any other string retains current behavior: only the base span is rendered, with no status label, icon, or status-specific classes.

Only these files may be written:

- `dashboard/starter-example/app/ui/invoices/status.tsx`
- `dashboard/starter-example/app/ui/invoices/status.test.tsx`

The example has no configured test runner. Focused coverage must therefore use dependency-free `node:test` source-contract assertions in a JS-compatible `.tsx` file to detect drift in both labels and all exact class fragments. Adding a test dependency or changing a package manifest/lockfile is outside this plan.

## Execution wave

| Wave | Task | Isolation | Dispatch condition |
| --- | --- | --- | --- |
| 1 | `V02-REAL-022-T1` | Dedicated worktree at the pinned base revision | Contract digest/revision match and the worktree is clean |

There is no useful writer parallelism inside this task: implementation and its focused contract test concern the same component and mapping. The host owns worktree creation, execution, and integration.

## Validation and evidence

The executor must run the focused `node:test`, TypeScript checking for `dashboard/starter-example`, the packet's file-presence command, and `git diff --check`. Completion evidence must map every acceptance criterion to a passing command or a direct diff observation and list the changed files. Missing local dependencies are an environment blocker; they do not authorize network access or manifest changes.

## Routing, risk, and human boundaries

- Route recommendation: bounded executor, Luna high under policy `sol-luna-v0.1`; this is policy-only because the manual adapter does not provide trusted effective-model verification.
- Risk: low. Primary risks are subtle class/label/icon drift, accidentally narrowing the public prop type, and changing unknown-string behavior.
- No network, credentials, external effects, destructive actions, dependency installation, package changes, or writes outside the two owned files are authorized.
- The executor is non-recursive and must stop for any requested public API decision, new status, test-tooling addition, or broader cleanup. Architecture changes return to the architect; new authority returns to the human.
