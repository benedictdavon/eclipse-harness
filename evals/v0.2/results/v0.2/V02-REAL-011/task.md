# Architecture terminal plan — V02-REAL-011

Trusted identity: run `V02-REAL-011`, plan revision `1`, plan digest `sha256:9b49ba48e1f779a27f4902d1af11e661c86423094270a00c29e3d3eacf3c9846`, base revision `a975ef64864354867c88e0ed3a17ba7d17dca752`.

No executable Task Contract is issued under this identity. The packet has no frozen acceptance-validation command.

## Decisions required before delegation

1. **Storage and migration:** approve `User.timezone` as a bounded string containing an IANA key; choose nullable-with-fallback versus non-null default, maximum length, index policy, migration upgrade/backfill and downgrade. Preserve all timestamp columns as UTC instants.
2. **Timezone source:** freeze viewer preference precedence. Recommended: authenticated viewer's saved zone; application-configured default for anonymous/no preference. Decide whether browser autodetection may preselect a form value but never silently overrides stored preference.
3. **Invalid zones:** validate submitted values with `zoneinfo.ZoneInfo`; reject with a localized form/API validation error. For legacy/corrupt persisted values, log and fall back to the configured default rather than crashing. Decide behavior if system tzdata lacks a key; dependency installation is not currently authorized.
4. **Public representation:** decide whether `timezone` appears in `User.to_dict`, whether it is visible for every user or only self, and whether create/update API clients may write it. Freeze error schema and backward compatibility for omitted fields.
5. **Forms:** add an edit-profile choice or validated string field, freeze choice source/order/display labels, prepopulation, translation strategy, and CSRF/error behavior. Do not hard-code translated labels as stored values.
6. **Rendering:** decide whether Flask-Moment receives a page-level timezone and performs client rendering, or the server converts datetimes before templates. Freeze one approach for `_post.html`, `messages.html` reuse, `user.html`, and `user_popup.html`; avoid double conversion.
7. **Coverage boundary:** enumerate “every post/message timestamp”: relative post/message time in `_post.html`, profile last-seen displays, notification epoch timestamps, and export task timestamps. Explicitly include or exclude last-seen, notifications, emails, API values, and exported JSON.
8. **Compatibility:** old rows, anonymous pages, API clients omitting timezone, DST gaps/folds, and naive timestamps already loaded from SQLite must preserve a defined interpretation. Existing timestamps must not be rewritten merely to add presentation preference.
9. **Localization:** keep `g.locale`/Flask-Babel language selection independent; decide date/time format localization after zone conversion and translated validation messages for invalid zones.
10. **Acceptance plan:** require migration upgrade/downgrade tests, form/API valid-invalid-zone tests, anonymous/default behavior, two users viewing the same instant in different zones, DST-boundary vectors, post/message/profile rendering, no double conversion, and unchanged UTC persistence.

## Required next state

Sol produces an ADR and a file/task ownership plan spanning model+migration, form/routes/API, rendering/localization, and tests. The project owner approves items 1–7. The host then issues a new plan revision and canonical digest verbatim. Until then: no worker task, migration, product write, or validation command.
