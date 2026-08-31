# Architect result — V02-REAL-002

Executable bounded implementation is approved as `V02-REAL-002-T1`; the complete wire contract is in `task.md`.

## Architecture decisions

- Enforce the eight-byte limit with an explicit length check at the start of `bytes_to_int`, raising exactly `ValueError("bytestr must contain at most 8 bytes")` before padding or unpacking.
- Preserve the existing right-padding-to-eight and unsigned unpack result for inputs of zero through eight bytes; retain the public function name.
- Add a focused nine-byte regression test and one concise sentence documenting the maximum in `docs/encoding.rst`.

## Execution wave

Wave 1 contains only `V02-REAL-002-T1`. Although its three writes are logically one bounded change, actual scheduling is host-controlled; the host must capture the complete task patch/status and keep validation caches or bytecode out of the product patch.

## Risk, routing, and human boundaries

Risk is low and the policy route is Luna/high for normal bounded implementation. Effective model and permissions are unverified, so this is policy-only. Stop for any need to rename the public function, change dependencies, expand documentation scope, or alter behavior for valid inputs. No network, installation, credentials, external effects, destructive actions, or other writes are authorized.
