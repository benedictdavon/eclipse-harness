# Architect result — V02-REAL-014

Executable multi-file implementation is approved as `V02-REAL-014-T1`; the complete contract is in `task.md`.

## Architecture decisions

- Add optional `RetryOptions.minimumDelayMs?: number`, documented default `0`.
- Normalize omission to `0`; reject a supplied negative value with exactly `Error("retry.minimumDelayMs must be non-negative")`.
- Only when no custom `retry.delay` is supplied, normalize `delay` to the existing exponential value bounded below by `minimumDelayMs`. A custom delay remains authoritative. The existing core order remains unchanged: jitter is applied after this default delay, then `backoffLimit` caps it. Server retry headers and `maxRetryAfter` remain untouched.

Wave 1 contains T1 only. This bounded behavior/type change routes to Luna/high. Effective model and permissions are unverified. No core runtime file, dependency, lockfile, network, install, credential, external-effect, destructive, or other write is authorized.
