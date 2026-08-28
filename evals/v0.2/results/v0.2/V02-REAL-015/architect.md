# Architect result — V02-REAL-015

Executable bounded bug fix is approved as `V02-REAL-015-T1`; the complete contract is in `task.md`.

## Diagnosis and fixed design

`hasSearchParameters` excludes only `undefined`; `null` reaches the `typeof search === 'object'` branch and `Object.keys(null)` throws. Extend only the empty guard to include `null`. Keep the typed signature unchanged, preserve string truth testing (`'0'` is true), and do not reorder the `URLSearchParams` branch whose deletion-marker handling makes an otherwise empty instance actionable.

Wave 1 contains T1 only. This low-risk bounded fix routes to Luna/high. Effective model and permissions are unverified. No public type, merge/core logic, dependency, lockfile, network, install, credential, external-effect, destructive, or other write is authorized.
