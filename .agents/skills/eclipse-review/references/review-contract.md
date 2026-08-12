# Review contract

Bind the review to the task contract digest and exact result digest. Reject stale or mismatched packets.

An `accepted` outcome requires:

- no material findings;
- a satisfied verdict for every acceptance criterion;
- authorization-compliant changed files;
- adequate direct validation evidence;
- preserved architecture and invariants.

Record desired, effective, and enforcement status for reviewer permissions. If the host cannot prove read-only enforcement, state `effective: unverified`; do not silently claim mechanical isolation.

Never convert review into implementation. Return precise correction requirements so a bounded worker can act.
