# Architect result — V02-REAL-001

Executable bounded implementation is approved as `V02-REAL-001-T1`; the complete wire contract is in `task.md`.

## Architecture decisions

- Reject negative input explicitly at the start of `int_to_bytes` with exactly `ValueError("num must be non-negative")`, before `_int_to_bytes` is invoked.
- Preserve the existing unsigned-64-bit packing and leading-zero stripping path for every non-negative input. Do not alter exports, dependencies, or unrelated encoding behavior.
- Add one focused negative-input assertion and retain coverage of zero and maximum `uint64` behavior in the existing encoding tests.

## Execution wave

Wave 1 contains only `V02-REAL-001-T1`. The host controls scheduling, must capture this task's patch and status before any later work, and must keep validation-generated cache/bytecode out of the product patch.

## Risk, routing, and human boundaries

Risk is low and the change is a normal bounded local implementation, so the policy route is Luna/high. Effective model and mechanical permissions remain unverified; the route is policy-only, not an identity or cost guarantee. Stop for any required public-export, dependency, or out-of-scope change. Network, installation, credentials, external effects, destructive actions, and writes outside the two authorized files require a new human/architect authorization.
