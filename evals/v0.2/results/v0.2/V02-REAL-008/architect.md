# Architect result — V02-REAL-008

Executable multi-file implementation is approved as `V02-REAL-008-T1`; the complete wire contract is in `task.md`.

## Architecture decisions

- Use explicit viewer injection, not an import of API authentication state into `app.models`: add an optional `viewer` argument to user serialization and paginated collection serialization.
- Include top-level `is_following` only when `viewer` is not `None`; compute it as `viewer.is_following(serialized_user)`. With no viewer, omit the field and preserve safe context-independent serialization.
- Every token-authenticated user API response passes `token_auth.current_user()` through the relevant direct or collection serialization call. The unauthenticated create-user response supplies no viewer and therefore omits the field.
- This is computed response data, never a mapped attribute or database column.

## Execution wave

Wave 1 contains only `V02-REAL-008-T1`, because the model serialization signature, API call sites, and tests form one shared interface change. The host controls execution and captures its complete patch/status. Compile-created bytecode is validation output, not product scope.

## Risk, routing, and human boundaries

Risk is medium due to an API representation and serializer call-signature change; policy routing is Luna/high for the now-bounded implementation. Effective model and permissions are unverified. Stop for database/migration work, implicit auth lookup in models, query optimization that changes schema, or other endpoint changes. Network, installation, credentials, external effects, destructive actions, and other writes are unauthorized.
