```json
{
  "schema_version": "1.0",
  "run_id": "V02-REAL-001",
  "plan_revision": 1,
  "plan_digest": "sha256:4e30854d8be881c4d5f005a2cf1a7edea464bd4029ce25145f9b8e9ebb365445",
  "task_id": "V02-REAL-001-T1",
  "dependencies": [],
  "objective": "Make int_to_bytes reject negative integers with exactly ValueError('num must be non-negative') before struct packing, and add focused regression coverage without changing non-negative behavior.",
  "rationale": "An explicit domain check gives callers the required stable error while leaving the existing unsigned-64-bit serialization path intact.",
  "context_manifest": {
    "schema_version": "1.0",
    "summary": "The current int_to_bytes directly calls the unsigned >Q packer and strips leading zero bytes. Existing focused tests already cover 0, 192, and maximum uint64 round trips.",
    "references": [
      {
        "path": "src/itsdangerous/encoding.py",
        "symbol": "int_to_bytes",
        "purpose": "Add the negative-input guard while preserving the existing packing path.",
        "digest": null,
        "trust": "repository"
      },
      {
        "path": "tests/test_itsdangerous/test_encoding.py",
        "symbol": "test_int_bytes",
        "purpose": "Add focused negative-input coverage and retain boundary behavior coverage.",
        "digest": null,
        "trust": "repository"
      }
    ],
    "trusted_sources": [
      "/workspace/scratch/473866e9940e/repo/evals/v0.2/results/v0.2/V02-REAL-001/packet.json",
      "/workspace/scratch/473866e9940e/repo/evals/v0.2/results/v0.2/V02-REAL-001/host-metadata.json"
    ]
  },
  "decisions": {
    "fixed": [
      "Raise exactly ValueError('num must be non-negative') for num < 0 before invoking _int_to_bytes.",
      "Keep the existing pack-and-lstrip behavior unchanged for all non-negative inputs.",
      "Do not change public exports or dependencies."
    ],
    "assumptions": [
      "The pinned checkout and clean pre-task status reported by the trusted host remain current when the task starts."
    ]
  },
  "invariants": [
    "int_to_bytes(0) remains b''.",
    "int_to_bytes(18446744073709551615) remains b'\\xff' * 8.",
    "Existing non-negative input behavior and bytes_to_int behavior remain unchanged."
  ],
  "non_goals": [
    "Changing behavior for values above uint64 range.",
    "Changing exception behavior elsewhere in the encoding module.",
    "Changing public exports, dependencies, or documentation."
  ],
  "scope": {
    "write_globs": [
      "src/itsdangerous/encoding.py",
      "tests/test_itsdangerous/test_encoding.py"
    ],
    "read_globs": [
      "src/itsdangerous/encoding.py",
      "tests/test_itsdangerous/test_encoding.py"
    ],
    "forbidden_globs": [
      "src/itsdangerous/__init__.py",
      "pyproject.toml",
      "requirements*.txt",
      "docs/**"
    ],
    "shared_interfaces": [
      "itsdangerous.encoding.int_to_bytes behavior"
    ],
    "exclusive_resources": [
      "src/itsdangerous/encoding.py:int_to_bytes",
      "tests/test_itsdangerous/test_encoding.py:int-byte tests"
    ],
    "parallel_safe": false,
    "isolation": "manual"
  },
  "required_capabilities": [
    "bounded Python implementation",
    "pytest regression testing"
  ],
  "execution_profile": {
    "role": "worker",
    "capability_tier": "bounded-local-implementation",
    "cost_tier": "low",
    "reasoning_effort": "high",
    "preferred_model": null,
    "fallback_profiles": [
      "Return local implementation ambiguity to the architect; do not increase authority or scope."
    ]
  },
  "implementation_instructions": [
    "Add an explicit num < 0 guard as the first operation in int_to_bytes and raise ValueError with the exact required message.",
    "Leave the existing _int_to_bytes(num).lstrip(b'\\x00') expression as the non-negative path.",
    "Add a focused pytest assertion that int_to_bytes(-1) raises ValueError with an exact message match.",
    "Do not modify the existing zero and maximum uint64 assertions except for a minimal test organization change if necessary."
  ],
  "acceptance_criteria": [
    {
      "id": "AC1",
      "statement": "int_to_bytes(-1) raises ValueError('num must be non-negative') before struct packing.",
      "evidence_required": "Passing focused pytest assertion with exact exception type and message, plus the relevant source diff."
    },
    {
      "id": "AC2",
      "statement": "Zero and maximum uint64 serialization remain unchanged.",
      "evidence_required": "Passing existing test_int_bytes cases for 0 and 18446744073709551615."
    },
    {
      "id": "AC3",
      "statement": "The focused encoding test module passes with no unauthorized product changes.",
      "evidence_required": "Exit status 0 and concise output from the required validation command, together with a task-local final diff/status."
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
    "Task-local patch limited to the two authorized files.",
    "Required command, exit status, and concise output showing the focused tests pass.",
    "Final git status identifying any pytest cache or bytecode as validation output and excluding it from the product patch.",
    "Result evidence written to the host-provided destination outside the product checkout."
  ],
  "stop_conditions": [
    "The required change needs a public export, dependency, generated-file, or out-of-scope modification.",
    "The exact frozen validation command cannot run in the existing environment without installation, network, credentials, or permission expansion.",
    "The pinned base revision or clean pre-task status does not match host metadata.",
    "Tests expose an architecture or behavior decision beyond the fixed decisions in this contract."
  ],
  "risk": {
    "level": "low",
    "flags": [
      "public helper behavior change",
      "validation may create local caches or bytecode"
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
      "tests/test_itsdangerous/test_encoding.py"
    ]
  },
  "provenance": {
    "base_revision": "672971d66a2ef9f85151e53283113f33d642dabd",
    "created_by": "eclipse-architect",
    "created_at": "2026-08-13T00:00:00+08:00"
  }
}
```
