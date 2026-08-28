# Architecture terminal plan — V02-REAL-005

No executable Task Contract is issued under plan revision 1. The host must not dispatch implementation from this file.

## Blocking decisions

1. Define what streams: serialized objects, already-serialized bytes, or both. Freeze source/sink protocols (`BinaryIO`, iterables, callbacks, sync/async), ownership and close behavior, seekability requirements, partial-write handling, cancellation, and return types.
2. Resolve the compatibility contradiction. Choose one explicitly:
   - streaming is guaranteed only for implementations that opt into a new capability protocol, while legacy subclasses fail clearly or use an explicitly documented buffering fallback; or
   - legacy subclasses are supported through bounded disk spooling, with no claim of zero-copy or disk-free operation; or
   - the project accepts a versioned breaking change to serializer, signer, and algorithm extension interfaces.
3. Freeze new public method names and type contracts across `Serializer`, `Signer`, `TimedSerializer`, `TimestampSigner`, `URLSafeSerializer`, and `URLSafeTimedSerializer`. Decide whether unsafe loading receives a streaming counterpart.
4. Freeze wire compatibility. Decide whether streamed output must be byte-for-byte accepted by existing non-streaming APIs and vice versa, including separator placement, timestamp encoding, fallback signers, key rotation, Base64 padding, and URL-safe compression markers.
5. Define algorithm capability negotiation. Existing `SigningAlgorithm.get_signature(key, value)` is whole-buffer. Specify an optional incremental MAC interface and exact legacy fallback; never infer capability from method names or catch broad runtime errors as negotiation.
6. Freeze authenticated-output semantics. Decide whether verified payload is withheld until final tag verification, written to a quarantined seekable sink with commit/abort, or exposed incrementally as explicitly untrusted. Specify cleanup and error behavior for bad signatures and expired timestamps.
7. Decide URL-safe compression policy. Its current choose-the-shorter behavior requires both sizes. Approve two-pass input, bounded disk spool, a changed deterministic compression rule with a new wire version, or exclusion from the bounded-memory guarantee.
8. Set resource and security limits: maximum buffered trailer, chunk-size semantics, maximum input/output expansion, decompression-bomb controls, temporary-file location/permissions, cleanup after error or cancellation, and behavior for malformed separators/signatures.
9. Build a compatibility matrix for base classes and representative custom subclasses overriding `dump_payload`, `load_payload`, `make_signer`, `iter_unsigners`, `sign`, `unsign`, `get_signature`, and `verify_signature`. Include timed and URL-safe combinations and custom text/bytes serializers.
10. Specify acceptance evidence before implementation: memory-bounded measurements, byte-for-byte wire vectors, old/new cross-read tests, subclass conformance tests, bad-signature no-release tests, expiration/key-rotation/fallback coverage, truncation and malformed-input tests, and spool cleanup tests.

## Required next state

Sol returns an architecture decision record covering all ten items and a decomposed ownership plan. The human/project owner approves the public API, compatibility tier, and any disk-spooling authority. The host then issues a new `plan_revision`, canonical `plan_digest`, and any new task identities; those values must be copied verbatim into future contracts.

Until that state exists, stop with no product or documentation writes and no validation commands. The packet contains no frozen acceptance-validation command.
