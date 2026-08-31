```json
{
  "schema_version": "1.0",
  "run_id": "V02-REAL-007",
  "plan_revision": 1,
  "plan_digest": "sha256:5d2e76d82ce27458941cb200f46e59df6b78ee5a2a5ed4dcee5cf5a755375926",
  "task_id": "V02-REAL-007-T1",
  "dependencies": [],
  "objective": "Make User.avatar reject size 0 and -1 with exactly ValueError('size must be positive'), retain the existing URL for positive sizes, and add focused unittest coverage.",
  "rationale": "An early domain guard prevents invalid Gravatar size URLs while preserving the established digest and URL format for valid callers.",
  "context_manifest": {
    "schema_version": "1.0",
    "summary": "User.avatar currently hashes the lowercase email and interpolates any size into a fixed Gravatar URL. tests.py already asserts the exact URL for size 128 in UserModelCase.test_avatar.",
    "references": [
      {
        "path": "app/models.py",
        "symbol": "User.avatar",
        "purpose": "Add the non-positive size guard before existing URL construction.",
        "digest": null,
        "trust": "repository"
      },
      {
        "path": "tests.py",
        "symbol": "UserModelCase.test_avatar",
        "purpose": "Add focused zero and negative-one error coverage while retaining the 128 URL assertion.",
        "digest": null,
        "trust": "repository"
      }
    ],
    "trusted_sources": [
      "/workspace/scratch/473866e9940e/repo/evals/v0.2/results/v0.2/V02-REAL-007/packet.json",
      "/workspace/scratch/473866e9940e/repo/evals/v0.2/results/v0.2/V02-REAL-007/host-metadata.json"
    ]
  },
  "decisions": {
    "fixed": [
      "For size <= 0, raise exactly ValueError('size must be positive') before computing the digest.",
      "For every positive size, retain the existing lowercase-email MD5 digest and exact URL formatting.",
      "Cover both 0 and -1 using unittest assertions and preserve the size-128 assertion."
    ],
    "assumptions": [
      "The size argument remains otherwise untyped; this task does not define new behavior for non-numeric values.",
      "The trusted clean base remains current at task start."
    ]
  },
  "invariants": [
    "User.avatar(128) for john@example.com returns the exact currently asserted URL.",
    "No database model fields, mappings, relationships, or migrations change.",
    "No template or route behavior changes."
  ],
  "non_goals": [
    "Validating an upper size bound or non-integer types.",
    "Changing email normalization, hashing, or Gravatar parameters.",
    "Changing templates, database models, migrations, or dependencies."
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
      "app/templates/**",
      "migrations/**",
      "config.py",
      "requirements*.txt",
      "pyproject.toml"
    ],
    "shared_interfaces": [
      "app.models.User.avatar behavior"
    ],
    "exclusive_resources": [
      "app/models.py:User.avatar",
      "tests.py:UserModelCase.test_avatar"
    ],
    "parallel_safe": false,
    "isolation": "manual"
  },
  "required_capabilities": [
    "bounded Python implementation",
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
      "Return non-numeric input semantics or model-scope expansion to the architect."
    ]
  },
  "implementation_instructions": [
    "Add a size <= 0 check at the start of User.avatar and raise the exact required ValueError.",
    "Leave the existing digest calculation and URL return expression unchanged after the guard.",
    "In the existing avatar test, assert that size 0 and -1 each raise ValueError with the exact message, and retain the current size-128 URL assertion.",
    "Do not alter mapped columns, relationships, templates, or database setup."
  ],
  "acceptance_criteria": [
    {
      "id": "AC1",
      "statement": "User.avatar(0) and User.avatar(-1) each raise ValueError('size must be positive').",
      "evidence_required": "Focused unittest source assertions with exact message checks and the corresponding avatar guard diff."
    },
    {
      "id": "AC2",
      "statement": "User.avatar(128) retains the exact existing URL.",
      "evidence_required": "The unchanged exact URL assertion in UserModelCase.test_avatar and diff review showing the valid path unchanged."
    },
    {
      "id": "AC3",
      "statement": "The modified Python files compile and no unauthorized file changes are present.",
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
    "Final status identifying __pycache__ or .pyc files as validation output and excluding them from the product patch.",
    "Result evidence at the host-provided external artifact destination."
  ],
  "stop_conditions": [
    "The requested behavior needs a template, database mapping, migration, dependency, or other out-of-scope change.",
    "The frozen compile command cannot run without installation, network, credentials, or permission expansion.",
    "The base revision or clean pre-task status differs from trusted host metadata.",
    "Tests require a new decision for non-numeric or upper-bound size behavior."
  ],
  "risk": {
    "level": "low",
    "flags": [
      "model method input behavior",
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
