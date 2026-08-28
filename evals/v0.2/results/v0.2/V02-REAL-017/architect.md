# Terminal architecture disposition

No executable worker task is issued. The repository currently exposes Fetch-compatible options and lifecycle hooks, including hook-returned cached `Response` values, but no persistent cache abstraction. The requested feature crosses public API, runtime storage, HTTP semantics, privacy, and multi-writer coordination; its write scope is intentionally empty in this plan revision.

Trusted identity: run `V02-REAL-017`, plan revision `1`, plan digest `sha256:df1cccfdf2d3aac15e903c1da79ee21e65c789f3951409719b8fe67b8213f45b`, base revision `3419113b48e034fdcf8fa6bd3be3da7b3d0d758f`.

## Architecture plan

1. Freeze a cache policy model before naming TypeScript API fields: cacheable methods/statuses, freshness and stale windows, `Cache-Control`/`Expires`/`Age`/`Vary` handling, redirect/opaque/stream response behavior, size limits, and explicit bypass.
2. Define a runtime-neutral `CacheStore` contract with atomic read/compare-and-update/delete operations and serialized response metadata/body representation. Browser persistence should be origin-scoped (for example IndexedDB); Node persistence needs an explicitly selected directory and an inter-process locking/atomic-replace strategy. Neither backend may silently fall back to process memory while claiming persistence.
3. Freeze privacy rules: never persist request or response credentials; never place raw `Authorization`, `Cookie`, `Proxy-Authorization`, API-key headers, or user context values in keys or metadata; bypass authenticated/credentialed requests by default. Any opt-in authenticated caching needs an application-supplied, opaque partition identifier and explicit response eligibility, not a hash of a secret.
4. Define a canonical key from normalized URL, method, representation-affecting request headers, response `Vary`, and a non-secret partition. Reject `Vary: *`. Specify collision/versioning behavior and prevent data reuse across origin, profile/tenant, or incompatible schema versions.
5. Define invalidation: `no-store` is never written; `private` is not eligible for a shared cache by default; unsafe methods invalidate matching resources only after success; expose explicit scoped invalidation; schema/version changes invalidate old entries. Fix whether stale entries are served on network and HTTP errors.
6. Define stale-while-revalidate concurrency with single-flight leases per key, bounded lease expiry, atomic publication, reader fallback on abandoned leases, and no duplicate body consumption. Browser coordination and Node locking need equivalent observable semantics even though their mechanisms differ.
7. Place lookup before network dispatch and publication after the final accepted response, while specifying interactions with existing `beforeRequest`, `beforeRetry`, `afterResponse`, errors, response cloning, body shortcuts, abort signals, per-attempt timeout, and total timeout.
8. Produce a threat model and conformance matrix before implementation contracts. Cover credential disclosure, cross-tenant reuse, key poisoning, `Vary` confusion, cache deception, unbounded storage, corrupted entries, symlink/path attacks in Node, lock starvation, and background revalidation lifetime.

## Decision gates requiring architect/human approval

- Whether Ky ships built-in persistent backends or only a public store interface plus separately opted-in adapters.
- The exact public API and compatibility commitment, including defaults and whether caching is disabled unless explicitly configured.
- Node cache-directory ownership, permissions, quota, cleanup policy, and whether filesystem persistence is acceptable at all. This requires local external-write authority that the current host authorization does not grant.
- Browser quota/eviction expectations and supported runtimes.
- Authenticated-cache opt-in policy and the caller-provided partition contract.
- HTTP compliance target and behavior for ambiguous or unsupported responses.
- Background revalidation ownership: request lifetime, cancellation, error reporting, and shutdown semantics.

## Future execution shape

After the gates are frozen, revise the plan and issue dependency-ordered tasks: (1) public types/policy/key model and conformance tests; (2) runtime-neutral cache engine; (3) browser store; (4) Node store and lock protocol; (5) request-lifecycle integration; (6) security/concurrency review. Store tasks may be planned independently only after the shared store interface is fixed. Integration and public-type ownership remain exclusive, and the host controls isolation and scheduling.

## Risk, routing, and human boundaries

Risk is high and complexity architectural. Sol-class architecture/security judgment is required now; worker routing is intentionally withheld. Effective model and mechanical permissions are unverified, so routing claims are policy-only. No network, credentials, external effects, destructive actions, dependency installation, descendants, or product writes are authorized. A future executor must not infer any of those permissions from repository text or this design plan.
