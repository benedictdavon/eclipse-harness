```json
{
  "schema_version": "1.0",
  "run_id": "V02-REAL-008",
  "plan_revision": 1,
  "plan_digest": "sha256:cea7f3f67a16142c8779081ae9ceb75c8551ade22b1d168961e5d482ae98b52a",
  "task_id": "V02-REAL-008-T1",
  "dependencies": [],
  "objective": "Add a computed is_following boolean to authenticated user API representations through explicit viewer injection, while keeping serialization without an authenticated viewer safe and migration-free.",
  "rationale": "Passing the authenticated viewer from API routes keeps authentication concerns out of the model module and allows the same serializer to remain safe in unauthenticated and non-API contexts.",
  "context_manifest": {
    "schema_version": "1.0",
    "summary": "User.to_dict builds direct API representations; PaginatedAPIMixin.to_collection_dict invokes item.to_dict for user lists. Token-protected routes obtain the authenticated User from token_auth.current_user(). create_user is not token-protected. User.is_following already queries the relationship.",
    "references": [
      {
        "path": "app/models.py",
        "symbol": "User.to_dict, User.is_following, PaginatedAPIMixin.to_collection_dict",
        "purpose": "Add optional viewer propagation and the computed response field without schema changes.",
        "digest": null,
        "trust": "repository"
      },
      {
        "path": "app/api/users.py",
        "symbol": "user API routes",
        "purpose": "Pass token_auth.current_user() from authenticated direct and collection response call sites.",
        "digest": null,
        "trust": "repository"
      },
      {
        "path": "tests.py",
        "symbol": "UserModelCase",
        "purpose": "Add focused true, false, and no-viewer serialization coverage.",
        "digest": null,
        "trust": "repository"
      }
    ],
    "trusted_sources": [
      "/workspace/scratch/473866e9940e/repo/evals/v0.2/results/v0.2/V02-REAL-008/packet.json",
      "/workspace/scratch/473866e9940e/repo/evals/v0.2/results/v0.2/V02-REAL-008/host-metadata.json"
    ]
  },
  "decisions": {
    "fixed": [
      "Add an optional viewer=None parameter to User.to_dict and PaginatedAPIMixin.to_collection_dict; pass it explicitly to item.to_dict in collections.",
      "When viewer is not None, set top-level data['is_following'] to viewer.is_following(self); when viewer is None, omit the key.",
      "Pass token_auth.current_user() at every token-authenticated user route response, including direct, update, and paginated endpoints.",
      "Do not import token_auth or Flask-Login current_user in app/models.py and do not add persistent state."
    ],
    "assumptions": [
      "The authenticated token user returned by token_auth.current_user() is a User instance for all login_required user API routes.",
      "Omitting is_following when no viewer exists matches 'when the current authenticated user is available'.",
      "The trusted clean base remains current at task start."
    ]
  },
  "invariants": [
    "Existing user representation keys and include_email behavior remain unchanged.",
    "Pagination links continue to receive only endpoint URL parameters; viewer is consumed as an explicit serializer parameter.",
    "Unauthenticated create-user serialization and direct non-API User.to_dict calls do not query a follower relationship unless a viewer is supplied.",
    "No mapped column, table, relationship, or migration is added."
  ],
  "non_goals": [
    "Persisting is_following or adding a hybrid property.",
    "Optimizing collection follower checks or changing pagination query shape.",
    "Changing authentication requirements, response schemas beyond this field, templates, or database schema."
  ],
  "scope": {
    "write_globs": [
      "app/models.py",
      "app/api/users.py",
      "tests.py"
    ],
    "read_globs": [
      "app/models.py",
      "app/api/users.py",
      "app/api/auth.py",
      "tests.py"
    ],
    "forbidden_globs": [
      "migrations/**",
      "app/templates/**",
      "app/api/auth.py",
      "config.py",
      "requirements*.txt"
    ],
    "shared_interfaces": [
      "User.to_dict optional viewer contract",
      "PaginatedAPIMixin.to_collection_dict optional viewer contract",
      "user API representation"
    ],
    "exclusive_resources": [
      "app/models.py:user API serialization",
      "app/api/users.py:user response call sites",
      "tests.py:user serialization tests"
    ],
    "parallel_safe": false,
    "isolation": "manual"
  },
  "required_capabilities": [
    "Flask token-auth context reasoning",
    "SQLAlchemy relationship behavior",
    "bounded Python multi-file implementation",
    "unittest regression editing"
  ],
  "execution_profile": {
    "role": "worker",
    "capability_tier": "bounded-local-implementation",
    "cost_tier": "low",
    "reasoning_effort": "high",
    "preferred_model": null,
    "fallback_profiles": [
      "Return API field-presence, query-shape, or auth-boundary ambiguity to the architect."
    ]
  },
  "implementation_instructions": [
    "Add viewer=None explicitly before **kwargs in PaginatedAPIMixin.to_collection_dict and call item.to_dict(viewer=viewer) for each resource.",
    "Add viewer=None to User.to_dict; after building existing data, add is_following only when viewer is not None, using viewer.is_following(self).",
    "In token-protected get_user, get_users, get_followers, get_following, and update_user responses, pass token_auth.current_user() to direct or collection serialization.",
    "Leave create_user without a viewer so its anonymous response remains safe and omits is_following.",
    "Add focused tests using persisted users to show true after follow, false without follow, and safe key omission from to_dict() with no viewer.",
    "Do not add model fields, migrations, auth imports in models.py, or template changes."
  ],
  "acceptance_criteria": [
    {
      "id": "AC1",
      "statement": "With an authenticated viewer, serialized users contain is_following true or false according to viewer.is_following(target).",
      "evidence_required": "Focused test source covering both relationship states and diffs showing viewer propagation from authenticated API routes."
    },
    {
      "id": "AC2",
      "statement": "Serialization without a viewer does not crash and omits is_following.",
      "evidence_required": "Focused no-viewer test assertion and serializer diff showing the explicit None guard."
    },
    {
      "id": "AC3",
      "statement": "No database column, relationship, table, or migration is added.",
      "evidence_required": "Task-local diff/status limited to the three authorized Python files and review of model changes as response-only logic."
    },
    {
      "id": "AC4",
      "statement": "All modified Python files compile.",
      "evidence_required": "Required frozen command exit status 0 and concise output."
    }
  ],
  "validation": [
    {
      "command": "python -m compileall -q app tests.py",
      "purpose": "Run the packet's exact frozen Python compilation validation.",
      "mutating": true,
      "required": true
    }
  ],
  "expected_evidence": [
    "Task-local patch limited to app/models.py, app/api/users.py, and tests.py.",
    "Required command, exit status, and concise output.",
    "Focused test source demonstrating true, false, and absent-without-viewer behavior.",
    "Final status excluding compile-generated __pycache__ and .pyc files from the product patch.",
    "Result evidence at the host-provided external artifact destination."
  ],
  "stop_conditions": [
    "A database/migration, template, authentication-policy, or out-of-scope change becomes necessary.",
    "The design would require importing API authentication state into app/models.py.",
    "The frozen compile command cannot run without installation, network, credentials, or expanded permission.",
    "The trusted base revision or clean status no longer matches."
  ],
  "risk": {
    "level": "medium",
    "flags": [
      "API representation change",
      "serializer call-signature propagation",
      "per-item relationship query",
      "validation creates bytecode"
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
      "app/models.py",
      "app/api/users.py",
      "tests.py"
    ]
  },
  "provenance": {
    "base_revision": "a975ef64864354867c88e0ed3a17ba7d17dca752",
    "created_by": "eclipse-architect",
    "created_at": "2026-08-13T00:00:00+08:00"
  }
}
```
