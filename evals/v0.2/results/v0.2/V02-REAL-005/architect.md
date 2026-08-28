# Architect result — V02-REAL-005

No executable worker contract is approved. This request terminates in architecture escalation under host plan revision 1 (`sha256:b4b433cab4da523c1144d998caec84f4956385cd7734c249da3b7640e00a039a`). `task.md` records the required decision plan; a revised host-issued plan identity is required before implementation can be delegated.

## Discovery result

The current extension points are whole-value APIs:

- `Serializer.dump_payload` calls arbitrary `serializer.dumps(obj)` and materializes bytes; `load_payload` calls arbitrary `loads` on a complete payload.
- `Serializer.dumps` materializes the payload and calls `Signer.sign`; `dump` merely writes that completed value. `load` similarly reads the whole source.
- `SigningAlgorithm.get_signature(key, value)` and `verify_signature(key, value, sig)` receive complete bytes. Existing custom algorithms and signer subclasses can rely on those signatures.
- `TimestampSigner` changes the signed envelope, and `TimedSerializer` changes unsigning semantics including expiration and timestamp return.
- `URLSafeSerializerMixin` decides whether to compress only after comparing complete compressed and uncompressed representations, then Base64-encodes the selected value.

Therefore a hard constant-memory guarantee cannot transparently cover every existing serializer, signer, signing-algorithm, timed, and URL-safe subclass. Buffering preserves compatibility but violates the memory requirement; changing existing extension methods breaks subclass compatibility. This is a public API and security design conflict, not bounded implementation work.

## Invariants that the revised architecture must preserve

- Existing `dumps`/`loads`, `dump`/`load`, `sign`/`unsign`, validation, fallback signer, key rotation, timed expiration, exception, and return-type behavior remain source- and wire-compatible unless an explicitly versioned incompatibility is approved.
- Streaming verification must not expose unauthenticated deserialized output as trusted. Any early-output design needs an explicit quarantined/staged sink and commit/abort contract.
- Key derivation, algorithm selection, constant-time signature comparison, signature-envelope parsing, timestamp coverage, and fallback signer order cannot weaken.
- Legacy subclasses must never be falsely advertised as bounded-memory capable. Capability negotiation and fallback behavior must be explicit and observable.
- Resource ownership, maximum trailer buffering, spooling, cleanup on error/cancellation, and input/output limits must be deterministic.

## Routing and human boundary

Route the next phase to Sol architecture for public API, compatibility, and security design. Human/project-owner decisions are required for compatibility level, local disk spooling authority, and whether legacy subclasses may use an explicitly non-streaming fallback. Do not route to a Luna worker, install dependencies, use network or credentials, write product files, or create a plausible revised digest. Effective model and permissions remain unverified.
