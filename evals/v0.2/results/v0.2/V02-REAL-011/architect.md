# Architect result — V02-REAL-011

No executable worker contract is approved. This cross-cutting request terminates in architecture planning under host plan revision 1 (`sha256:9b49ba48e1f779a27f4902d1af11e661c86423094270a00c29e3d3eacf3c9846`). A revised host-issued identity is required after decisions are approved.

## Discovery result

The application stores UTC-oriented `Post.timestamp`, `Message.timestamp`, `User.last_seen`, and `last_message_read_time`, renders posts and messages through `_post.html` using Flask-Moment, and sets locale separately through Flask-Babel. The edit-profile flow is the natural preference UI. `User.to_dict` exposes `last_seen`; there is no post/message API representation at present. Existing migrations use nullable user-profile additions.

The request remains architectural because the timezone identifier, default/backfill, invalid-zone policy, API exposure/writeability, form choices, browser-vs-server rendering source, DST behavior, and definition of “every timestamp” are not fixed. A worker must not improvise them.

## Required invariants

- Stored instants remain UTC; the preference changes presentation only.
- Use canonical IANA zone keys, not fixed offsets or translated display labels.
- Conversion must be DST-aware, and naive historical database values need an explicit UTC interpretation policy.
- Anonymous viewers and users without a saved preference have a deterministic fallback.
- Invalid persisted or submitted zones cannot crash templates or API serialization.
- Locale (language/format) and timezone (instant conversion) remain separate concerns.

## Routing and human boundary

Route to Sol architecture, then human/project-owner approval for public representation, migration/default, and rendering-source decisions. Do not dispatch implementation, create a migration, install timezone data, use network/credentials, or write product files. Effective model and permissions are unverified.
