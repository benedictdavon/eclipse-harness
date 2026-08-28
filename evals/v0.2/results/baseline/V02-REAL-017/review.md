# Architecture terminal review — V02-REAL-017

Outcome: **architecture revision required**  
Review round: 1  
Implementation disposition: **not authorized; no worker task may be emitted**

## Review binding

- Packet: `sha256:a1834e0ad2a933fa234e73b1e16c42668382dce8f64ad35bcfb9600d2f8f9b56`
- Architect result: `sha256:b81b50c13334123dd3d0d85914c8458be44f44dc40741708c2bb5b28527823c8`
- Architect plan revision/digest: `1` / `sha256:3d21e0f8dd7b1f310eb61a3857a726431e216894ac9a0fb42ac0d0f3f33ac3f2`
- Pinned repository revision: `3419113b48e034fdcf8fa6bd3be3da7b3d0d758f`
- Checkout state: clean; no staged or unstaged implementation change

Reviewer permission posture:

- Desired: read-only inspection of the packet, architect result, and pinned checkout, with writes limited to this review and its terminal summary.
- Effective: inspection remained read-only and the pinned checkout remained clean.
- Enforcement: unverified; the host did not provide mechanical read-only attestation.

## Acceptance criteria

1. **Architect owns public API, storage, credential, and concurrency decisions — not satisfied.** The architect fixed the main facility name, runtime adapter split, persistence backends, credential partition rule, and generation fencing, but left material public/privacy/invalidation decisions unresolved in findings `ARCH-001` through `ARCH-004`.
2. **No worker receives unresolved cache authority — satisfied for this revision.** The architect emitted no worker task, the packet has an empty write scope, and the pinned checkout is clean. That must remain true until the architecture findings are resolved.
3. **Terminal result is an architecture plan or escalation — satisfied.** The submitted artifact is explicitly a terminal architecture plan and does not claim implementation.

## Validation summary

- The checkout HEAD exactly matches the packet revision.
- Every source/package digest listed by the architect matches the pinned checkout.
- The inspected Ky lifecycle confirms that cache integration would cross request finalization, hooks, retries, response processing, option merging, root exports, and package exports; those are correctly treated as architecture-sensitive future work.
- No runtime validation was required or appropriate because the packet authorizes no implementation.

## Findings

### ARCH-001 — High — security-concern — architect

- Path/symbol: proposed `ResponseCacheOptions` and sensitive-header eligibility
- Criterion: architect owns public API and credential decisions
- Evidence: the design says applications may add sensitive header names but may not remove the mandatory set. The fixed `ResponseCacheOptions` type has no `sensitiveHeaders` field or other extension mechanism. `varyHeaders` is separately defined as a variant-key input and cannot safely stand in for a sensitive-header registry.
- Impact: a future worker must invent the public configuration and merge semantics. Until then, an application-specific authentication header can avoid partition gating and may either alias responses across identities or have a low-entropy value represented by a persistent fingerprint.
- Exact correction: the architect must add a concrete public mechanism for extra sensitive header names, define normalization and validation, union it with the non-removable mandatory set, specify `create`/`extend`/init-hook cloning semantics, and require the resulting set to drive both partition gating and sensitive `Vary` handling.
- Disposition: architect

### ARCH-002 — High — security-concern — architect

- Path/symbol: implicit public partition and explicit partition digest
- Criterion: architect owns credential/privacy decisions
- Evidence: the plan names the credential-free implicit partition `public` and says explicit partition strings are SHA-256 digested, but does not require a reserved value or domain-separated canonical encodings for implicit and explicit partitions.
- Impact: an implementation can make explicit partition value `"public"` collide with the implicit public partition. That permits credentialed and credential-free variants to share a partition despite otherwise fail-closed gating.
- Exact correction: fix one canonical rule before delegation: either reject a reserved explicit value or, preferably, domain-separate implicit-public and explicit-identity encodings before hashing. Add a required collision/non-aliasing test.
- Disposition: architect

### ARCH-003 — High — architecture-escalation — architect

- Path/symbol: automatic mutation invalidation when `partition` cannot resolve
- Criterion: architect owns invalidation, credential, and concurrency decisions
- Evidence: partition callback `undefined`, error, or timeout bypasses cache reads and writes. Automatic mutation invalidation is limited to the current explicit partition (or the public partition for credential-free requests), but the plan does not define what happens after a successful credentialed mutation when no explicit partition can be resolved. The later failure rule addresses a store invalidation failure, not partition-resolution failure.
- Impact: a worker must choose whether to skip invalidation, invalidate every partition, or poison reads. Skipping can leave stale credentialed entries readable by other Ky instances, tabs, or processes after the mutation.
- Exact correction: define a cross-instance fail-closed rule for this case. The architecture must require either resource-wide invalidation across partitions or a persistent generation/read-disable action that prevents all sharers from serving the affected resource; callback failure must not silently become no invalidation.
- Disposition: architect

### ARCH-004 — Medium — invalid-contract — architect

- Path/symbol: `ResponseCacheStore`, `ResponseCacheRecord`, selector, event, and `invalidateResponseCache` public exports
- Criterion: architect owns public API and storage decisions
- Evidence: these types are declared public, asynchronous, and versioned only in prose. Concrete method signatures, selector/options shapes, version negotiation, record mutability/ownership, and error contract are absent. The future sequence tells implementation to “freeze and test” them.
- Impact: a worker would necessarily choose externally observable API and custom-adapter compatibility behavior. Those choices are not implementation detail once the types are root exports.
- Exact correction: publish concrete TypeScript contracts for every exported store/record/selector/event/invalidation surface, including atomic replace preconditions, generation operands/results, clear/invalidate failure behavior, and body ownership/copy rules, before any worker task is authorized.
- Disposition: architect

## Preserved decisions

The following architect-owned decisions are sufficiently fixed and should not be reopened by a worker: `responseCache` does not overload native `RequestInit.cache`; browser and Node use separate IndexedDB and local-filesystem adapters; storage is explicit and disabled by default; raw credentials and URLs are excluded from persistence metadata; credentialed requests require an explicit partition; stale serving and background revalidation behavior are separated from hook side effects; and namespace/resource/partition generation fencing prevents late writes from resurrecting invalidated data when invalidation succeeds.

## Residual risk and terminal disposition

No implementation exists to accept or reject. The architecture is close to bounded, but its remaining gaps sit directly on credential isolation, invalidation safety, and public custom-store compatibility. Return the packet to the architect for one plan revision. Keep the expected implementation write scope empty and do not delegate to a worker until all four findings are resolved and the revised architect artifact receives a new digest.
