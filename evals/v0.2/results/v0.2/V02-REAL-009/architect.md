# Architect result — V02-REAL-009

Executable bounded bug fix is approved as `V02-REAL-009-T1`; the complete wire contract is in `task.md`.

## Diagnosis and fixed design

`User.to_dict` unconditionally calls `.replace(...).isoformat()` on the nullable `last_seen` mapped attribute. Guard only that expression: serialize `None` as Python `None` (JSON `null`), otherwise retain the exact existing `last_seen.replace(tzinfo=timezone.utc).isoformat()` path. Add focused coverage for both branches without changing the column, default, or schema.

## Execution wave

Wave 1 contains only `V02-REAL-009-T1`. The host captures its task-local patch/status. The frozen compile command may create bytecode, which must remain outside the product patch.

## Risk, routing, and human boundaries

This low-risk bounded fix routes by policy to Luna/high. Effective model and permissions are unverified. Stop for schema/migration, timestamp normalization, endpoint, dependency, or template changes. No network, installation, credentials, external effects, destructive actions, or other writes are authorized.
