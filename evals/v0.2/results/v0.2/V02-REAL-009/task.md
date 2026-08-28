```json
{
  "schema_version": "1.0",
  "run_id": "V02-REAL-009",
  "plan_revision": 1,
  "plan_digest": "sha256:5da16237c46b7b633dd9c9de34a5cff7eb5be28f65a0300054e559bb3d96e957",
  "task_id": "V02-REAL-009-T1",
  "dependencies": [],
  "objective": "Make User.to_dict serialize a None last_seen as null while preserving the exact existing timezone-aware ISO string path for non-None values, with focused regression coverage.",
  "rationale": "The mapped attribute is explicitly optional, but the serializer dereferences it unconditionally; a narrow conditional fixes the crash without changing persistence or timestamp semantics.",
  "context_manifest": {
    "schema_version": "1.0",
    "summary": "User.last_seen is Optional[datetime]. User.to_dict currently calls self.last_seen.replace(tzinfo=timezone.utc).isoformat() unconditionally. UserModelCase provides an app context and transient SQLite database for focused model tests.",
    "references": [
      {
        "path": "app/models.py",
        "symbol": "User.to_dict and User.last_seen",
        "purpose": "Guard the nullable serialization expression without changing the model mapping.",
        "digest": null,
        "trust": "repository"
      },
      {
        "path": "tests.py",
        "symbol": "UserModelCase",
        "purpose": "Add focused None and non-None last_seen serialization coverage.",
        "digest": null,
        "trust": "repository"
      }
    ],
    "trusted_sources": [
      "/workspace/scratch/473866e9940e/repo/evals/v0.2/results/v0.2/V02-REAL-009/packet.json",
      "/workspace/scratch/473866e9940e/repo/evals/v0.2/results/v0.2/V02-REAL-009/host-metadata.json"
    ]
  },
  "decisions": {
    "fixed": [
      "When self.last_seen is None, data['last_seen'] is Python None so Flask JSON renders null.",
      "When non-None, retain exactly self.last_seen.replace(tzinfo=timezone.utc).isoformat().",
      "Do not change the mapped column, default, or persistence semantics."
    ],
    "assumptions": [
      "Existing behavior intentionally assigns UTC with replace rather than converting with astimezone; preservation forbids changing that detail.",
      "The trusted clean base remains current at task start."
    ]
  },
  "invariants": [
    "All User.to_dict fields other than null handling for last_seen remain unchanged.",
    "Non-None last_seen output remains byte-for-byte the same string as the pinned implementation.",
    "No schema or migration changes occur."
  ],
  "non_goals": [
    "Changing timezone conversion semantics.",
    "Changing the last_seen default or nullability.",
    "Changing API endpoints, templates, or dependencies."
  ],
  "scope": {
    "write_globs": [
      "app/models.py",
      "tests.py"
    ],
    "read_globs": [
      "app/models.py",
      "tests.py"
    ],
    "forbidden_globs": [
      "migrations/**",
      "app/api/**",
      "app/templates/**",
      "config.py",
      "requirements*.txt"
    ],
    "shared_interfaces": [
      "User.to_dict last_seen representation"
    ],
    "exclusive_resources": [
      "app/models.py:User.to_dict last_seen field",
      "tests.py:last_seen serialization tests"
    ],
    "parallel_safe": false,
    "isolation": "manual"
  },
  "required_capabilities": [
    "bounded Python bug fix",
    "SQLAlchemy nullable-field reasoning",
    "unittest regression editing",
    "Python compile validation"
  ],
  "execution_profile": {
    "role": "worker",
    "capability_tier": "bounded-local-implementation",
    "cost_tier": "low",
    "reasoning_effort": "high",
    "preferred_model": null,
    "fallback_profiles": [
      "Return any timestamp normalization or schema decision to the architect."
    ]
  },
  "implementation_instructions": [
    "Make only the last_seen value in User.to_dict conditional: None when the attribute is None, otherwise the existing replace-and-isoformat expression.",
    "Add a focused model test that persists or otherwise prepares a valid User, sets last_seen to None, and asserts the serialized value is None.",
    "In the same focused coverage, set a known non-None datetime and assert the exact existing UTC ISO string.",
    "Do not change the model field declaration, database setup, or unrelated representation fields."
  ],
  "acceptance_criteria": [
    {
      "id": "AC1",
      "statement": "User.to_dict returns None for the last_seen field when User.last_seen is None.",
      "evidence_required": "Focused regression test source and serializer diff showing the explicit None branch."
    },
    {
      "id": "AC2",
      "statement": "A non-None last_seen retains the existing timezone-aware ISO formatting.",
      "evidence_required": "Focused exact-string assertion and diff showing the original replace(tzinfo=timezone.utc).isoformat() expression retained."
    },
    {
      "id": "AC3",
      "statement": "Modified Python files compile and no unauthorized files change.",
      "evidence_required": "Required frozen command exit status 0, concise output, and task-local final diff/status."
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
    "Task-local patch limited to app/models.py and tests.py.",
    "Required command, exit status, and concise output.",
    "Focused test source proving both nullable branches.",
    "Final status excluding compile-generated bytecode and __pycache__ directories from the product patch.",
    "Result evidence at the host-provided external artifact destination."
  ],
  "stop_conditions": [
    "The fix appears to require a database mapping, migration, timezone semantic, endpoint, template, dependency, or out-of-scope change.",
    "The frozen compile command cannot run without installation, network, credentials, or expanded permission.",
    "The trusted base revision or clean status no longer matches.",
    "Focused coverage exposes a separate User.to_dict defect not required for the nullable last_seen fix."
  ],
  "risk": {
    "level": "low",
    "flags": [
      "API null representation",
      "nullable model field",
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
