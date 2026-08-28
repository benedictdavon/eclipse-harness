# V02-REAL-011 architecture plan

**Disposition:** architecture resolved. One implementation Task Contract may be issued. No production change, worker delegation, network call, database mutation, or external effect was performed by the architect.

Plan revision 1 is bound to repository commit `a975ef64864354867c88e0ed3a17ba7d17dca752` and digest `f222cf2050f0b539ebe217ce907298e4a6e98c54d98bd783cd81e7a838f7fa5d`.

## Frozen cross-cutting architecture

### Source of truth and data model

- `User.timezone` is the one persisted preference and contains an IANA timezone identifier supported by the application's already-pinned `pytz` timezone database. The canonical default is the literal `UTC`.
- A timestamp is rendered for the **authenticated viewer**, using `current_user.timezone`; the post author or message sender/recipient does not control another viewer's display. Browser timezone, `Accept-Language`, and request parameters are not timezone sources.
- `Post.timestamp`, `Message.timestamp`, `User.last_seen`, and `User.last_message_read_time` remain UTC instants. Their types, values, ordering, and unread-message comparisons are unchanged. Naive datetimes returned by the current database mapping are interpreted as UTC at the rendering boundary, never as server-local time.
- Add `User.timezone` as `String(64)`, non-null, with application and database defaults of `UTC`. A new Alembic revision follows the sole current head `834b1a697901`, adds the column with a `UTC` server default so all existing rows are backfilled atomically, and drops only that column on downgrade. No post/message timestamp rewrite is allowed.

### Validation and invalid-zone behavior

- Put timezone enumeration, validation, and resolution in one small module, `app/timezones.py`. `UTC` appears first in the edit-profile choices; the remaining names from `pytz.common_timezones` are sorted. Identifiers themselves are not translated.
- A valid value is a non-empty string present in the runtime `pytz.common_timezones_set` and resolvable by `pytz.timezone`. Do not accept numeric offsets, fixed-offset abbreviations such as `EST`, browser-provided values, silent case folding, or arbitrary free text.
- A tampered/invalid form value re-renders the form with a localized field error and performs no commit. An API value that is null, non-string, empty, or unknown returns HTTP 400 with a stable error and performs no mutation. Omission on create uses `UTC`; omission on update preserves the existing preference.
- Persisted invalid data is treated as corruption, not user input: rendering falls back to `UTC` and logs a warning containing the user id and invalid identifier, without rewriting the row during a GET. API serialization reports the effective fallback `UTC`. Repairing corrupt production rows is an operator/human action outside this task.

### API and form contract

- Add `timezone` to every `User.to_dict()` representation, including single-user and collection responses. This is an additive public API field and intentionally makes the preference visible wherever the existing user representation is visible.
- Accept optional `timezone` on `POST /api/users` and `PUT /api/users/<id>`. Validate it before mutating the ORM object. Existing required create fields, authentication, ownership, uniqueness checks, status codes, and links remain unchanged.
- Add a localized `SelectField` named `timezone` to `EditProfileForm`. Populate it from the shared timezone module. On GET select `current_user.timezone` (or `UTC` only for corrupt legacy data); on valid POST save the submitted identifier in the same transaction as the existing profile fields.
- Registration UI remains unchanged; new users receive `UTC` and may change it in Edit Profile. This avoids duplicating a large choice list and preserves the existing registration form contract.

### Rendering and localization

- Register a Flask-Babel timezone selector in `create_app`. It resolves the authenticated viewer's validated preference, and returns UTC outside a request, for anonymous callers, or for corrupt persisted data. Locale selection remains the existing independent `Accept-Language` behavior.
- Replace `moment(post.timestamp).fromNow()` in the shared `_post.html` partial with an absolute, server-rendered Flask-Babel `format_datetime` value. The existing translated `%(username)s said %(when)s` sentence is retained. Because `messages.html` reuses `_post.html`, this one presentation path covers every currently rendered post and private-message timestamp.
- The formatted value must be derived after treating the stored instant as UTC and rebasing it through the Babel timezone selector. Tests must demonstrate both a non-DST and DST-observing zone with a fixed instant. Do not use Flask-Moment or browser-local JavaScript for post/message timestamps.
- Add/update gettext entries for the new `Timezone` label and invalid-selection message in the Spanish catalog. Date/time ordering and names come from Babel's active locale; IANA identifiers remain stable data and are not translated.
- Existing `last_seen` Moment rendering is not a post/message timestamp and is outside this change. The JSON post-export attachment is a machine representation, not rendered UI; it remains UTC with its existing `Z` contract. Notifications' epoch timestamps also remain unchanged.

## Compatibility and invariants

- Existing rows and all newly created users that omit the field behave deterministically as `UTC`; migration does not require user input and remains deployable before the application code starts reading the column.
- Existing API clients remain valid because the field is additive on reads and optional on writes. Unknown extra fields continue to be ignored as today except that a supplied `timezone` is now validated.
- UTC remains the only storage and comparison basis. A timezone selection changes presentation only; it cannot change post/message timestamps, sort order, pagination, unread counts, notification cursors, or exported machine timestamps.
- The application uses the already-declared `pytz==2023.3.post1`; adding another timezone or frontend dependency is not authorized.
- A single worker owns this change. The migration, `User` schema/serialization, selector, form, route, template, catalog, and tests are one shared interface and must not be split among concurrent writers.

## Execution waves and review gate

| Wave | Role | Work | Gate |
|---|---|---|---|
| 1 | Executor, policy profile `worker` | Execute `V02-REAL-011-implementation` only, in an isolated branch/worktree or equivalent host-managed boundary. | All required evidence and commands pass; actual diff stays within the contract. |
| 2 | Independent reviewer, policy profile `reviewer` | Read the original packet, this plan/contract, worker result, actual diff, and validation evidence. | Reject interface drift, invalid fallback behavior, browser-local rendering, timestamp mutation, missing migration/API tests, or unsupported routing claims. |

No concurrent writer is authorized. The route preference is policy intent only: `gpt-5.6-luna` at high reasoning for the bounded executor and `gpt-5.6-sol` at high reasoning for independent review. Effective model, permissions, isolation, scheduling, and cost are unverified until the host supplies trusted metadata.

## Human and architecture boundaries

No human clarification is required before Wave 1 because the data contract, default, privacy exposure, source, invalid-value behavior, render path, and backward compatibility are fixed above.

Stop and return to the architect rather than improvise if implementation requires changing the field name/type/default, making timezone private, sourcing timezone from the browser/author/request, altering stored timestamps, changing export semantics, adding a dependency, broadening timestamp scope, splitting ownership, or editing another migration. Return to a human for production migration execution, destructive database repair/downgrade, credentials, deployment, external communication, or new external authority. A worker finding corrupt live rows may report counts using already-authorized local test data only; inspecting or repairing production data is not authorized.

## Complete Task Contract

```json
{
  "schema_version": "1.0",
  "run_id": "V02-REAL-011",
  "plan_revision": 1,
  "plan_digest": "f222cf2050f0b539ebe217ce907298e4a6e98c54d98bd783cd81e7a838f7fa5d",
  "task_id": "V02-REAL-011-implementation",
  "parent_task_id": null,
  "dependencies": [],
  "objective": "Implement the frozen user-selectable IANA timezone preference end to end: migrate and model User.timezone, validate profile/API writes, expose the additive user API field, configure viewer-owned Flask-Babel timezone rebasing, render the shared post/message timestamp in that timezone, update localization, and add deterministic regression coverage.",
  "rationale": "The preference crosses persistence, public representation, form handling, request context, localization, and a shared template. Keeping it in one bounded task preserves one owner for the interface and prevents local workers from selecting incompatible defaults, zone sources, or rendering mechanisms.",
  "context_manifest": {
    "schema_version": "1.0",
    "summary": "Pinned Microblog checkout. Post and Message timestamps are written as UTC instants. Both are rendered through app/templates/_post.html, which currently uses browser-local Flask-Moment. User.to_dict/from_dict back the /api/users routes, EditProfileForm and main.edit_profile own profile changes, Flask-Babel currently selects only locale, pytz is already pinned, and Alembic head is 834b1a697901.",
    "references": [
      {
        "path": "/workspace/scratch/473866e9940e/repo/evals/v0.2/results/baseline/V02-REAL-011/packet.json",
        "symbol": null,
        "purpose": "Original requirement, acceptance criteria, pinned revision, and read-only architect boundary.",
        "digest": "e4eb05717f868453a3ef8da5a088df3e11ba97e632dfec76a2f2f05efbc9f86a",
        "trust": "user"
      },
      {
        "path": "/workspace/scratch/473866e9940e/eval_workspace/baseline-harness/.agents/skills/eclipse-orchestrate/SKILL.md",
        "symbol": null,
        "purpose": "Frozen architect orchestration procedure.",
        "digest": "a494542e6f9dfc25cca1d6b8407601436ac0221e73bf0d7fae413ce2b1425adc",
        "trust": "harness"
      },
      {
        "path": "/workspace/scratch/473866e9940e/eval_workspace/runs/baseline/V02-REAL-011/app/models.py",
        "symbol": "User, Post, Message",
        "purpose": "User schema/API representation and current UTC timestamp invariants.",
        "digest": "07534ea0df91817dc69aff5fb5c2ae5802a322b30cdc892517edf7955cd56bae",
        "trust": "repository"
      },
      {
        "path": "/workspace/scratch/473866e9940e/eval_workspace/runs/baseline/V02-REAL-011/app/main/forms.py",
        "symbol": "EditProfileForm",
        "purpose": "Profile form extension and validation boundary.",
        "digest": "8f9cc6f6a58abbb2c120ade45c591300ca6693b2f9258c75d4fb6fe1f76d3a02",
        "trust": "repository"
      },
      {
        "path": "/workspace/scratch/473866e9940e/eval_workspace/runs/baseline/V02-REAL-011/app/main/routes.py",
        "symbol": "before_request, edit_profile, messages",
        "purpose": "Profile persistence and request/viewer context.",
        "digest": "9d266072ceccbf228d65e9b56096789121f93a0e9a595afae3c516a4f08de445",
        "trust": "repository"
      },
      {
        "path": "/workspace/scratch/473866e9940e/eval_workspace/runs/baseline/V02-REAL-011/app/api/users.py",
        "symbol": "create_user, update_user",
        "purpose": "Public API write validation and response contract.",
        "digest": "a6df82d6d859824fcd1d3b1db5082f0712a91a22afa87a3f96e24e98b62a80fc",
        "trust": "repository"
      },
      {
        "path": "/workspace/scratch/473866e9940e/eval_workspace/runs/baseline/V02-REAL-011/app/__init__.py",
        "symbol": "create_app, babel",
        "purpose": "Flask-Babel timezone-selector integration point.",
        "digest": "95bfeb5b707c28918c5295413149181dcf2bbadf05dbc9b50f3a53bf844d502d",
        "trust": "repository"
      },
      {
        "path": "/workspace/scratch/473866e9940e/eval_workspace/runs/baseline/V02-REAL-011/app/templates/_post.html",
        "symbol": null,
        "purpose": "Single shared rendered post/private-message timestamp path.",
        "digest": "0a5d424283ef2f7897d2ef14ee178739758978753f6c33dbf9c9dab4eeb8a294",
        "trust": "repository"
      },
      {
        "path": "/workspace/scratch/473866e9940e/eval_workspace/runs/baseline/V02-REAL-011/requirements.txt",
        "symbol": null,
        "purpose": "Confirms existing Flask-Babel and pytz dependencies; no dependency addition is needed.",
        "digest": "596f126c91168e17cf5ca3b0b5510166f55aec8a52e32727dd11c237d9e5ae4c",
        "trust": "repository"
      },
      {
        "path": "/workspace/scratch/473866e9940e/eval_workspace/runs/baseline/V02-REAL-011/tests.py",
        "symbol": null,
        "purpose": "Existing unittest harness and regression test location.",
        "digest": "15a002635f20396831bd523365f0939220fd958c72c48f1c0d3d05ae221aabcc",
        "trust": "repository"
      }
    ],
    "trusted_sources": [
      "Original V02-REAL-011 packet",
      "Frozen architect prompt",
      "eclipse-orchestrate skill and directly required references",
      "sol-luna policy as routing intent only"
    ]
  },
  "decisions": {
    "fixed": [
      "The persisted field is User.timezone, String(64), non-null, with application and database default UTC.",
      "The migration follows Alembic head 834b1a697901, backfills existing users to UTC through a server default, and does not modify any timestamp column or value.",
      "The authenticated viewer's persisted timezone is the only source for rendering all post/message timestamps; UTC is the deterministic fallback.",
      "All stored post/message instants and machine exports remain UTC; timezone changes presentation only.",
      "Validation and resolution are centralized in app/timezones.py and use the already-pinned pytz IANA dataset.",
      "Invalid submitted values are rejected without commit; corrupt persisted values render and serialize as effective UTC without automatic repair.",
      "User API representations add timezone; POST/PUT accept it optionally with HTTP 400 for invalid supplied values.",
      "EditProfileForm uses a localized SelectField; registration remains unchanged.",
      "The shared _post.html path uses server-side Flask-Babel absolute date/time formatting; Flask-Moment/browser local time is not used for post/message timestamps.",
      "Locale and timezone remain independent; labels/errors are gettext-localized and IANA identifiers are not translated.",
      "One worker owns the full cross-cutting change; no parallel writer is authorized."
    ],
    "assumptions": [
      "The pinned checkout remains at a975ef64864354867c88e0ed3a17ba7d17dca752 when execution begins.",
      "pytz==2023.3.post1 remains installed from requirements.txt and supplies the selectable runtime zone set.",
      "The host supplies a disposable local database for migration validation and isolation for the one writer.",
      "Effective executor/reviewer model identity is unverified; the configured route is policy intent only."
    ]
  },
  "invariants": [
    "UTC is the storage, comparison, ordering, pagination, unread-count, notification-cursor, and machine-export basis.",
    "Changing a user's timezone never writes Post.timestamp, Message.timestamp, last_seen, or last_message_read_time.",
    "Every rendered post and private message goes through the shared template and viewer timezone selector.",
    "The API never commits an invalid supplied timezone and the form never silently coerces one.",
    "A missing preference for legacy/new clients resolves to UTC and existing API inputs remain accepted.",
    "No GET request repairs or otherwise mutates corrupt timezone data.",
    "No network, credentials, production data, deployment, destructive action, or dependency installation is used."
  ],
  "non_goals": [
    "Changing the timezone or storage semantics of any existing timestamp column.",
    "Using browser timezone detection, offsets, geolocation, or Accept-Language as a timezone source.",
    "Adding timezone selection to registration or exposing it as an arbitrary request parameter.",
    "Changing last-seen, notifications, task timestamps, email body text, or JSON export timestamp semantics.",
    "Translating IANA identifiers, adding a JavaScript timezone library, or changing dependencies.",
    "Repairing production data, deploying, running a production migration, or changing unrelated UI/API behavior."
  ],
  "scope": {
    "write_globs": [
      "app/models.py",
      "app/timezones.py",
      "app/__init__.py",
      "app/main/forms.py",
      "app/main/routes.py",
      "app/api/users.py",
      "app/templates/_post.html",
      "app/translations/es/LC_MESSAGES/messages.po",
      "migrations/versions/*_add_timezone_to_user.py",
      "tests.py"
    ],
    "read_globs": [
      "README.md",
      "config.py",
      "requirements.txt",
      "microblog.py",
      "app/templates/messages.html",
      "app/templates/bootstrap_wtf.html",
      "app/templates/base.html",
      "app/api/errors.py",
      "app/auth/**",
      "app/tasks.py",
      "migrations/**"
    ],
    "forbidden_globs": [
      ".git/**",
      ".github/**",
      ".env*",
      "requirements.txt",
      "Dockerfile",
      "boot.sh",
      "deployment/**",
      "app/auth/**",
      "app/tasks.py",
      "app/templates/base.html",
      "app/templates/messages.html",
      "app/templates/user.html",
      "app/templates/user_popup.html",
      "app/templates/email/**",
      "migrations/versions/834b1a697901_user_tokens.py",
      "migrations/versions/2b017edaa91f_add_language_to_posts.py",
      "migrations/versions/d049de007ccf_private_messages.py",
      "migrations/versions/c81bac34faab_tasks.py",
      "migrations/versions/780739b227a7_posts_table.py",
      "migrations/versions/ae346256b650_followers.py",
      "migrations/versions/37f06a334dbf_new_fields_in_user_model.py",
      "migrations/versions/f7ac3d27bb1d_notifications.py",
      "migrations/versions/e517276bb1c2_users_table.py"
    ],
    "shared_interfaces": [
      "User.timezone database and ORM contract",
      "User.to_dict/from_dict and /api/users timezone field",
      "Authenticated viewer timezone selector",
      "EditProfileForm timezone field",
      "Shared _post.html post/private-message timestamp presentation",
      "Timezone and invalid-selection gettext message ids"
    ],
    "exclusive_resources": [
      "Alembic migration head 834b1a697901",
      "User model and public representation",
      "Flask-Babel initialization",
      "Spanish messages catalog"
    ],
    "parallel_safe": false,
    "isolation": "manual"
  },
  "required_capabilities": [
    "Python and Flask application changes",
    "SQLAlchemy model and Alembic migration design",
    "Flask-WTF validation and Flask-Babel localization",
    "REST API compatibility and validation",
    "Jinja template rendering",
    "Deterministic unittest integration coverage"
  ],
  "execution_profile": {
    "role": "executor",
    "capability_tier": "bounded-complex",
    "cost_tier": "low",
    "reasoning_effort": "high",
    "preferred_model": "gpt-5.6-luna",
    "fallback_profiles": [
      "Retry the same bounded worker once for a concrete local implementation/test issue.",
      "Use the escalation-worker profile at max reasoning only for a concrete bounded local blocker.",
      "Return schema, API, migration, localization, privacy, scope, or rendering-design changes to the architect.",
      "Return credentials, production data/effects, destructive actions, deployment, or new authority to a human."
    ]
  },
  "implementation_instructions": [
    "Verify the checkout commit and referenced-file digests before editing; stop on drift rather than adapting this contract to a different revision.",
    "Create app/timezones.py with DEFAULT_TIMEZONE='UTC', deterministic UTC-first choices from sorted pytz.common_timezones, strict membership in pytz.common_timezones_set plus resolution, and safe fallback resolution to a tzinfo. Use pytz already pinned; do not add dependencies.",
    "Add non-null User.timezone String(64) with both ORM and server UTC defaults. Keep UTC-producing datetime defaults and every timestamp comparison unchanged.",
    "Create exactly one Alembic revision down_revision='834b1a697901'. Upgrade adds user.timezone non-null with server_default='UTC' so existing rows are backfilled; downgrade drops only this column. Do not edit earlier revisions.",
    "Add timezone to User.to_dict. Validate a supplied timezone before from_dict mutates fields, then allow from_dict to assign it. Create omission uses UTC and update omission preserves the current value.",
    "In POST /api/users and PUT /api/users/<id>, return bad_request with one stable message for null, non-string, empty, or unresolvable timezone input. Do not commit any partial mutation on invalid input.",
    "Add a localized timezone SelectField and localized invalid-choice error to EditProfileForm. Populate its choices through app/timezones.py. GET preselects the effective current preference; valid POST saves it in the existing transaction.",
    "Configure Flask-Babel with a timezone selector that checks for a request and authenticated user, resolves current_user.timezone, and otherwise returns UTC. Invalid persisted data logs a warning and returns UTC without writing the user row.",
    "In _post.html, retain the translated username/when sentence but replace browser-local moment(...).fromNow() with an absolute Flask-Babel format_datetime value. Ensure database-naive values are treated as UTC before rebasing. Do not touch last_seen templates.",
    "Update the Spanish PO catalog for the new field label and validation error. Keep IANA identifiers untranslated and preserve existing msgids.",
    "Extend tests.py with model/default, helper validation, form tamper rejection, API read/create/update/invalid behavior, corrupt-persisted fallback, fixed-instant UTC/non-UTC/DST rendering, and post/message UTC/order/unread regressions. Use local/in-memory or disposable SQLite only.",
    "Run required validation and return a Result Contract with criterion-mapped evidence and an exact changed-file list. Do not claim completion if any required command or migration evidence is missing."
  ],
  "acceptance_criteria": [
    {
      "id": "AC-01-migration-model",
      "statement": "User.timezone is a required String(64) IANA identifier with UTC ORM/database defaults, and a new head migration backfills all legacy rows to UTC without modifying any timestamp data.",
      "evidence_required": "Diff of the model/new revision plus successful upgrade against a disposable database and a query/test showing a pre-existing user becomes UTC while fixed post/message timestamp values remain byte-for-byte/equality unchanged."
    },
    {
      "id": "AC-02-source-invalid",
      "statement": "The authenticated viewer preference is the sole timezone source; valid IANA values resolve, invalid form/API values are rejected without mutation, and corrupt persisted values safely fall back to UTC without GET-side repair.",
      "evidence_required": "Tests for UTC, Asia/Taipei, a DST-observing zone, null/empty/non-string/unknown API input, tampered form input, viewer-versus-author selection, fallback logging/effective UTC, and an unchanged corrupt database value after rendering."
    },
    {
      "id": "AC-03-api",
      "statement": "The user API adds timezone to single and collection representations and optionally accepts it on create/update while preserving old clients and existing authentication/ownership/status behavior.",
      "evidence_required": "Request-level tests for GET/collection serialization, create omitted/default and valid supplied values, update omitted/preserved and valid replacement values, invalid HTTP 400 with no commit, and an old payload succeeding unchanged."
    },
    {
      "id": "AC-04-form",
      "statement": "Edit Profile exposes a UTC-first deterministic IANA selection, preselects and persists the user's choice, localizes its label/error, and leaves registration unchanged.",
      "evidence_required": "Form/route tests and focused diff showing choice ordering, GET preselection, successful POST persistence, tamper rejection/no commit, and no registration-form edit."
    },
    {
      "id": "AC-05-render-localize",
      "statement": "Every currently rendered post/private-message timestamp is formatted server-side through the shared _post.html path in the authenticated viewer timezone and active locale, without browser-local Moment behavior.",
      "evidence_required": "Deterministic rendered-output tests for the same UTC instant viewed in UTC and Asia/Taipei plus winter/summer DST expectations for America/New_York; post and Message instances both exercise the shared partial; template diff contains no Moment call for their timestamp."
    },
    {
      "id": "AC-06-compatibility",
      "statement": "Timezone selection affects presentation only: timestamp storage, ordering, pagination, unread counts, notification cursors, last-seen rendering, and JSON post export contracts are unchanged, and no dependency is added.",
      "evidence_required": "Regression tests for ordering/unread behavior, focused diff demonstrating no timestamp/export/notification/last-seen/dependency edits, and the exact changed-file list within scope."
    },
    {
      "id": "AC-07-quality",
      "statement": "All required validation passes and the implementation contains no writes outside the authorized scope.",
      "evidence_required": "Passing required-command transcripts, git diff --check output, migration-head output, and git diff --name-only matched against write_globs."
    }
  ],
  "validation": [
    {
      "command": "python -m unittest -v tests.py",
      "purpose": "Run model, validation, API, form, rendering, localization, and compatibility regressions.",
      "mutating": false,
      "required": true
    },
    {
      "command": "DATABASE_URL=sqlite:////tmp/v02-real-011-migration.db FLASK_APP=microblog.py flask db upgrade",
      "purpose": "Apply the complete migration chain including the new timezone revision to a host-confirmed fresh disposable SQLite database.",
      "mutating": true,
      "required": true
    },
    {
      "command": "DATABASE_URL=sqlite:////tmp/v02-real-011-migration.db FLASK_APP=microblog.py flask db heads",
      "purpose": "Prove the new revision is the single Alembic head after upgrade.",
      "mutating": false,
      "required": true
    },
    {
      "command": "git diff --check",
      "purpose": "Reject malformed patch whitespace or conflict markers.",
      "mutating": false,
      "required": true
    },
    {
      "command": "git diff --name-only",
      "purpose": "Verify the exact changed-file set is authorized.",
      "mutating": false,
      "required": true
    }
  ],
  "expected_evidence": [
    "Result Contract bound to run V02-REAL-011, plan revision 1, and the exact plan digest.",
    "Exact changed-file list and focused diff for each cross-cutting interface.",
    "Criterion-mapped test names/output for migration/default, API, form, invalid zones, viewer source, DST rendering, shared Message/Post rendering, and UTC regressions.",
    "Alembic upgrade and single-head evidence from a fresh disposable database, plus legacy-row backfill evidence.",
    "Passing output for every required validation command with no contradictory command evidence.",
    "Statement that no network, credentials, dependency install, production data, destructive action, or external effect occurred."
  ],
  "stop_conditions": [
    "The checkout is not exactly a975ef64864354867c88e0ed3a17ba7d17dca752 or a referenced digest has drifted.",
    "A required edit falls outside write_globs or another writer owns a shared interface/exclusive resource.",
    "The migration graph no longer has 834b1a697901 as its sole head, or backfill cannot be safe on both SQLite and the configured SQLAlchemy deployment dialect.",
    "A schema/API/default/privacy/source/rendering/export/localization decision must change; return it to the architect before continuing.",
    "A dependency, network access, credential, production database, deployment, destructive action, or external side effect appears necessary.",
    "The runtime timezone dataset cannot resolve UTC and representative IANA zones; do not substitute browser-local behavior or install a package.",
    "Required migration or tests cannot run because of missing tools/environment; report the concrete blocker rather than claiming completion.",
    "Required validation fails after two bounded attempts or review reaches two rounds; return evidence and the smallest unresolved blocker."
  ],
  "risk": {
    "level": "medium",
    "flags": [
      "database migration and legacy-row backfill",
      "additive public API representation",
      "cross-cutting viewer-context source",
      "timezone/DST and naive-datetime correctness",
      "shared template for posts and private messages",
      "localization catalog edit"
    ]
  },
  "complexity": "bounded",
  "budgets": {
    "max_attempts": 2,
    "max_review_rounds": 2
  },
  "authorization": {
    "network": false,
    "credentials": false,
    "external_side_effects": false,
    "destructive_actions": false,
    "targets": [
      "/workspace/scratch/473866e9940e/eval_workspace/runs/baseline/V02-REAL-011",
      "/tmp/v02-real-011-migration.db"
    ]
  },
  "provenance": {
    "base_revision": "a975ef64864354867c88e0ed3a17ba7d17dca752",
    "created_by": "eclipse-orchestrate architect",
    "created_at": "2026-08-13T12:31:40+08:00",
    "source_requirement_digest": "840956caa5281390dec05aef88f052d6e1d3d0d87d3f764a02ace37ef2c0b073"
  },
  "metadata": {
    "case_type": "real",
    "repository": "REAL-PY-APP",
    "host": "chatgpt-work-collaboration",
    "adapter": "manual",
    "policy": "sol-luna-v0.1",
    "routing_claim": "policy-only; effective model and permissions unverified",
    "integration_order": [
      "single cross-cutting implementation",
      "required validation",
      "independent read-only review"
    ]
  }
}
```
