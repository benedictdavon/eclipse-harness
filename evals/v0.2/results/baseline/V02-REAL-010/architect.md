# V02-REAL-010 architecture packet

## Disposition

The requirement is executable as one bounded implementation task. Plan revision 1 is approved for dispatch subject to the identity, scope, and environment checks in the contract. No clarification, broader architecture, migration, or new human authority is required, and no production implementation was performed during architecture.

The change is local to three duplicated methods on `User`: each currently constructs the same `select(count())` over a relationship-select subquery and executes it with `db.session.scalar`. The implementation must extract that construction into one private instance helper, preserve each public entry point and its corresponding relationship, retain the existing follow-count coverage, and add direct zero/one coverage for `posts_count`.

## Plan identity

- Run: `V02-REAL-010`
- Plan revision: `1`
- Plan digest: `sha256:633b8276e63ba3c0ff8177d2a5b1b524748922af4ce5a347fcd5ee9a632082d8`
- Base revision: `a975ef64864354867c88e0ed3a17ba7d17dca752`
- Requirement digest: `sha256:c0050986b4477cc2b82404dfaeea57d47aed9cf45b8d269d49f08f98de81f904`

The plan digest is SHA-256 over these exact UTF-8 bytes, with no trailing newline:

```json
{"base_revision":"a975ef64864354867c88e0ed3a17ba7d17dca752","fixed_decisions":["introduce one private User._count_relationship helper that performs the existing select(count()).select_from(relationship.select().subquery()) construction and returns db.session.scalar(query)","keep followers_count, following_count, and posts_count public names and make each delegate to the helper with self.followers, self.following, and self.posts respectively","retain the existing follow-count coverage and add one focused posts_count unittest covering zero and one without changing migrations or unrelated behavior"],"plan_revision":1,"run_id":"V02-REAL-010","task_ids":["V02-REAL-010-T01"],"waves":[["V02-REAL-010-T01"]]}
```

Any architecture change requires plan revision 2, a new digest, and supersession of the nonterminal revision-1 contract.

## Frozen decisions

1. Add exactly one private instance helper, `User._count_relationship`. It receives a write-only relationship collection, constructs the same `sa.select(sa.func.count()).select_from(relationship.select().subquery())` query, and returns `db.session.scalar(query)`.
2. Keep `followers_count()`, `following_count()`, and `posts_count()` public and zero-argument. They delegate with `self.followers`, `self.following`, and `self.posts`, respectively.
3. The helper may remove duplication but may not alter the query row set or scalar behavior: no filter, join, distinct, coalesce, cast, alternate session API, or fallback value.
4. Retain `UserModelCase.test_follow` as its current zero/one coverage for follower and following counts. Add exactly one focused `test_posts_count` that persists a user, proves zero, persists one authored post, and proves one.
5. Writes are limited to `app/models.py` and `tests.py`. No migration, mapping, schema, dependency, configuration, API, template, documentation, or new-file change is authorized.
6. Validation bytecode is redirected to `/tmp/eclipse-V02-REAL-010-pycache`; no repository cache generation or destructive cleanup is authorized.

## Task and execution wave

| Wave | Task | Dependencies | Exclusive ownership | Isolation | Parallel-safe |
|---|---|---|---|---|---|
| 1 | `V02-REAL-010-T01` | none | `User` count helper/public methods and `UserModelCase` count coverage | host-provided worktree | `false` |

There is one task because the helper, all three delegations, and their regression coverage are one atomic behavior-preserving acceptance unit within the packet's shared two-file scope. Splitting it would create incomplete intermediate states and overlapping ownership. No concurrent writer is authorized. The deterministic checker confirmed the DAG and returned `[["V02-REAL-010-T01"]]`; the host owns dispatch, isolation, workflow state, and integration.

## Validation and evidence gates

The worker must run the focused unittest command for the retained follower/following cases and new posts case, the packet-required `compileall` operation, a scoped whitespace check, and repository-wide path/status checks. The `PYTHONPYCACHEPREFIX` assignments retain the required Python module and arguments while moving bytecode writes outside the repository. Each command needs its exact exit status and concise output, including silent successes.

Acceptance requires direct evidence for:

- exactly one private helper owning the unchanged query construction;
- unchanged public method signatures and correct zero/one results through all three public methods;
- no filter, distinct, join, coercion, fallback, relationship, schema, or migration drift;
- successful compilation and final repository status containing only `app/models.py` and `tests.py`.

A missing command, nonzero required exit, uncovered criterion, extra path, stale base, owned-file digest mismatch, or contradictory evidence makes the result incomplete or blocked.

## Risk and routing assumptions

Risk is low and complexity is bounded. The main risk is making a superficially equivalent refactor that changes ORM query or return semantics. The exact helper flow, direct relationship mapping, retained zero/one assertions, focused new post-count test, symbol-level exclusive ownership, and exact-file write scope control that risk.

Under `sol-luna-v0.1`, the configured policy preference is `worker-lite`: executor, bounded-routine capability, low cost tier, medium reasoning effort, and preferred model `gpt-5.6-luna`. This is policy-only routing. The manual adapter provides no trusted observation of the effective model, permissions, or cost, so none is claimed as verified. A concrete still-bounded reasoning blocker may use the configured worker fallback; interface, query-semantics, test-design, scope, migration, or concurrency changes return to the architect.

## Human and host boundaries

No human response is needed before dispatch if the base revision, plan identity, owned-file digests, and clean isolated checkout match. The host owns scheduling, worktree or branch isolation, workflow status, git integration, and final review.

Stop and return evidence instead of improvising if the checkout is stale or overlapping, a required dependency or tool is unavailable, the exact query semantics cannot be retained for all three relationships, validation cannot keep bytecode outside the repository, an unrelated test failure prevents acceptance, or any solution needs broader files or semantics. Credentials, destructive actions, dependency installation, network access, external effects, expanded permissions, and verified-routing guarantees require new human authority and are not granted by this packet.

## Architect validation evidence

- The task contract passed `eclipse validate --kind task` through the repository-local optional CLI.
- Canonical task-contract digest: `sha256:1dc825421b5a9a6ac70556fbb54bd57e018b28bce76e6a352d516b9b5d45e213`.
- The plan digest recomputed from the exact `metadata.plan_digest_input` bytes and matched the declared value.
- `eclipse check-concurrency --max-writers 1` reported a valid DAG and the single wave `[["V02-REAL-010-T01"]]`.
- The pinned checkout was clean at the required base revision, and the owned-file digests matched the context manifest.
- No implementation edit or application/test validation was performed in the pinned checkout during architecture.

## Complete Task Contract

The same machine-readable contract is provided separately as `task.json`.

```json
{
  "schema_version": "1.0",
  "run_id": "V02-REAL-010",
  "plan_revision": 1,
  "plan_digest": "sha256:633b8276e63ba3c0ff8177d2a5b1b524748922af4ce5a347fcd5ee9a632082d8",
  "task_id": "V02-REAL-010-T01",
  "parent_task_id": null,
  "dependencies": [],
  "objective": "Refactor User.followers_count, User.following_count, and User.posts_count to share one private relationship-count helper while preserving their public names, SQL construction, scalar return behavior, and focused regression coverage.",
  "rationale": "All three methods duplicate the same SQLAlchemy count construction and differ only in the write-only relationship selected. A private User._count_relationship helper can own that unchanged construction while each public method supplies its existing relationship; the existing follow test plus one focused posts-count test directly exercise all three public entry points at zero and one.",
  "context_manifest": {
    "schema_version": "1.0",
    "summary": "At base revision a975ef64864354867c88e0ed3a17ba7d17dca752, User.followers_count, User.following_count, and User.posts_count each build sa.select(sa.func.count()).select_from(<relationship>.select().subquery()) and return db.session.scalar(query). User.followers, User.following, and User.posts are SQLAlchemy write-only relationships. tests.UserModelCase.test_follow already proves zero and one for following_count and followers_count using the in-memory SQLite fixture; posts_count lacks direct count coverage. Extract only the duplicated construction into a private instance helper, delegate the three public methods to it, retain test_follow, and add one direct zero/one posts_count unittest. Migrations and query semantics remain untouched.",
    "references": [
      {
        "path": "/workspace/scratch/473866e9940e/repo/evals/v0.2/results/baseline/V02-REAL-010/packet.json",
        "symbol": null,
        "purpose": "Authoritative requirement, allowed write scope, acceptance criteria, required compile command, policy, and pinned revision.",
        "digest": "sha256:c0050986b4477cc2b82404dfaeea57d47aed9cf45b8d269d49f08f98de81f904",
        "trust": "harness"
      },
      {
        "path": "/workspace/scratch/473866e9940e/repo/evals/v0.2/prompts/architect.md",
        "symbol": null,
        "purpose": "Frozen architect role, read-only planning boundary, and output requirements.",
        "digest": "sha256:a8e484e802d361e2236c7b7221ae84c40037fca40815cb6ae695b5897528e931",
        "trust": "harness"
      },
      {
        "path": "/workspace/scratch/473866e9940e/repo/AGENTS.md",
        "symbol": null,
        "purpose": "Applicable Eclipse workflow, role separation, and repository policy.",
        "digest": "sha256:a366165b64fd24fdb33cf4c95a557605ea0aed337ba97c9e9ed6821e294c6f77",
        "trust": "project-config"
      },
      {
        "path": "/workspace/scratch/473866e9940e/repo/.agents/skills/eclipse-orchestrate/SKILL.md",
        "symbol": null,
        "purpose": "Task-contract construction, routing, concurrency, and human-boundary process used for this plan.",
        "digest": "sha256:a494542e6f9dfc25cca1d6b8407601436ac0221e73bf0d7fae413ce2b1425adc",
        "trust": "project-config"
      },
      {
        "path": "/workspace/scratch/473866e9940e/repo/policies/sol-luna.json",
        "symbol": "profiles.worker-lite",
        "purpose": "Configured routing preference for a small deterministic implementation task.",
        "digest": "sha256:0748e68bb125b6aa8e3a36893b43966217953d01828c6c84306d6ed8caa7fcbf",
        "trust": "project-config"
      },
      {
        "path": "app/models.py",
        "symbol": "User.followers; User.following; User.posts; User.followers_count; User.following_count; User.posts_count",
        "purpose": "Owned production relationships and the three duplicated count methods to refactor.",
        "digest": "sha256:07534ea0df91817dc69aff5fb5c2ae5802a322b30cdc892517edf7955cd56bae",
        "trust": "repository"
      },
      {
        "path": "tests.py",
        "symbol": "TestConfig; UserModelCase.test_follow; UserModelCase.test_follow_posts",
        "purpose": "Owned standard-library unittest module, in-memory database fixture, existing follow-count coverage, and Post construction examples.",
        "digest": "sha256:15a002635f20396831bd523365f0939220fd958c72c48f1c0d3d05ae221aabcc",
        "trust": "repository"
      },
      {
        "path": "app/__init__.py",
        "symbol": "db; create_app",
        "purpose": "Read-only application and SQLAlchemy fixture context used by UserModelCase.",
        "digest": "sha256:95bfeb5b707c28918c5295413149181dcf2bbadf05dbc9b50f3a53bf844d502d",
        "trust": "repository"
      },
      {
        "path": "requirements.txt",
        "symbol": "Flask-SQLAlchemy==3.1.1; SQLAlchemy==2.0.23",
        "purpose": "Read-only dependency context for the write-only relationship and select/subquery APIs already in use.",
        "digest": "sha256:596f126c91168e17cf5ca3b0b5510166f55aec8a52e32727dd11c237d9e5ae4c",
        "trust": "repository"
      }
    ],
    "trusted_sources": [
      "/workspace/scratch/473866e9940e/repo/evals/v0.2/results/baseline/V02-REAL-010/packet.json",
      "/workspace/scratch/473866e9940e/repo/evals/v0.2/prompts/architect.md",
      "/workspace/scratch/473866e9940e/repo/AGENTS.md",
      "/workspace/scratch/473866e9940e/repo/.agents/skills/eclipse-orchestrate/SKILL.md",
      "/workspace/scratch/473866e9940e/repo/policies/sol-luna.json"
    ]
  },
  "decisions": {
    "fixed": [
      "Add exactly one private instance helper named User._count_relationship that accepts a write-only relationship collection, constructs sa.select(sa.func.count()).select_from(relationship.select().subquery()), and returns db.session.scalar(query).",
      "Keep followers_count, following_count, and posts_count as public zero-argument instance methods and make each return _count_relationship applied to self.followers, self.following, and self.posts respectively.",
      "Do not add filters, joins, distinct, coalesce, casts, eager loading, alternate session APIs, or any other change to the existing count/subquery/scalar semantics or return values.",
      "Do not reorder unrelated User methods. Place the helper adjacent to the first count methods and change only the three duplicated method bodies needed to delegate.",
      "Retain UserModelCase.test_follow unchanged as the focused zero/one coverage for following_count and followers_count, and add exactly one UserModelCase.test_posts_count method that persists a user, asserts posts_count is zero, persists one authored Post, and asserts posts_count is one.",
      "Repository writes are limited to app/models.py and tests.py. No migration, mapped relationship, schema, dependency, configuration, API, template, documentation, or new-file change is authorized.",
      "Redirect Python bytecode generated by unittest and compileall to /tmp/eclipse-V02-REAL-010-pycache; do not create or destructively clean repository cache files."
    ],
    "assumptions": [
      "The executor starts from the clean pinned base revision and the app/models.py and tests.py digests in the context manifest still match.",
      "SQLAlchemy write-only relationship collections for followers, following, and posts continue to expose the select() method already used by each current public method.",
      "The existing TestConfig, application context, in-memory SQLite fixture, and Post defaults are sufficient for the focused posts_count test.",
      "The host-provided execution environment already contains the pinned dependencies needed by the existing tests.",
      "The existing test_follow assertions remain authoritative focused coverage for the public followers_count and following_count methods."
    ]
  },
  "invariants": [
    "User.followers_count(), User.following_count(), and User.posts_count() retain their public names, zero-argument signatures, call sites, and scalar return behavior.",
    "Each count remains SELECT count(*) FROM (<that same relationship>.select()) AS subquery and executes through db.session.scalar; no relationship or row set is broadened or narrowed.",
    "User.followers, User.following, User.posts, their joins and foreign keys, and all mapped schema declarations remain unchanged.",
    "Existing test_follow behavior and all application behavior outside removal of the duplicated construction remain unchanged.",
    "No migration file or migration metadata is created, edited, renamed, or deleted.",
    "No network, credentials, dependency installation, external effect, destructive action, generated repository file, or unrelated formatting change is authorized."
  ],
  "non_goals": [
    "Changing count SQL for performance, using relationship length, adding caching, adding distinct, or coercing the scalar result to int.",
    "Generalizing counts outside followers_count, following_count, and posts_count, including unread_message_count or pagination totals.",
    "Changing public method names, signatures, return types, callers, API response keys, relationship configuration, or database schema.",
    "Moving methods, reformatting the User model, redesigning the test fixture, or changing existing test_follow assertions.",
    "Adding a migration, dependency, type-checking framework, new test file, documentation, or broader application refactor."
  ],
  "scope": {
    "write_globs": [
      "app/models.py",
      "tests.py"
    ],
    "read_globs": [
      "app/models.py",
      "tests.py",
      "app/__init__.py",
      "requirements.txt",
      "config.py"
    ],
    "forbidden_globs": [
      "migrations/**",
      "app/api/**",
      "app/templates/**",
      "app/__init__.py",
      "requirements.txt",
      "config.py",
      ".git/**"
    ],
    "shared_interfaces": [
      "app.models.User.followers_count()",
      "app.models.User.following_count()",
      "app.models.User.posts_count()"
    ],
    "exclusive_resources": [
      "app.models.User private relationship-count helper and three public count methods",
      "tests.UserModelCase count-method regression coverage"
    ],
    "parallel_safe": false,
    "isolation": "worktree"
  },
  "required_capabilities": [
    "bounded Python refactoring",
    "SQLAlchemy select/subquery and write-only relationship preservation",
    "standard-library unittest authoring",
    "local validation and git-diff evidence capture"
  ],
  "execution_profile": {
    "role": "executor",
    "capability_tier": "bounded-routine",
    "cost_tier": "low",
    "reasoning_effort": "medium",
    "preferred_model": "gpt-5.6-luna",
    "fallback_profiles": [
      "worker: executor/bounded-complex/low/high for a concrete still-bounded local reasoning blocker",
      "manual executor under the same contract",
      "architect for any interface, query-semantics, test-design, scope, migration, or concurrency decision"
    ]
  },
  "implementation_instructions": [
    "Before editing, verify HEAD is a975ef64864354867c88e0ed3a17ba7d17dca752, plan revision 1 is current, the checkout is clean, and the owned-file digests match the context manifest.",
    "In app/models.py, add a private instance method named _count_relationship adjacent to the existing followers_count/following_count methods. It takes one relationship argument, assigns query = sa.select(sa.func.count()).select_from(relationship.select().subquery()), and returns db.session.scalar(query).",
    "Replace the body of followers_count with return self._count_relationship(self.followers), the body of following_count with return self._count_relationship(self.following), and the body of posts_count with return self._count_relationship(self.posts).",
    "Preserve the helper's select(count()) -> select_from(relationship.select().subquery()) -> db.session.scalar(query) flow exactly. Do not add filtering, distinct, coercion, fallback values, alternate execution APIs, type imports, or relationship changes.",
    "Do not change the names or signatures of the three public methods, move unrelated methods, or edit any other production symbol.",
    "In tests.py, retain test_follow unchanged and add exactly one UserModelCase method named test_posts_count. Persist a User with the existing fixture, assert posts_count() equals 0, persist one Post with that user as author, and assert posts_count() equals 1.",
    "Keep the new test deterministic and local: reuse the imported User and Post classes and existing database setup, add no mocks/dependencies/new test file, and do not test unrelated Post ordering or API serialization.",
    "Run every required validation command exactly as listed and capture its command, exit status, and concise output. The PYTHONPYCACHEPREFIX assignment is required to keep bytecode outside the repository; do not delete artifacts because destructive cleanup is not authorized.",
    "Report the exact files changed, a focused diff, criterion-by-criterion evidence, and any blockers or deviations. Do not commit, push, install dependencies, access the network, modify migrations, or claim verified model/cost/permission routing."
  ],
  "acceptance_criteria": [
    {
      "id": "AC-01",
      "statement": "Exactly one private User._count_relationship helper owns the duplicated count-query construction, and all three public count methods delegate to it with their corresponding relationship.",
      "evidence_required": "The focused app/models.py diff shows one helper with the preserved construction and direct delegations from followers_count, following_count, and posts_count; repository search/diff shows no second new count helper."
    },
    {
      "id": "AC-02",
      "statement": "followers_count, following_count, and posts_count preserve their public names, zero-argument behavior, scalar return values, and zero/one results through the existing unittest fixture.",
      "evidence_required": "Exit status 0 and concise output from the focused unittest command running the retained test_follow and new test_posts_count, plus direct diff evidence that signatures are unchanged."
    },
    {
      "id": "AC-03",
      "statement": "The refactor preserves SQL semantics: each count still selects count(*) from the corresponding relationship.select().subquery() and returns db.session.scalar(query), with no filtering, distinct, joins, coercion, or query broadening.",
      "evidence_required": "A focused app/models.py diff demonstrates that the existing query statements moved unchanged into the helper and each caller passes only its original relationship; the worker explicitly maps this diff to AC-03."
    },
    {
      "id": "AC-04",
      "statement": "Focused coverage exists for all three public count methods, modified Python files compile, and tracked/untracked repository changes are confined to app/models.py and tests.py with no migration change.",
      "evidence_required": "The retained test_follow and new zero/one test_posts_count are visible in the focused diff; required unittest and compileall commands exit 0; diff/status evidence lists only app/models.py and tests.py and no migrations or generated repository files."
    }
  ],
  "validation": [
    {
      "command": "PYTHONPYCACHEPREFIX=/tmp/eclipse-V02-REAL-010-pycache python -m unittest tests.UserModelCase.test_follow tests.UserModelCase.test_posts_count",
      "purpose": "Exercise the retained zero/one follower and following counts and the new zero/one post count through all three public methods while keeping import bytecode outside the repository.",
      "mutating": true,
      "required": true
    },
    {
      "command": "PYTHONPYCACHEPREFIX=/tmp/eclipse-V02-REAL-010-pycache python -m compileall -q app tests.py",
      "purpose": "Run the packet-required compilation of the application package and tests.py while redirecting bytecode outside the repository.",
      "mutating": true,
      "required": true
    },
    {
      "command": "git diff --check -- app/models.py tests.py",
      "purpose": "Reject whitespace errors in the authorized patch.",
      "mutating": false,
      "required": true
    },
    {
      "command": "git diff --name-only",
      "purpose": "Prove that tracked modifications are confined to the two authorized files and exclude migrations.",
      "mutating": false,
      "required": true
    },
    {
      "command": "git status --short",
      "purpose": "Prove that no generated, untracked, migration, or other repository artifacts were created during implementation and validation.",
      "mutating": false,
      "required": true
    }
  ],
  "expected_evidence": [
    "Base revision, current plan revision/digest, clean starting status, and owned-file digest verification.",
    "Exact files_changed list containing only app/models.py and tests.py.",
    "Focused app/models.py diff showing one private helper, unchanged query construction, unchanged public signatures, and the three corresponding relationship delegations.",
    "Focused tests.py diff showing retained test_follow coverage and exactly one new deterministic test_posts_count method with zero and one assertions.",
    "Command, exit status, and concise output for every required validation command, including commands that succeed silently.",
    "Criterion-by-criterion evidence mapped to AC-01 through AC-04, with deviations, blockers, and unrelated environment failures stated explicitly."
  ],
  "stop_conditions": [
    "HEAD is not a975ef64864354867c88e0ed3a17ba7d17dca752, plan revision 1 is no longer current, or either owned-file digest differs from the context manifest.",
    "The checkout has pre-existing changes overlapping app/models.py or tests.py and the host cannot provide an isolated clean worktree.",
    "Satisfying the requirement appears to require any repository write outside app/models.py and tests.py, especially migrations or dependency/configuration files.",
    "The helper cannot preserve the exact relationship.select().subquery(), select(count()), and db.session.scalar flow for all three relationships.",
    "Any public method signature, relationship mapping, return-value policy, query row set, API contract, database schema, or migration would need to change.",
    "The focused posts_count test cannot use the existing application/database fixture and Post model without changing unrelated setup or adding a dependency.",
    "A required validation command fails for an environment or unrelated reason; report the blocker rather than installing dependencies, using the network, deleting files, or widening scope.",
    "Bytecode cannot be redirected to the authorized /tmp prefix and validation would create repository files outside write_globs.",
    "Credentials, external effects, destructive actions, expanded permissions, or verified model/cost guarantees are requested.",
    "An architecture, interface, query-semantics, test-design, scope, migration, or concurrency decision must change; return to the architect for a new plan revision."
  ],
  "risk": {
    "level": "low",
    "flags": [
      "three public ORM-backed methods share a new internal dependency",
      "relationship-specific query semantics and scalar return behavior must remain exact",
      "production and regression-test files require exclusive ownership",
      "Python validation generates bytecode in an authorized temporary prefix"
    ]
  },
  "complexity": "bounded",
  "budgets": {
    "max_attempts": 2,
    "max_review_rounds": 1
  },
  "authorization": {
    "network": false,
    "credentials": false,
    "external_side_effects": false,
    "destructive_actions": false,
    "targets": [
      "app/models.py",
      "tests.py",
      "/tmp/eclipse-V02-REAL-010-pycache/**"
    ]
  },
  "provenance": {
    "base_revision": "a975ef64864354867c88e0ed3a17ba7d17dca752",
    "created_by": "eclipse-architect",
    "created_at": "2026-08-13T04:20:04Z",
    "source_requirement_digest": "sha256:c0050986b4477cc2b82404dfaeea57d47aed9cf45b8d269d49f08f98de81f904"
  },
  "metadata": {
    "case_id": "V02-REAL-010",
    "adapter": "manual",
    "policy": "sol-luna-v0.1",
    "routing_status": "policy-only; requested/configured model identity, effective route, permissions, and cost are unverified",
    "execution_wave": 1,
    "integration_order": 1,
    "concurrency_decision": "Single task in wave 1; no concurrent writer is authorized.",
    "plan_digest_algorithm": "SHA-256 over the exact UTF-8 bytes of metadata.plan_digest_input, with no trailing newline.",
    "plan_digest_input": "{\"base_revision\":\"a975ef64864354867c88e0ed3a17ba7d17dca752\",\"fixed_decisions\":[\"introduce one private User._count_relationship helper that performs the existing select(count()).select_from(relationship.select().subquery()) construction and returns db.session.scalar(query)\",\"keep followers_count, following_count, and posts_count public names and make each delegate to the helper with self.followers, self.following, and self.posts respectively\",\"retain the existing follow-count coverage and add one focused posts_count unittest covering zero and one without changing migrations or unrelated behavior\"],\"plan_revision\":1,\"run_id\":\"V02-REAL-010\",\"task_ids\":[\"V02-REAL-010-T01\"],\"waves\":[[\"V02-REAL-010-T01\"]]}"
  }
}
```

