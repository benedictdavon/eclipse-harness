# V02-REAL-009 architecture packet

## Disposition

The requirement is executable as one bounded implementation task. Plan revision 1 is approved for dispatch subject to the identity, scope, and environment checks in the contract. No clarification, broader architecture, or new human authority is required, and no production implementation was performed during architecture.

The defect is local: `User.last_seen` is declared nullable, while `User.to_dict` unconditionally calls `.replace(...).isoformat()`. The implementation must add only an explicit `None` branch around the existing non-null formatting expression and one focused regression test covering both branches.

## Plan identity

- Run: `V02-REAL-009`
- Plan revision: `1`
- Plan digest: `sha256:25add2d1b92503525baa241ed3aeb1a4c3186b315ac92dface37d2d7601341c2`
- Base revision: `a975ef64864354867c88e0ed3a17ba7d17dca752`
- Requirement digest: `sha256:4af93e3188d11fb385e35126ec5b90d447cf66a1c858f01719833fb548ce7bc3`

The plan digest is SHA-256 over these exact UTF-8 bytes, with no trailing newline:

```json
{"base_revision":"a975ef64864354867c88e0ed3a17ba7d17dca752","fixed_decisions":["return null for User.to_dict last_seen when the attribute is None","preserve the existing self.last_seen.replace(tzinfo=timezone.utc).isoformat() expression for every non-None value","add one focused unittest method covering both the None and fixed UTC datetime cases without broader production changes"],"plan_revision":1,"run_id":"V02-REAL-009","task_ids":["V02-REAL-009-T01"],"waves":[["V02-REAL-009-T01"]]}
```

Any architecture change requires plan revision 2, a new digest, and supersession of the nonterminal revision-1 contract.

## Frozen decisions

1. When `self.last_seen is None`, the existing `last_seen` response field receives Python `None`, which Flask exposes as JSON `null`.
2. Every non-`None` value continues through the exact existing expression `self.last_seen.replace(tzinfo=timezone.utc).isoformat()`. This task does not introduce datetime conversion or normalization semantics.
3. The fix stays in the existing dictionary entry in `User.to_dict`; the public signature, response shape, model declaration, routes, counts, links, and all other fields are frozen.
4. `tests.py` gains exactly one `UserModelCase.test_to_dict_last_seen` method. It persists a user, explicitly tests `None` under a Flask request context, then tests the fixed UTC value `datetime(2024, 1, 2, 3, 4, 5, tzinfo=timezone.utc)` against `2024-01-02T03:04:05+00:00`.
5. Repository writes are limited to `app/models.py` and `tests.py`. No migration, dependency, configuration, template, API-route, documentation, or new-file change is authorized.
6. Validation bytecode is redirected to the authorized temporary prefix `/tmp/eclipse-V02-REAL-009-pycache`; no repository cache generation or destructive cleanup is authorized.

## Task and execution wave

| Wave | Task | Dependencies | Exclusive ownership | Isolation | Parallel-safe |
|---|---|---|---|---|---|
| 1 | `V02-REAL-009-T01` | none | `User.to_dict` last-seen branch and `UserModelCase` last-seen coverage | host-provided worktree | `false` |

There is one task because production behavior and its regression test are one atomic acceptance unit and the packet gives them the same two-file write scope. Splitting them would add an artificial dependency and incomplete intermediate states. No concurrent writer is authorized. The deterministic checker confirmed the DAG and returned `[["V02-REAL-009-T01"]]`; the host owns dispatch, isolation, workflow state, and integration.

## Validation and evidence gates

The worker must run the focused unittest, the packet-required `compileall` operation, a scoped whitespace check, and repository-wide path/status checks. The `PYTHONPYCACHEPREFIX` assignments retain the required Python module and arguments while moving bytecode writes outside the repository. Each command needs its exact exit status and concise output, including silent successes.

Acceptance requires direct evidence for:

- `None` completing without exception and remaining `None` in the model dictionary;
- the fixed aware UTC value retaining the exact `+00:00` ISO string;
- one focused test method exercising both branches under the existing fixture;
- successful compilation and a final repository status containing only the two authorized files.

A missing command, nonzero required exit, uncovered criterion, extra path, stale base, or contradictory evidence makes the result incomplete or blocked.

## Risk and routing assumptions

Risk is low and complexity is bounded. The main risks are accidental drift in the existing non-null timezone behavior and collateral edits in a large model file. The unchanged expression requirement, exact-string regression assertion, symbol-level exclusive ownership, and exact-file write scope control those risks.

Under `sol-luna-v0.1`, the configured policy preference is `worker-lite`: executor, bounded-routine capability, low cost tier, medium reasoning effort, and preferred model `gpt-5.6-luna`. This is policy-only routing. The manual adapter provides no trusted observation of the effective model, permissions, or cost, so none is claimed as verified. A concrete still-bounded reasoning blocker may use the configured worker fallback; interface, scope, test-design, timezone-policy, or concurrency changes return to the architect.

## Human and host boundaries

No human response is needed before dispatch if the base revision, plan identity, owned-file digests, and clean isolated checkout match. The host owns scheduling, worktree/branch isolation, workflow status, git integration, and final review.

Stop and return evidence instead of improvising if the checkout is stale or overlapping, a required dependency/tool is unavailable, validation cannot keep bytecode outside the repository, an unrelated test failure prevents acceptance, or any solution needs broader files or semantics. Credentials, destructive actions, dependency installation, network access, external effects, expanded permissions, and verified-routing guarantees require new human authority and are not granted by this packet.

## Architect validation evidence

- The task contract passed `eclipse validate --kind task` through the repository-local optional CLI.
- Canonical task-contract digest: `sha256:6b081376238780a6e9ae779b113190c7a1011fb0e873f3e4fb23a4347c111094`.
- The plan digest recomputed from the exact `metadata.plan_digest_input` bytes and matched the declared value.
- `eclipse check-concurrency --max-writers 1` reported a valid DAG and the single wave `[["V02-REAL-009-T01"]]`.
- No implementation edit or application/test validation was performed in the pinned checkout during architecture.

## Complete Task Contract

The same machine-readable contract is provided separately as `task.json`.

```json
{
  "schema_version": "1.0",
  "run_id": "V02-REAL-009",
  "plan_revision": 1,
  "plan_digest": "sha256:25add2d1b92503525baa241ed3aeb1a4c3186b315ac92dface37d2d7601341c2",
  "task_id": "V02-REAL-009-T01",
  "parent_task_id": null,
  "dependencies": [],
  "objective": "Make User.to_dict serialize last_seen as None when the model attribute is None, preserve the current UTC-tagged ISO string for non-None datetimes, and add focused unittest regression coverage.",
  "rationale": "User.to_dict currently calls replace on last_seen unconditionally, so a nullable mapped value raises AttributeError. One explicit None branch around the existing formatting expression fixes the defect without changing schema or API shape; one model test can prove both branches.",
  "context_manifest": {
    "schema_version": "1.0",
    "summary": "At base revision a975ef64864354867c88e0ed3a17ba7d17dca752, app.models.User.last_seen is an Optional[datetime], but User.to_dict unconditionally evaluates self.last_seen.replace(tzinfo=timezone.utc).isoformat(). tests.py uses standard-library unittest with an application context and an in-memory SQLite database. Add a None branch in the existing last_seen dictionary entry and one UserModelCase test that runs under a request context so to_dict can build its URL links; retain the existing non-None expression exactly.",
    "references": [
      {
        "path": "/workspace/scratch/473866e9940e/repo/evals/v0.2/results/baseline/V02-REAL-009/packet.json",
        "symbol": null,
        "purpose": "Authoritative requirement, allowed write scope, acceptance criteria, required compile command, and pinned revision.",
        "digest": "sha256:4af93e3188d11fb385e35126ec5b90d447cf66a1c858f01719833fb548ce7bc3",
        "trust": "harness"
      },
      {
        "path": "/workspace/scratch/473866e9940e/repo/evals/v0.2/prompts/architect.md",
        "symbol": null,
        "purpose": "Frozen architect-role and read-only planning boundary.",
        "digest": "sha256:a8e484e802d361e2236c7b7221ae84c40037fca40815cb6ae695b5897528e931",
        "trust": "harness"
      },
      {
        "path": "/workspace/scratch/473866e9940e/repo/AGENTS.md",
        "symbol": null,
        "purpose": "Applicable Eclipse workflow, role, and validation policy.",
        "digest": "sha256:a366165b64fd24fdb33cf4c95a557605ea0aed337ba97c9e9ed6821e294c6f77",
        "trust": "project-config"
      },
      {
        "path": "/workspace/scratch/473866e9940e/repo/policies/sol-luna.json",
        "symbol": "profiles.worker-lite",
        "purpose": "Configured routing preference for a tiny deterministic implementation task.",
        "digest": "sha256:0748e68bb125b6aa8e3a36893b43966217953d01828c6c84306d6ed8caa7fcbf",
        "trust": "project-config"
      },
      {
        "path": "app/models.py",
        "symbol": "User.last_seen; User.to_dict",
        "purpose": "Nullable mapped attribute and the sole production serialization branch to change.",
        "digest": "sha256:07534ea0df91817dc69aff5fb5c2ae5802a322b30cdc892517edf7955cd56bae",
        "trust": "repository"
      },
      {
        "path": "tests.py",
        "symbol": "TestConfig; UserModelCase",
        "purpose": "Owned standard-library unittest module and existing application/database fixture.",
        "digest": "sha256:15a002635f20396831bd523365f0939220fd958c72c48f1c0d3d05ae221aabcc",
        "trust": "repository"
      },
      {
        "path": "app/__init__.py",
        "symbol": "create_app",
        "purpose": "Read-only application factory context establishing registered API endpoints used by User.to_dict URL generation.",
        "digest": "sha256:95bfeb5b707c28918c5295413149181dcf2bbadf05dbc9b50f3a53bf844d502d",
        "trust": "repository"
      },
      {
        "path": "app/api/users.py",
        "symbol": "get_user; get_followers; get_following",
        "purpose": "Read-only endpoint context for the URL links produced during the focused to_dict test.",
        "digest": "sha256:a6df82d6d859824fcd1d3b1db5082f0712a91a22afa87a3f96e24e98b62a80fc",
        "trust": "repository"
      }
    ],
    "trusted_sources": [
      "/workspace/scratch/473866e9940e/repo/evals/v0.2/results/baseline/V02-REAL-009/packet.json",
      "/workspace/scratch/473866e9940e/repo/evals/v0.2/prompts/architect.md",
      "/workspace/scratch/473866e9940e/repo/AGENTS.md",
      "/workspace/scratch/473866e9940e/repo/policies/sol-luna.json"
    ]
  },
  "decisions": {
    "fixed": [
      "For last_seen is None, assign Python None to data['last_seen']; Flask JSON serialization will expose that value as JSON null.",
      "For every non-None last_seen, preserve the existing self.last_seen.replace(tzinfo=timezone.utc).isoformat() expression and its output semantics exactly.",
      "Implement the two outcomes as a local conditional in the existing last_seen entry of User.to_dict; do not change the method signature or response shape.",
      "Add exactly one focused UserModelCase unittest method that proves both an explicit None value and a fixed timezone-aware UTC datetime value.",
      "Persist the test user before overriding last_seen and invoke to_dict inside self.app.test_request_context() so existing count queries and URL generation execute normally.",
      "Redirect Python bytecode generated by unittest and compileall to /tmp/eclipse-V02-REAL-009-pycache so required validation does not create repository artifacts."
    ],
    "assumptions": [
      "The executor starts from the clean pinned base revision and the referenced app/models.py and tests.py digests still match.",
      "The existing TestConfig, application factory, registered API blueprint, and in-memory SQLite fixture remain sufficient for the focused test.",
      "The host-provided execution environment already contains the pinned dependencies needed by the existing test suite.",
      "Python None is the intended model-layer representation because Flask converts it to JSON null at the API boundary."
    ]
  },
  "invariants": [
    "User.to_dict keeps its current signature, keys, include_email behavior, count queries, links, and all non-last_seen values.",
    "A non-None datetime is still processed by replace(tzinfo=timezone.utc).isoformat() exactly as before; no timezone conversion policy is introduced.",
    "User.last_seen remains nullable with its existing default and no mapped-column, relationship, table, or migration change.",
    "Existing tests and application behavior outside the nullable serialization case remain unchanged.",
    "No network, credentials, dependency installation, external effects, destructive actions, generated repository files, or unrelated formatting changes are authorized."
  ],
  "non_goals": [
    "Changing how non-UTC aware datetimes are converted, normalizing naive datetimes differently, or redesigning timezone storage.",
    "Changing API routes, response keys, database schema, migrations, templates, serializers, or User.from_dict.",
    "Refactoring User.to_dict, model count helpers, test setup, or unrelated tests.",
    "Adding a new test file, framework, fixture library, dependency, configuration, or documentation.",
    "Testing every User.to_dict field or API endpoint beyond the focused last_seen regression."
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
      "app/api/users.py",
      "config.py",
      "requirements.txt"
    ],
    "forbidden_globs": [
      "app/api/**",
      "app/templates/**",
      "migrations/**",
      "config.py",
      "requirements.txt",
      ".git/**"
    ],
    "shared_interfaces": [
      "app.models.User.to_dict(include_email=False)"
    ],
    "exclusive_resources": [
      "app.models.User.to_dict last_seen branch",
      "tests.UserModelCase last_seen serialization coverage"
    ],
    "parallel_safe": false,
    "isolation": "worktree"
  },
  "required_capabilities": [
    "bounded Python implementation",
    "standard-library unittest authoring",
    "Flask request-context test setup",
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
      "architect for any interface, scope, timezone-policy, or test-design decision"
    ]
  },
  "implementation_instructions": [
    "Before editing, verify HEAD is a975ef64864354867c88e0ed3a17ba7d17dca752, plan revision 1 is current, the checkout is clean, and the owned-file digests match the context manifest.",
    "In app/models.py, change only the value expression for the existing 'last_seen' item in User.to_dict: return None when self.last_seen is None, otherwise evaluate the existing self.last_seen.replace(tzinfo=timezone.utc).isoformat() expression unchanged.",
    "Do not change the User.to_dict signature, dictionary shape, remaining values, model declaration, timezone policy, or any other production symbol.",
    "In tests.py, add exactly one focused method named test_to_dict_last_seen to UserModelCase. Create and persist a user with the existing database fixture, then explicitly assign last_seen = None.",
    "Inside self.app.test_request_context(), call to_dict and assert that data['last_seen'] is None. Then assign datetime(2024, 1, 2, 3, 4, 5, tzinfo=timezone.utc), call to_dict again, and assert the exact string '2024-01-02T03:04:05+00:00'.",
    "Preserve all existing tests and imports; datetime and timezone are already imported. Do not add mocks, dependencies, a new test class, or a new file.",
    "Run every required validation command exactly as listed and capture its command, exit status, and concise output. The PYTHONPYCACHEPREFIX assignment is required to keep generated bytecode outside the repository; do not delete validation artifacts because destructive cleanup is not authorized.",
    "Report the exact files changed, a focused diff, criterion-by-criterion evidence, and any blockers or deviations. Do not commit, push, install dependencies, access the network, or claim verified model/cost/permission routing."
  ],
  "acceptance_criteria": [
    {
      "id": "AC-01",
      "statement": "When User.last_seen is None, User.to_dict completes without exception and returns Python None for the last_seen field, which serializes as JSON null at the Flask API boundary.",
      "evidence_required": "The focused diff shows an explicit None branch, and the passing test_to_dict_last_seen method includes assertIsNone on data['last_seen'] after explicitly assigning None."
    },
    {
      "id": "AC-02",
      "statement": "For a non-None timezone-aware UTC datetime, User.to_dict retains the existing timezone-aware ISO formatting and returns exactly 2024-01-02T03:04:05+00:00 for the fixed test value.",
      "evidence_required": "The focused diff retains self.last_seen.replace(tzinfo=timezone.utc).isoformat() on the non-None branch, and the passing focused test asserts the exact expected string."
    },
    {
      "id": "AC-03",
      "statement": "A single focused regression test exercises both the nullable and non-null last_seen serialization branches using the existing unittest fixture and a Flask request context.",
      "evidence_required": "Exit status 0 and concise output from PYTHONPYCACHEPREFIX=/tmp/eclipse-V02-REAL-009-pycache python -m unittest tests.UserModelCase.test_to_dict_last_seen, plus the focused tests.py diff."
    },
    {
      "id": "AC-04",
      "statement": "The application package and tests.py compile successfully, and repository modifications are limited to app/models.py and tests.py.",
      "evidence_required": "Exit status 0 from the required compileall command with bytecode redirected to the authorized temporary prefix, passing diff whitespace evidence, and final git diff/status output listing only the two owned files."
    }
  ],
  "validation": [
    {
      "command": "PYTHONPYCACHEPREFIX=/tmp/eclipse-V02-REAL-009-pycache python -m unittest tests.UserModelCase.test_to_dict_last_seen",
      "purpose": "Run only the focused regression test for both last_seen serialization branches while keeping import bytecode outside the repository.",
      "mutating": true,
      "required": true
    },
    {
      "command": "PYTHONPYCACHEPREFIX=/tmp/eclipse-V02-REAL-009-pycache python -m compileall -q app tests.py",
      "purpose": "Run the packet-required compileall validation with bytecode redirected to the authorized temporary prefix.",
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
      "purpose": "Prove that tracked modifications are confined to the two authorized files.",
      "mutating": false,
      "required": true
    },
    {
      "command": "git status --short",
      "purpose": "Prove that no generated or untracked repository artifacts were created during validation.",
      "mutating": false,
      "required": true
    }
  ],
  "expected_evidence": [
    "Base revision, current plan revision/digest, clean starting status, and owned-file digest verification.",
    "Exact files_changed list containing only app/models.py and tests.py.",
    "Focused app/models.py diff showing only the explicit None conditional around the unchanged non-None formatting expression.",
    "Focused tests.py diff showing exactly one new test method with direct assertions for None and 2024-01-02T03:04:05+00:00.",
    "Command, exit status, and concise output for every required validation command, including commands that succeed silently.",
    "Criterion-by-criterion evidence mapped to AC-01 through AC-04, with deviations, blockers, and observed unrelated failures stated explicitly."
  ],
  "stop_conditions": [
    "HEAD is not a975ef64864354867c88e0ed3a17ba7d17dca752, plan revision 1 is no longer current, or either owned-file digest differs from the context manifest.",
    "The checkout has pre-existing changes overlapping app/models.py or tests.py and the host cannot provide an isolated clean worktree.",
    "Satisfying the requirement appears to require any repository write outside app/models.py and tests.py.",
    "The existing non-None replace(tzinfo=timezone.utc).isoformat() behavior, public response shape, model schema, API routes, or broader timezone policy would need to change.",
    "The focused test cannot use the existing application/database fixture and request context without changing unrelated setup or adding a dependency.",
    "A required validation command fails for an environment or unrelated reason; report the blocker rather than installing dependencies, using the network, deleting files, or widening scope.",
    "Bytecode cannot be redirected to the authorized /tmp prefix and validation would create repository files outside write_globs.",
    "Credentials, external effects, destructive actions, expanded permissions, or verified model/cost guarantees are requested.",
    "An architecture, interface, scope, test-design, or concurrency decision must change; return to the architect for a new plan revision."
  ],
  "risk": {
    "level": "low",
    "flags": [
      "public API serialization behavior for a nullable field",
      "non-None timezone behavior must remain byte-for-byte compatible",
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
      "/tmp/eclipse-V02-REAL-009-pycache/**"
    ]
  },
  "provenance": {
    "base_revision": "a975ef64864354867c88e0ed3a17ba7d17dca752",
    "created_by": "eclipse-architect",
    "created_at": "2026-08-13T04:05:39Z",
    "source_requirement_digest": "sha256:4af93e3188d11fb385e35126ec5b90d447cf66a1c858f01719833fb548ce7bc3"
  },
  "metadata": {
    "case_id": "V02-REAL-009",
    "adapter": "manual",
    "policy": "sol-luna-v0.1",
    "routing_status": "policy-only; requested/configured model identity, effective route, permissions, and cost are unverified",
    "execution_wave": 1,
    "integration_order": 1,
    "concurrency_decision": "Single task in wave 1; no concurrent writer is authorized.",
    "plan_digest_algorithm": "SHA-256 over the exact UTF-8 bytes of metadata.plan_digest_input, with no trailing newline.",
    "plan_digest_input": "{\"base_revision\":\"a975ef64864354867c88e0ed3a17ba7d17dca752\",\"fixed_decisions\":[\"return null for User.to_dict last_seen when the attribute is None\",\"preserve the existing self.last_seen.replace(tzinfo=timezone.utc).isoformat() expression for every non-None value\",\"add one focused unittest method covering both the None and fixed UTC datetime cases without broader production changes\"],\"plan_revision\":1,\"run_id\":\"V02-REAL-009\",\"task_ids\":[\"V02-REAL-009-T01\"],\"waves\":[[\"V02-REAL-009-T01\"]]}"
  }
}
```

