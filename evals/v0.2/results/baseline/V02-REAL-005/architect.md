# V02-REAL-005 architecture discovery

## Terminal outcome

**Architecture escalation; no Task Contract and no execution wave are authorized.**

The requirement cannot yet be converted into bounded implementation work. The
current extension contracts are deliberately one-shot, while the requested
property is bounded-memory processing. Supporting arbitrary existing
`Serializer`, `Signer`, and `SigningAlgorithm` subclasses during a streaming
call is incompatible with a strict larger-than-memory guarantee unless
"compatible" is defined to allow a clear, capability-based refusal.

The pinned checkout was verified at
`672971d66a2ef9f85151e53283113f33d642dabd`. No production change is proposed
or authorized by this document.

## Repository facts that constrain the design

| Surface | Current invariant | Streaming consequence |
| --- | --- | --- |
| `Signer.sign(value)` / `Signer.unsign(signed_value)` | The complete value is a `str | bytes`; the wire form is `value + sep + base64(signature)`, parsed from the right. | The existing methods necessarily materialize the value. A new method may preserve this wire form for stream-capable implementations, but cannot make arbitrary overrides incremental. |
| `Signer.get_signature` / `verify_signature` | Each receives the complete value. Key rotation retries verification with multiple keys. | A streaming implementation that directly constructs an HMAC bypasses overrides of these public methods and may change subclass behavior. The input must also be replayable across key attempts. |
| `SigningAlgorithm` | The public customization points `get_signature(key, value)` and `verify_signature(key, value, sig)` are one-shot. The default verifier uses `hmac.compare_digest`. | `HMACAlgorithm` can be implemented incrementally, but an arbitrary existing algorithm cannot. Joining chunks as a fallback violates the memory requirement. |
| `TimestampSigner` | Overrides the signed envelope by inserting a timestamp before the signature and extends `unsign` with `max_age` and `return_timestamp`. | A base implementation that ignores the override would emit or parse the wrong format. Timestamp capture time and expiry/error semantics must be fixed for the streaming API. |
| `Serializer` | `dump_payload` and `load_payload` take and return complete `bytes`; `dumps`/`loads` call those hooks. `dump`/`load` are file-shaped convenience methods but call `dumps` or `f.read()`, so they are not streaming. | Bypassing payload hooks breaks subclasses. Delegating to them buffers. A deserializer that returns one Python object cannot represent a result larger than memory without a new producer/consumer codec abstraction. |
| Serializer backend | The accepted structural interface only promises `dumps(obj)` and `loads(payload)`. It may produce text or bytes. `serializer_kwargs` are passed to `dumps`. | Existing backends, including arbitrary user objects, need not expose incremental encode/decode operations. Runtime probing for unrelated `dump`/`load` names would be ambiguous and could change behavior. |
| `URLSafeSerializerMixin` | Overrides both payload hooks. It optionally compresses the whole serialized value only when compression saves at least two bytes, then base64 encodes it; a leading dot marks compression. | Preserving its exact tokens requires explicit streaming support, including a complete compressed-vs-uncompressed size decision. That can be bounded-memory only with disk-backed staging or multiple passes. Decompression also creates an amplification risk. |
| `TimedSerializer` and fallback signers | `loads` calls the specialized `TimestampSigner.unsign`; serializer fallback signers may be arbitrary classes and the input is retried. | Streaming verification must preserve specialized keyword and exception behavior, and must rewind staged input for every fallback. A one-shot fallback cannot safely be invoked for an unbounded value. |
| Failure API | `BadSignature.payload` commonly contains the entire unsigned payload, and `loads_unsafe` may deserialize it. Tests and documentation expose this behavior. | Attaching an unbounded payload as `bytes` defeats bounded memory. Releasing or deserializing data before authentication is unsafe. A streaming-specific failure contract is required. |

## Public API decision that must be fixed

The following is the recommended compatibility-first API direction, but it is
**not frozen** until the human owner resolves the semantic questions below.

1. Keep every existing constructor and method (`sign`, `unsign`, `dumps`,
   `loads`, `dump`, `load`, and unsafe variants) behaviorally unchanged.
2. Add new binary-stream entry points rather than silently changing `dump` and
   `load`:

   ```python
   Signer.sign_stream(source: BinaryIO, destination: BinaryIO, /, *, chunk_size: int = ...) -> None
   Signer.unsign_stream(source: BinaryIO, destination: BinaryIO, /, *, chunk_size: int = ..., max_value_size: int | None = ...) -> None

   Serializer.dump_stream(obj: Any, destination: BinaryIO, /, *, salt: str | bytes | None = None, chunk_size: int = ...) -> None
   Serializer.load_stream(source: BinaryIO, /, *, salt: str | bytes | None = None, max_signed_size: int | None = ..., max_payload_size: int | None = ...) -> Any
   ```

   `TimestampSigner.unsign_stream` and `TimedSerializer.load_stream` would need
   their existing `max_age` and `return_timestamp` options. Exact names,
   positional-only policy, return values, and whether text streams are accepted
   remain public-API decisions.
3. Define an explicit opt-in streaming codec protocol for serializer backends;
   do not infer capability merely because an object happens to have `dump` and
   `load` attributes. The protocol must specify text versus bytes, encode and
   decode operations, kwargs, finalization, error mapping to `BadPayload`, and
   whether decoding returns a materialized object or emits values/events to a
   consumer.
4. Define an explicit opt-in incremental signing algorithm protocol. It must
   preserve derived-key use, key rotation, final signature bytes, and
   constant-time verification. It cannot default to `b"".join(chunks)`.
5. A subclass that changes an envelope or payload hook must explicitly provide
   corresponding streaming hooks. Base code must never bypass an override and
   claim compatibility. Unsupported combinations must fail before consuming
   input or modifying the destination with a dedicated, documented exception.

Adding inherited methods that merely raise for legacy subclasses is source and
binary compatible, but it does **not** mean streaming works with every existing
subclass. If the requirement instead means that every existing subclass must be
able to use the streaming calls successfully, no architecture can guarantee
both that and bounded memory: arbitrary subclass code can require complete
`bytes` and can define a non-incremental signature function.

## Subclass invariants to freeze before implementation

- Existing one-shot dispatch and override order must not change.
- New streaming code may use an existing override only when that override
  explicitly advertises the new streaming contract; it must not inspect method
  bodies, guess from signatures, or bypass the override.
- Changing only existing configuration (`salt`, `sep`, key derivation, digest
  method, key rotation) must retain its current meaning. Stream support still
  depends on the selected algorithm being incrementally capable.
- `TimestampSigner` owns its timestamp envelope and expiry semantics;
  `URLSafeSerializerMixin` owns compression/base64 framing; `TimedSerializer`
  owns the additional load parameters. Each requires an explicit streaming
  implementation rather than generic base-class dispatch.
- Custom `SigningAlgorithm` instances and custom serializer backends that only
  implement today's protocol remain fully usable through today's APIs. New
  streaming calls either require explicit capability or must be documented as
  unsupported; they must never secretly buffer without a caller-selected bound.
- Fallback signer order and newest-to-oldest secret-key order must remain
  unchanged. Every candidate used by a streaming verification must support the
  new capability, or the call must fail deterministically before untrusted
  payload is released.
- For inputs small enough to compare, a stream-capable built-in must produce a
  token accepted by the corresponding legacy method. Whether it must be
  byte-for-byte identical (including JSON, zlib, and timestamp details) is still
  an explicit compatibility decision.

## Security decisions to freeze before implementation

1. **Authenticate before release.** `unsign_stream` and `load_stream` must not
   expose payload bytes, decompress data, or invoke a potentially unsafe
   deserializer until the signature is valid. Because the current signature is
   a suffix, verification needs a private, rewindable staging area. For a
   non-seekable destination, copying authenticated data is a second phase.
2. **Failure atomicity.** Decide whether the library guarantees that the
   destination is unchanged on authentication, expiry, size-limit, decode, or
   I/O failure. A reliable guarantee requires a library-owned temporary file or
   a documented transactional destination protocol.
3. **Disk use and confidentiality.** Approve whether temporary disk storage is
   allowed, who selects its directory, file permissions, in-memory spool
   threshold, cleanup behavior, and what is promised after abnormal process
   termination. Temporary files may contain plaintext or attacker-controlled
   bytes.
4. **Resource limits.** Fix limits and defaults for signed bytes, authenticated
   payload bytes, decoded bytes/events, compression ratio or output, chunk size,
   and temporary disk consumption. `URLSafeSerializerMixin` must enforce the
   decoded bound during decompression, not after it.
5. **Verification behavior.** Preserve constant-time tag comparison. Truncated,
   malformed, over-limit, and I/O-error cases need stable exception types.
   Parsing must continue to honor the rightmost separator and arbitrary legal
   separator values.
6. **Failure payloads.** A streaming failure cannot populate
   `BadSignature.payload` with unbounded `bytes`. Choose between `None`, a
   bounded diagnostic prefix, or a new explicitly owned temporary-payload
   object. The latter introduces lifetime and cleanup obligations. Existing
   one-shot exceptions must remain unchanged.
7. **Unsafe APIs.** Do not add a streaming counterpart to `loads_unsafe` in the
   first implementation wave. If it is required, its untrusted-data release,
   deserialization, size limits, and storage ownership need a separate threat
   decision.
8. **Timed data.** Decide whether an invalid token may still expose its parsed
   timestamp as current `BadTimeSignature` can. Parsed fields from an invalid
   signature remain untrusted regardless of compatibility labeling.

## Compatibility choices requiring owner approval

The owner must choose one option in each row before a worker can receive a
bounded contract.

| Decision | Recommended choice | Alternatives / consequence |
| --- | --- | --- |
| Meaning of "values larger than memory" | Bound all intermediate buffers and support producer/consumer streaming codecs; materialized input/output objects are outside that guarantee. | If `load_stream` must return an object larger than memory, the `Any -> Any` serializer model must be replaced with an event/record consumer API. |
| Meaning of "every existing subclass" | Preserve all existing APIs for all subclasses; new streaming calls are capability-gated and refuse unsupported subclasses before I/O. | Requiring successful streaming for arbitrary existing subclasses is infeasible. Allowing hidden one-shot fallback removes the memory guarantee. |
| Wire compatibility | Built-in streaming output uses the existing suffix formats and is accepted by legacy readers; require byte identity for deterministic, untimed built-ins on small fixtures. | A new framed format simplifies parsing but requires version negotiation and is not legacy-readable. |
| Destination safety | Stage privately and copy only after full verification/decode succeeds; destination remains unchanged on content/authentication failure. | Direct output is cheaper but releases unauthenticated data and is rejected. Seek/truncate rollback excludes pipes and is not reliably atomic. |
| Temporary storage | Permit secure library-owned disk staging with documented permissions, limits, cleanup, and caller override. | Forbid disk staging, in which case suffix-format verification of non-seekable oversized streams is not generally possible. |
| Limits | Require explicit finite limits for decode/decompression and staging, with secure documented defaults. | Unlimited defaults preserve historical behavior but expose disk exhaustion and decompression-amplification denial of service. |
| Text streams | Make new streaming surfaces binary-only; codecs own UTF-8 adaptation. | Supporting `TextIO` doubles atomicity, byte-counting, and encoding semantics and needs a separate typed contract. |
| Failure payload | Streaming exceptions do not materialize the payload; use `payload=None` plus bounded metadata. | A temporary-payload handle needs a new public ownership/lifetime API. |

## Revised architecture plan after approval

Once the choices above are frozen, issue separate, dependency-ordered contracts
rather than one cross-cutting worker task:

1. **Wave 1: protocol and threat contract** — public types, capability rules,
   error taxonomy, staging/limits, and compatibility fixtures. No production
   behavior until this contract is independently reviewed.
2. **Wave 2: signer core** — built-in `Signer`/`HMACAlgorithm` incremental
   support and secure verify-before-copy staging. `TimestampSigner` follows as a
   dependent contract because it owns a different envelope.
3. **Wave 3: serializer core** — explicit streaming codec integration after
   signer semantics are stable. Built-in JSON behavior and object-materializing
   limits must be stated in acceptance evidence.
4. **Wave 4: URL-safe and timed composition** — bounded base64/zlib processing,
   compression-choice compatibility, decompression limits, timestamp behavior,
   and fallback replay.
5. **Wave 5: compatibility/security review** — one-shot regression suite,
   subclass matrix, exact legacy-token fixtures, malformed/truncated inputs,
   key rotation/fallbacks, non-seekable streams, destination atomicity, resource
   limits, and memory/disk-bound evidence.

These waves are descriptive only. There are no authorized task IDs, write
globs, or parallel ownership assignments until the owner resolves the public
contract and security choices.

## Human boundary / required response

Human approval is required for the eight choices in the compatibility table,
especially whether capability-based refusal satisfies "compatible with every
existing subclass" and whether secure disk staging is permitted. If successful
streaming through arbitrary legacy subclasses is mandatory, the requirement
must be revised because it is inconsistent with the existing one-shot subclass
contracts. Until that response, creating `task.json` or delegating production
work would give a worker unresolved architecture and security decisions and is
therefore prohibited.
