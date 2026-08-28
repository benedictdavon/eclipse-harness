# Architect result — V02-REAL-007

Executable bounded implementation is approved as `V02-REAL-007-T1`; the complete wire contract is in `task.md`.

## Architecture decisions

- Guard `User.avatar` before hashing or URL construction: `size <= 0` raises exactly `ValueError("size must be positive")`.
- Leave the existing email digest and Gravatar URL expression untouched for positive sizes.
- Extend the existing `test_avatar` coverage with both zero and negative-one error cases; do not touch templates, mapped fields, relationships, migrations, or other model behavior.

## Execution wave

Wave 1 contains only `V02-REAL-007-T1`. The host controls execution and captures its patch/status. The frozen compile command may create `__pycache__`/bytecode; those are validation artifacts and must not enter the product patch.

## Risk, routing, and human boundaries

This is a low-risk normal bounded edit routed by policy to Luna/high. Effective model and permissions are unverified. Stop for changes to database schema, templates, dependencies, or behavior for positive sizes. Network, installation, credentials, external effects, destructive actions, and writes beyond `app/models.py` and `tests.py` are not authorized.
