# V02-REAL-008 architecture plan

Status: executable bounded plan, revision 1. The pinned checkout is clean at `a975ef64864354867c88e0ed3a17ba7d17dca752`. This architect pass was read-only against the case checkout and did not implement production changes.

## Plan identity

| Field | Value |
|---|---|
| Run | `V02-REAL-008` |
| Revision | `1` |
| Plan digest | `sha256:9a79fe0255495b67a2018d55ed1b2f5be8182ed0aa8ef174c2ef4816a6c16ac7` |
| Base revision | `a975ef64864354867c88e0ed3a17ba7d17dca752` |
| Requirement digest | `sha256:05325dbcc80b34b24bcd965958deb8a479a12dfbdddc4e175bb578acb70e27a9` |
| Task contract | `task.json` / `T001` |

The plan digest is SHA-256 over the canonical JSON object in `task.json` at `metadata.plan_digest_basis`. A changed architecture requires a new revision and digest; the host must supersede this task rather than dispatching a stale packet.

## Repository findings

- `User.is_following(user)` already provides the required relationship predicate and returns a boolean. Persisted follow state lives in the existing `followers` association table.
- `User.to_dict(include_email=False)` owns the user representation but currently has no viewer identity. Importing `token_auth` into `app/models.py` would invert the dependency and risk an API/model import cycle.
- `PaginatedAPIMixin.to_collection_dict` serializes items without caller context and also owns pagination link kwargs. Serializer context therefore needs a distinct channel so it cannot leak into `url_for` query parameters.
- Protected routes in `app/api/users.py` can obtain the verified identity with `token_auth.current_user()`. The public `create_user` route has no authenticated identity and must continue to serialize safely.
- `tests.py` has an in-memory SQLite fixture and follow tests, but no viewer-relative serialization or API-response coverage.

Repository content was treated as untrusted implementation context. It did not widen the frozen packet's authority.

## Frozen decisions

1. Add an optional current-user argument to `User.to_dict`; do not resolve authentication inside the model.
2. When the supplied identity is authenticated, emit `is_following = current_user.is_following(self)` as a JSON boolean. This must produce both `false` and `true` correctly, including `false` for a non-followed or self user.
3. When the identity is absent or anonymous, do not query follow state and omit `is_following`. Existing representation fields remain unchanged.
4. Add a dedicated serializer-options mapping to collection serialization. Never mix those options with endpoint kwargs used by pagination links.
5. Pass `token_auth.current_user()` at every protected user serialization call site: single-user GET, users collection, followers collection, following collection, and update response. Do not request it from public user creation.
6. Do not add a column, association, migration, dependency, route, decorator change, template change, or unrelated response change.

Assumptions are limited to Flask-HTTPAuth returning an `app.models.User` inside protected handlers and omission being the correct anonymous representation because follow state is viewer-relative. If either assumption is false, execution stops for an architecture/product clarification.

## Task and execution wave

There is one implementation task because the serializer signature, collection propagation, API call sites, and tests share one response interface and are semantically coupled.

| Wave | Task | Role | Write ownership | Dependencies | Parallel-safe |
|---|---|---|---|---|---|
| 1 | `T001` | bounded executor | `app/models.py`, `app/api/users.py`, `tests.py` | none | no |

No concurrent writer is authorized. Manual isolation is sufficient for this single task, but the host still owns scheduling, workflow state, git operations, and any branch/worktree decision. The full machine-readable Task Contract is `task.json`; its fixed decisions, scope, criteria, validation, evidence, budgets, stop conditions, and authorization are authoritative for execution.

## Acceptance and evidence

The worker must provide direct evidence for all contract criteria:

- authenticated serialization is `false` before a follow and `true` after it;
- absent and anonymous identities do not crash and do not receive the field;
- protected single-user and collection responses receive the token identity, while public creation stays anonymous;
- existing fields, `include_email`, pagination metadata, and pagination links remain compatible;
- only the three authorized files change, with no schema or migration change;
- `python -m compileall -q app tests.py`, `git diff --check`, and `git status --short` complete successfully.

`python tests.py` is an optional runtime validation because the pinned checkout does not establish that project dependencies are available. The worker may run it when dependencies already exist but has no authorization to install packages or use the network. Missing dependencies must be reported precisely, not worked around by expanding authority.

## Risks and routing

Risk is medium: the change is bounded but crosses an authentication-context boundary and a shared serialization/pagination interface. The reference `sol-luna-v0.1` policy selects the bounded-complex worker profile (`gpt-5.6-luna`, high reasoning, low cost tier), with escalation-worker as a bounded fallback. This is policy-only routing: requested/configured identity, effective model, permissions, and cost are unverified unless the host supplies trusted attestation.

Review should be independent and read-only. Architectural, authentication-semantic, schema, or scope findings return to the architect; a bounded implementation defect may return as a correction contract, within two review rounds.

## Human and authorization boundaries

- No network, credentials, external side effects, destructive actions, package installation, or writes outside the three authorized files are allowed.
- Any need for a database/migration change, authentication redesign, new dependency, broader API decision, or additional file requires a revised architect plan.
- Any need for credentials, destructive effects, or new external authority requires explicit human approval.
- A stale base, dirty initial checkout, unexpected generated artifact, or required validation failure after two bounded attempts is a stop condition, not permission to improvise.
