# Architect result — V02-REAL-017

Status: terminal architecture plan; no implementation task authorized

Plan revision: 1  
Plan digest: `sha256:3d21e0f8dd7b1f310eb61a3857a726431e216894ac9a0fb42ac0d0f3f33ac3f2`

Base revision: `3419113b48e034fdcf8fa6bd3be3da7b3d0d758f`

## Decision

The persistent response cache is an explicit, cross-runtime Ky facility with separate browser and Node storage adapters. “Shared” means browser tabs and workers in the same origin/profile share one browser cache, while Node processes pointed at the same local cache directory share one Node cache. It does not mean that a browser and a Node process share one physical store.

The architecture is resolved, but this packet has an empty implementation write scope and asks for an architecture result. No worker task is emitted. Implementation requires a later plan revision with explicit source, test, documentation, package-export, and generated-output ownership.

No human escalation is required for the design itself. A human must separately authorize any future implementation scope and any dependency or package-engine change; this design does not require a runtime dependency or an engine change.

## Public API — fixed

The existing `RequestInit.cache` option remains a native Fetch option with its current string union and forwarding behavior. Ky must not overload it with a cache object. The new opt-in option is named `responseCache`:

```ts
type ResponseCacheOptions = {
	store: ResponseCacheStore;
	freshFor?: number;
	staleFor?: number;
	partition?: string | ((request: Request) => string | undefined | Promise<string | undefined>);
	varyHeaders?: readonly string[];
	maxBodyBytes?: number;
	revalidateTimeout?: number;
	backgroundTask?: (task: Promise<void>) => void;
	onCacheError?: (event: {operation: CacheOperation; error: unknown}) => void;
};

type KyOptions = {
	// Existing fields...
	responseCache?: false | ResponseCacheOptions;
};
```

The option is disabled by default. `store` is required whenever it is enabled; Ky never chooses a disk directory or persistent browser database implicitly. Durations are milliseconds. `freshFor` and `staleFor` override response freshness directives when supplied; otherwise Ky uses `Cache-Control: max-age` and `stale-while-revalidate`, with `Expires` as the freshness fallback. A response with no positive fresh or stale window is not retained. `maxBodyBytes` defaults to 10 MiB and is enforced while consuming the cache clone. `revalidateTimeout` defaults to 10 seconds and is independent of the completed caller request.

Root exports add the option, store, record, selector, and event types plus an environment-neutral `invalidateResponseCache(store, input, options?)` helper. Runtime adapters use separate exports so the browser entry never imports Node built-ins:

- `ky/cache/browser` exports `createBrowserResponseCache({namespace, maxEntries, maxBytes})`.
- `ky/cache/node` exports `createNodeResponseCache({directory, namespace, maxEntries, maxBytes})`.

Both factories return `ResponseCacheStore`. Both default to 1,000 entries and 100 MiB, perform best-effort least-recently-used eviction after commits, and expose `clear()`. `invalidateResponseCache` invalidates `GET` and `HEAD` variants for the supplied final URL; callers may narrow by method and partition. Omitting a partition invalidates every partition for that resource.

The public low-level store contract is asynchronous and versioned. It reads candidate variants by opaque resource digest, atomically replaces one immutable variant record, manages namespace/resource/partition generation tokens, invalidates by opaque selector, and clears the namespace. Raw request URLs, request header values, and credentials are never arguments to persistence methods. A custom adapter must provide the same atomic-visibility and generation-fencing semantics as the first-party adapters.

`ky.create()` and `ky.extend()` shallow-merge the `responseCache` policy while retaining `store` by reference. `store` is an atomic value, not deep-merged or cloned. `responseCache: false` disables an inherited cache. Init-hook option cloning retains the store reference and clones only the policy arrays such as `varyHeaders`.

## Storage — fixed

### Browser

The browser adapter uses IndexedDB, not `localStorage` and not the Cache API. IndexedDB supplies persistent binary records, indexed variant lookup, atomic read/write transactions, and visibility across same-origin tabs, dedicated workers, and service workers. The database name is derived from a validated namespace and includes the record schema major version. Upgrades use a new schema store and may delete only this adapter’s older namespaced stores.

### Node

The Node adapter uses an explicitly supplied local directory and no third-party dependency. Every variant is a single versioned binary envelope containing a bounded JSON metadata prefix and body bytes. A write creates a uniquely named temporary file in the same directory, applies file mode `0600`, flushes and closes it, then atomically renames it over the target. The directory is created with mode `0700`. Temporary files are ignored by readers and cleaned opportunistically. The adapter rejects symlink entries and never follows a cache record outside the resolved configured directory.

This yields atomic old-or-new visibility to all Node processes sharing that directory. The supported contract is a local filesystem with atomic same-directory rename; network filesystems that do not provide that guarantee require a custom adapter.

### Record format

Each record contains:

- schema version, namespace epoch, resource generation, and partition generation;
- opaque resource, partition, and variant digests;
- status, status text, safe response headers, response type, and body bytes;
- `storedAt`, `validatedAt`, `freshUntil`, `staleUntil`, and last-access time;
- `Vary` header names and opaque request-header fingerprints;
- `ETag` and `Last-Modified` validators when present.

The adapters do not claim encryption at rest. Browser origin/profile protection and Node directory permissions are the baseline. Applications that need encrypted persistence must supply a custom store. This limitation is documented next to credential partitioning, not hidden as an implementation detail.

## Eligibility and cache semantics — fixed

Only finalized `GET` and `HEAD` requests are eligible. Lookup occurs after every `beforeRequest` hook, so URL, method, and headers used for policy and keying are the actual outgoing values. A `Response` returned by a `beforeRequest` hook is never persisted by this facility.

Only non-redirected, non-opaque 2xx transport responses within `maxBodyBytes` are stored. Ky never stores responses with `Cache-Control: no-store`, `Vary: *`, or unsafe/invalid serialization metadata. `Cache-Control: private` is stored only in an explicit non-public partition. `must-revalidate` disables stale serving. `Set-Cookie`, `Set-Cookie2`, `Authentication-Info`, `Proxy-Authentication-Info`, and hop-by-hop headers are never persisted or replayed.

Native request cache modes are honored:

| Native mode | Persistent-cache behavior |
|---|---|
| `no-store` | Bypass read and write. |
| `reload` | Bypass read; a successful eligible response replaces the entry. |
| `no-cache` | A stored entry must be synchronously conditionally revalidated before use. |
| `force-cache` | Return a retained matching entry even when stale; never resurrect an evicted or invalidated entry. |
| `only-if-cached` | Return a retained matching entry or a synthetic 504 response; never use the network. |
| `default` or omitted | Return fresh; return stale within its SWR window and revalidate in the background; otherwise fetch. |

Request `Cache-Control: no-store` and `no-cache` directives impose the equivalent or stricter behavior. Response `Age` and `Date` are included in freshness calculation so persistence does not restart an already-aged response’s lifetime.

The stored object is the raw accepted transport response, captured before `afterResponse` transformations. It is committed only after the attempt survives the existing after-response/HTTP-error/forced-retry decision. A cache hit reconstructs that raw response and then runs the normal `afterResponse`, HTTP error, response decoration, progress, and body-shortcut pipeline. Hooks therefore run once per Ky call and request-specific hook transformations are never persisted for another caller.

Redirected responses are excluded because a portable reconstructed `Response` cannot preserve redirect-chain metadata without persisting potentially sensitive redirect URLs. The internal cached-response implementation reconstructs status, status text, safe headers, and body, reports the current finalized request URL, preserves the stored safe response type, reports `redirected: false`, and preserves those values across `clone()`.

Initial cache writes consume a bounded clone in the background so returning a streaming network response is not delayed. Storage failures are fail-open and cannot change the network response. `backgroundTask` receives the internally caught task so a service worker or server framework can attach it to its lifetime. Without that callback persistence remains best effort if the browser context terminates.

## Stale-while-revalidate — fixed

A fresh hit is returned directly. A stale hit within `staleUntil` is returned immediately and starts one best-effort background revalidation per variant per JavaScript process or browsing context. The revalidation clones the finalized request, removes the caller’s abort signal, adds `If-None-Match` or `If-Modified-Since` only when the caller did not supply a conditional header, uses the configured custom `fetch`, and applies `revalidateTimeout`.

Background revalidation does not rerun `beforeRequest`, `afterResponse`, retry, or error hooks. The finalized request already contains before-request authentication and routing changes; suppressing the remaining hooks avoids hidden user side effects after the original call has completed. It makes one transport attempt. A 304 merges permitted end-to-end metadata into the stored response and recomputes freshness. An eligible 2xx replaces the record. Any other status, timeout, network error, oversized body, or cache-policy rejection leaves the stale record unchanged until normal expiry. Errors are caught and reported through a sanitized `onCacheError` event.

Cross-tab and cross-process duplicate revalidations are allowed. Correctness does not depend on a distributed lock: every write is atomic, and the last successfully completed validation in the current generation wins. In-process/background coalescing is only a load optimization.

## Cache keys and privacy — fixed

No raw credential is ever placed in a cache key or persistent metadata. The resource digest is SHA-256 over a versioned canonical encoding of namespace, uppercase method, and the finalized URL including its query. The raw URL is not persisted. The variant digest is SHA-256 over the resource digest, an opaque partition digest, configured `varyHeaders`, the response’s normalized `Vary` names, and canonical values for non-sensitive varying request headers. Header names are lowercased, sorted, and encoded with lengths rather than delimiter concatenation.

The mandatory sensitive-header set is `authorization`, `proxy-authorization`, `cookie`, `cookie2`, `x-api-key`, and `x-auth-token`; applications may add names but may not remove the mandatory set. Sensitive header values are never fingerprinted. A response varying on a sensitive header is cacheable only when an explicit partition is present, and the partition digest stands in for that dimension.

Credential gating is fail-closed:

- If `Request.credentials` is not `omit`, or a mandatory/configured sensitive request header is present, a cache read and write require `partition` to resolve to a non-empty value.
- If the partition callback returns `undefined`, throws, or times out, the cache is bypassed.
- The returned partition value must be an application identity such as a tenant/session epoch, never a bearer token, cookie, password, or API key. Only its SHA-256 digest is persisted.
- When credentials are omitted and no sensitive header is present, the implicit partition is `public`.

This conservative rule intentionally means an ordinary browser request using the Fetch default `credentials: 'same-origin'` does not use persistent caching unless the caller supplies a partition or sets `credentials: 'omit'`. It prevents logged-in, logged-out, and account-switch traffic from sharing a response merely because a browser does not expose ambient cookie values to JavaScript.

Hashing keys is data minimization, not encryption. Query strings, low-entropy partition names, response bodies, and response headers may still be sensitive. The documentation must tell callers not to place secrets in URLs and to use a protected or encrypted store when the response itself is confidential.

## Invalidation and concurrency — fixed

Manual invalidation computes opaque selectors in memory and never persists the input URL. By default it invalidates all `GET`/`HEAD` variants and partitions for the exact finalized URL. Method and partition filters are optional. `clear()` changes the namespace epoch before deleting records.

After a successful network `POST`, `PUT`, `PATCH`, or `DELETE`, Ky synchronously invalidates cached `GET` and `HEAD` entries for the final request URL and same-origin `Location` and `Content-Location` targets. Automatic invalidation is limited to the current explicit partition, or the public partition for credential-free requests. A response supplied entirely by a hook does not trigger mutation invalidation.

Every fill captures the namespace, resource, and partition generation tokens read before its network operation. Invalidation first replaces the applicable token and only then removes matching records. A reader ignores any record whose captured tokens differ from current tokens. Consequently, a slow fill or revalidation that finishes after invalidate/clear may write bytes, but that record is unreachable and is later collected; it cannot resurrect invalidated data. This fencing rule applies identically in IndexedDB transactions and Node record/tombstone files.

Reads observe either the complete old record or the complete new record. Concurrent fills of the same live generation may both fetch and atomically commit; last completed valid commit wins. Concurrent eviction may remove a candidate but cannot produce a partial response. Cache errors default to bypassing the cache. A failed automatic invalidation disables cache reads for that store in the current Ky instance and reports `onCacheError`, but does not convert a successful mutation response into a request failure. Manual `invalidateResponseCache` and `clear()` reject on failure so callers can enforce their own recovery policy.

## Implementation boundaries for a future revision

Implementation should be split only after ownership is authorized:

1. Freeze and test the exported types, canonical key encoder, privacy eligibility, record schema, and generation contract.
2. Implement and independently test IndexedDB and Node filesystem adapters behind separate package subpaths.
3. Integrate lookup/fill/SWR/invalidation into the Ky lifecycle without altering native Fetch cache behavior, retry semantics, hook order, or streaming.
4. Add documentation, package exports, browser cross-tab tests, spawned Node cross-process tests, fake-clock freshness tests, credential redaction tests, mutation/invalidation race tests, crash/temporary-file tests, and full regression validation.

No future worker may choose a different public option name, persistence backend, key credential rule, hook ordering, stale behavior, invalidation fence, or cross-writer winner policy without returning to the architect and issuing a new plan revision.

## Risks and required proof

The implementation is high-risk and architectural. Required proof includes browser tests with two independent contexts, Node tests with independently spawned processes, absence of Node built-ins from the browser entry graph, byte-for-byte scans showing secrets and raw URLs absent from stored key metadata, atomic old-or-new reader tests, invalidation-versus-late-write fencing tests, exact native `RequestInit.cache` mode tests, hook-order tests on fresh/stale/miss paths, conditional 304 merge tests, bounded-body and eviction tests, and unchanged behavior when `responseCache` is omitted.

Inspected repository context:

- `source/core/Ky.ts` — `sha256:94a6e80411c77663c5fe272d9fccb942bab7290d7e10fdd9ef89f99d3c01ab25`
- `source/types/options.ts` — `sha256:53f67473dc01f1af07e6fddb6ba469d7205bf542b49c93ef22b82a75a0d6b32d`
- `source/utils/merge.ts` — `sha256:03b5b800027821ee2ec17eb95e01b6e86eb1a6b007ccf06b0b77e723abf1118b`
- `source/core/constants.ts` — `sha256:a5398477652b2a576bce02d4b2565952c41c00f9b3cdf27152b536124f671fb9`
- `source/index.ts` — `sha256:8c493886a2fd336792ffe3647c05f3ec7b7880dbe9c85f68b5242072c0d24208`
- `package.json` — `sha256:cc91aa643d4c22c6238af2e44202dd34e829d7a84531aacaa171d1dc1880206e`
- harness packet — `sha256:a1834e0ad2a933fa234e73b1e16c42668382dce8f64ad35bcfb9600d2f8f9b56`
