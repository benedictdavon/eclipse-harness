# Architect result — V02-REAL-004

Executable behavior-preserving refactor is approved as `V02-REAL-004-T1`; the complete wire contract is in `task.md`.

## Architecture decisions

- Extract only the expression that appends `=` bytes to reach a length divisible by four into a module-private bytes-to-bytes helper.
- Keep `base64_decode`'s signature, ASCII conversion mode, error boundary, `BadData` behavior, and decoder call unchanged. The helper must not be exported or treated as a new public test surface.
- Existing focused tests are sufficient acceptance coverage and remain unchanged unless a strictly necessary in-scope adjustment is identified; the product write is limited to `encoding.py`.

## Execution wave

Wave 1 contains only `V02-REAL-004-T1`. Execution is host-controlled, and the host must capture its patch/status while excluding validation-generated caches and bytecode.

## Risk, routing, and human boundaries

This is a low-risk deterministic refactor routed by policy to Luna/medium. Effective model and permissions are unverified. Stop rather than change any public behavior, expose the helper, edit tests or another module, or require additional authority. Network, installation, credentials, external effects, and destructive actions are prohibited.
