# Architecture packet — V02-REAL-019

## Decision

Issue one bounded utility task. Normalize the effective current page inside `generatePagination`: return `[]` immediately when `totalPages` is `0`, and for positive totals clamp `currentPage` into `1..totalPages` before applying the existing pagination branches. Add focused tests in the new authorized test file. Do not change the exported name, signature, valid-input output arrays, ellipsis placement, dependencies, or project configuration.

The adjacent `task.json` is the authoritative machine-readable Task Contract for plan revision 1:

- Run: `v02-real-019-baseline`
- Task: `V02-REAL-019-T1`
- Plan digest: `sha256:e312a82ed74b6eac676f31ab8b634ecfd282e41260f96ba1ed5ea9ed2dd60681`
- Base revision: `bb2558441a6673ab76c89914c25018bffa27a2ba`
- Dependencies: none
- Authorized writes: `dashboard/starter-example/app/lib/utils.ts`, `dashboard/starter-example/app/lib/utils.test.ts`

## Frozen behavior and scope

- `generatePagination(currentPage, 0)` returns `[]` for any ordinary numeric current page.
- When `totalPages` is positive, values below `1` behave exactly as page `1`, and values above `totalPages` behave exactly as page `totalPages`.
- When `1 <= currentPage <= totalPages`, preserve every existing array exactly, including array length, page numbers, ordering, and each `'...'` marker.
- Keep the export named `generatePagination` and its two-number call shape unchanged.
- Use the clamped value consistently for branch selection and any current-page neighbor values.
- Limit writes to the exact implementation and test paths. Do not edit manifests or lockfiles to add a test framework.

The bounded input model is non-negative integer `totalPages` and integer `currentPage`, matching page-count semantics. Defining validation, coercion, or rounding for negative, fractional, `NaN`, or infinite inputs is outside this task.

## Implementation and test shape

Make the smallest local change: handle zero before range clamping, calculate one clamped page for positive totals, and use it wherever the current implementation uses `currentPage`. Do not refactor unrelated currency, date, or Y-axis helpers.

The current branches already yield the requested arrays for ordinary zero and extreme integer examples as an incidental consequence of their thresholds. The task still requires the explicit zero guard and clamped local value so the range invariant is encoded at the utility boundary rather than left implicit. The focused test file must directly assert at least:

- zero pages: `(1, 0) -> []`;
- low clamp: `(0, 10)` equals the existing page-1 array;
- high clamp: `(11, 10)` equals the existing page-10 array; and
- unchanged valid examples covering small totals, the first-page region, a middle page, and the last-page region.

The dashboard starter does not configure a unit-test runner and its dependencies are not authorized to change. Tests should therefore be dependency-free and table-driven where practical. The contract also supplies a non-mutating Node behavior check that executes the self-contained function body from the authorized source and verifies the required representative arrays. This provides direct runtime evidence without changing project configuration.

## Execution waves

1. **Wave 1 — utility and focused tests:** `V02-REAL-019-T1` changes the utility and adds its test file, then runs every required validation and maps evidence to the criteria.
2. **Wave 2 — read-only acceptance check:** verify the diff is confined to the two authorized paths, the export is unchanged, test assertions cover the frozen cases, and all command evidence is passing.

There are no concurrent writers. The implementation and its new regression tests are one atomic task, so `parallel_safe` is false and no same-wave write ownership is authorized.

## Acceptance and evidence

Acceptance requires all four stable criteria in `task.json`. Evidence must include the exact changed-file list, a concise diff summary showing the explicit zero guard and clamped local value, the focused test assertions, passing output and exit status for each required command, and an `AC-1` through `AC-4` mapping. The behavior command covers zero pages, both clamp directions, and representative unchanged valid arrays. Missing or contradictory evidence invalidates completion.

## Risk and routing assumptions

Risk is low and complexity is bounded. The main regression risk is using the unclamped argument in one branch or changing the established valid-input shapes. Route to a bounded non-recursive worker at normal high reasoning under the configured Sol/Luna policy. The preferred model in `task.json` is a policy request only; effective routing and cost remain unverified unless the host supplies trusted metadata. Any request to redefine invalid-number semantics, change the public interface, add a dependency, or broaden scope returns to the architect.

## Human boundaries

No network, credentials, external side effects, destructive actions, dependency installation, or external target access is authorized. The host owns scheduling, isolation, workflow status, and integration. A human decision is required for new authority or destructive behavior; an architect decision is required for broader scope or interface changes.
