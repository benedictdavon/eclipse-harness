# Architect result — V02-REAL-003

Executable bounded bug fix is approved as `V02-REAL-003-T1`; the complete wire contract is in `task.md`.

## Diagnosis and fixed design

`base64_decode` calls `want_bytes(..., encoding="ascii", errors="ignore")` before decoding. For `str`, that silently drops non-ASCII code points and may decode altered data. The fix is to use strict ASCII conversion inside the existing bad-data translation boundary so an encoding failure becomes `BadData("Invalid base64-encoded data")`. Bytes input must bypass text encoding as it does now, and valid URL-safe padding/decoding stays unchanged.

## Execution wave

Wave 1 contains only `V02-REAL-003-T1`. The host controls execution and must capture its task-local patch/status; pytest-created cache or bytecode is validation output, not product scope.

## Risk, routing, and human boundaries

This is a low-risk bounded Python bug fix routed by policy to Luna/high. Effective model and permissions are unverified. Stop if satisfying the request would require redefining byte-input validation, changing `BadData`, altering dependencies, or broadening the public API. Network, installation, credentials, external effects, destructive actions, and other writes are unauthorized.
