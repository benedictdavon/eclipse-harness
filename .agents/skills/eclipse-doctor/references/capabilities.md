# Capability interpretation

Use these route states:

- `verified` — trusted host metadata proves the requested effective route.
- `broken` — host metadata proves a different route.
- `unverified` — configuration exists but runtime identity is not observable.
- `unavailable` — the host or requested capability is absent.

Never turn `unverified` into pass. A standard/manual workflow can continue in policy-only or manual mode, but no native routing or cost guarantee exists. Strict mode must fail closed.

Represent permissions in three layers: desired policy, verified host capability, and effective runtime permission. Expose gaps.
