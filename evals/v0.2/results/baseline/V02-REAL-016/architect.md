# Architect result — V02-REAL-016

Status: bounded worker task approved

Plan revision: 1  
Plan digest: `sha256:d8c84f14a62577ed879859129b1bbb0216eec008094ad415ab719da16cf27665`

## Architecture and scope

This is a behavior-preserving, private refactor. One worker may modify only `source/utils/normalize.ts` and `test/retry.ts` at base revision `3419113b48e034fdcf8fa6bd3be3da7b3d0d758f`. No public API, exported type, default retry value, normalized return shape, dependency, manifest, generated output, or unrelated test may change.

The worker must extract one non-exported helper used by both `methods` and `statusCodes` validation. The helper must preserve the current runtime predicate exactly: a truthy configured value that is not an array is rejected, while the existing behavior for absent or other falsy values is not broadened as part of this refactor. The helper must construct the existing field-specific messages exactly:

- `retry.methods must be an array`
- `retry.statusCodes must be an array`

The existing invalid-value tests should be tightened to assert these exact messages. Existing array normalization, including lowercasing `methods`, and all default object behavior remain untouched.

## Execution decision

The work is one low-risk, bounded task with no dependencies and no parallel writers. It is routed by policy to a bounded worker at the normal implementation tier; the configured model preference is not evidence of the effective runtime model. Network, credentials, destructive actions, external side effects, and writes outside the two approved files are unauthorized.

The task contract is in `task.json`. Stop and return to the architect if exact behavior cannot be retained within the approved files, if a public type or interface must change, or if the base revision is stale.

## Evidence required

Completion requires a two-file-or-smaller changed-file list, direct source evidence that both validations use the same private helper, exact-message assertions for both fields, a passing focused retry test, passing lint and TypeScript checks for the scoped change, and the packet-provided non-empty-file smoke check. Command output must be reported with exit status and mapped to each acceptance criterion.
