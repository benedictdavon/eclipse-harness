```json
{
  "schema_version": "1.0",
  "run_id": "V02-REAL-002",
  "plan_revision": 1,
  "plan_digest": "sha256:69e90b0639959b8be3bf2b74d33222cd7e7b3cc96f9062eea90dbea05a0e7dbd",
  "task_id": "V02-REAL-002-T1",
  "dependencies": [],
  "objective": "Enforce and document that bytes_to_int accepts at most eight bytes, with the exact required ValueError for a nine-byte input and unchanged results for valid inputs.",
  "rationale": "An explicit guard makes the public input limit stable and understandable instead of relying on the struct unpacker's incidental failure.",
  "context_manifest": {
    "schema_version": "1.0",
    "summary": "bytes_to_int currently right-pads to eight bytes and directly calls the >Q unpacker. Existing focused tests round-trip zero, 192, and maximum uint64. The encoding documentation currently lists only base64 helpers.",
    "references": [
      {
        "path": "src/itsdangerous/encoding.py",
        "symbol": "bytes_to_int",
        "purpose": "Add the explicit maximum-length guard while preserving the valid-input path.",
        "digest": null,
        "trust": "repository"
      },
      {
        "path": "tests/test_itsdangerous/test_encoding.py",
        "symbol": "test_int_bytes",
        "purpose": "Add the nine-byte regression and retain valid round-trip coverage.",
        "digest": null,
        "trust": "repository"
      },
      {
        "path": "docs/encoding.rst",
        "symbol": null,
        "purpose": "Document the eight-byte bytes_to_int input limit in one concise sentence.",
        "digest": null,
        "trust": "repository"
      }
    ],
    "trusted_sources": [
      "/workspace/scratch/473866e9940e/repo/evals/v0.2/results/v0.2/V02-REAL-002/packet.json",
      "/workspace/scratch/473866e9940e/repo/evals/v0.2/results/v0.2/V02-REAL-002/host-metadata.json"
    ]
  },
  "decisions": {
    "fixed": [
      "For len(bytestr) > 8, raise exactly ValueError('bytestr must contain at most 8 bytes') before rjust or unpacking.",
      "Keep the bytes_to_int public name and its existing result for inputs of at most eight bytes.",
      "Add exactly one concise documentation sentence stating the limit."
    ],
    "assumptions": [
      "The pinned checkout and clean pre-task status reported by the trusted host remain current when execution starts."
    ]
  },
  "invariants": [
    "Zero-length through eight-byte inputs continue through the existing rjust(8, b'\\x00') and unsigned unpack path.",
    "Existing int_to_bytes and valid bytes_to_int round trips remain unchanged.",
    "No public names or imports change."
  ],
  "non_goals": [
    "Changing accepted input types.",
    "Changing int_to_bytes behavior.",
    "Adding dependencies or broad encoding documentation."
  ],
  "scope": {
    "write_globs": [
      "src/itsdangerous/encoding.py",
      "tests/test_itsdangerous/test_encoding.py",
      "docs/encoding.rst"
    ],
    "read_globs": [
      "src/itsdangerous/encoding.py",
      "tests/test_itsdangerous/test_encoding.py",
      "docs/encoding.rst"
    ],
    "forbidden_globs": [
      "src/itsdangerous/__init__.py",
      "pyproject.toml",
      "requirements*.txt",
      "docs/**/index.rst"
    ],
    "shared_interfaces": [
      "itsdangerous.encoding.bytes_to_int behavior",
      "encoding utility documentation"
    ],
    "exclusive_resources": [
      "src/itsdangerous/encoding.py:bytes_to_int",
      "tests/test_itsdangerous/test_encoding.py:int-byte tests",
      "docs/encoding.rst"
    ],
    "parallel_safe": false,
    "isolation": "manual"
  },
  "required_capabilities": [
    "bounded Python implementation",
    "pytest regression testing",
    "concise reStructuredText editing"
  ],
  "execution_profile": {
    "role": "worker",
    "capability_tier": "bounded-local-implementation",
    "cost_tier": "low",
    "reasoning_effort": "high",
    "preferred_model": null,
    "fallback_profiles": [
      "Return any public API or documentation-scope ambiguity to the architect."
    ]
  },
  "implementation_instructions": [
    "Add an explicit len(bytestr) > 8 guard as the first operation in bytes_to_int and raise the exact required ValueError.",
    "Leave the existing rjust and _bytes_to_int expression as the valid-input path.",
    "Add a focused test that passes nine bytes and matches the exact exception message; retain existing valid round-trip cases.",
    "Add one concise sentence to docs/encoding.rst stating that bytes_to_int accepts at most eight bytes."
  ],
  "acceptance_criteria": [
    {
      "id": "AC1",
      "statement": "A nine-byte input raises ValueError('bytestr must contain at most 8 bytes').",
      "evidence_required": "Passing focused pytest assertion matching the exact exception type and message, plus the relevant source diff."
    },
    {
      "id": "AC2",
      "statement": "Inputs of at most eight bytes preserve their existing outputs and round-trip behavior.",
      "evidence_required": "Passing existing focused valid-input test cases including zero and maximum uint64."
    },
    {
      "id": "AC3",
      "statement": "docs/encoding.rst states the at-most-eight-byte limit in one concise sentence.",
      "evidence_required": "Task-local documentation diff showing the sentence."
    },
    {
      "id": "AC4",
      "statement": "The frozen focused encoding test command passes and no unauthorized files are changed.",
      "evidence_required": "Command exit status 0 with concise output and task-local final diff/status."
    }
  ],
  "validation": [
    {
      "command": "PYTHONPATH=src python -m pytest tests/test_itsdangerous/test_encoding.py -q",
      "purpose": "Run the frozen focused encoding regression suite.",
      "mutating": true,
      "required": true
    }
  ],
  "expected_evidence": [
    "Task-local patch limited to the three authorized files.",
    "Required command, exit status, and concise passing output.",
    "Final git status separating pytest cache or bytecode from the product patch.",
    "Result evidence written to the host-provided destination outside the checkout."
  ],
  "stop_conditions": [
    "The change requires renaming the public function, changing dependencies, or changing valid-input behavior.",
    "The exact frozen validation command cannot run without installation, network, credentials, or permission expansion.",
    "The pinned base or clean pre-task status differs from trusted host metadata.",
    "An out-of-scope file would need modification."
  ],
  "risk": {
    "level": "low",
    "flags": [
      "public helper input validation change",
      "documentation consistency",
      "validation may create caches or bytecode"
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
      "src/itsdangerous/encoding.py",
      "tests/test_itsdangerous/test_encoding.py",
      "docs/encoding.rst"
    ]
  },
  "provenance": {
    "base_revision": "672971d66a2ef9f85151e53283113f33d642dabd",
    "created_by": "eclipse-architect",
    "created_at": "2026-08-13T00:00:00+08:00"
  }
}
```
