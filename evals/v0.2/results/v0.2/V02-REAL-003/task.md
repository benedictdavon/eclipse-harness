```json
{
  "schema_version": "1.0",
  "run_id": "V02-REAL-003",
  "plan_revision": 1,
  "plan_digest": "sha256:0d72877b8a29508b6703311d151e29be603ea9d0cfc731b71124fcfcf8f04118",
  "task_id": "V02-REAL-003-T1",
  "dependencies": [],
  "objective": "Make base64_decode translate non-ASCII str input into BadData instead of silently dropping characters, while preserving valid str and bytes URL-safe decoding.",
  "rationale": "The current errors='ignore' ASCII conversion mutates text before decoding; strict conversion within the existing error boundary prevents silent data alteration and preserves the public bad-data abstraction.",
  "context_manifest": {
    "schema_version": "1.0",
    "summary": "base64_decode currently performs ASCII conversion with errors='ignore' before its try/except, pads to a multiple of four, and translates decoder TypeError/ValueError to BadData. want_bytes leaves bytes unchanged.",
    "references": [
      {
        "path": "src/itsdangerous/encoding.py",
        "symbol": "base64_decode",
        "purpose": "Replace lossy text conversion with strict conversion inside BadData translation.",
        "digest": null,
        "trust": "repository"
      },
      {
        "path": "src/itsdangerous/encoding.py",
        "symbol": "want_bytes",
        "purpose": "Confirm strict encoding semantics and unchanged bytes passthrough.",
        "digest": null,
        "trust": "repository"
      },
      {
        "path": "tests/test_itsdangerous/test_encoding.py",
        "symbol": "test_base64_bad",
        "purpose": "Add the non-ASCII str regression beside focused base64 tests.",
        "digest": null,
        "trust": "repository"
      }
    ],
    "trusted_sources": [
      "/workspace/scratch/473866e9940e/repo/evals/v0.2/results/v0.2/V02-REAL-003/packet.json",
      "/workspace/scratch/473866e9940e/repo/evals/v0.2/results/v0.2/V02-REAL-003/host-metadata.json"
    ]
  },
  "decisions": {
    "fixed": [
      "Use strict ASCII conversion for str input; do not ignore or replace non-ASCII characters.",
      "Place text conversion inside the error translation boundary so encoding failure raises BadData('Invalid base64-encoded data') from the original error.",
      "Preserve bytes passthrough, padding, and valid URL-safe decoding behavior."
    ],
    "assumptions": [
      "The existing BadData message remains appropriate because the packet requires the exception type but does not request new message text.",
      "The trusted clean base state remains current at task start."
    ]
  },
  "invariants": [
    "base64_decode continues to return bytes for valid URL-safe str and bytes inputs.",
    "base64_encode and want_bytes public behavior remain unchanged.",
    "Decoder and text-conversion failures exposed by this path use BadData rather than raw ValueError subclasses."
  ],
  "non_goals": [
    "Tightening validation of arbitrary ASCII bytes beyond existing decoder behavior.",
    "Changing BadData class hierarchy or public exports.",
    "Changing dependencies or documentation."
  ],
  "scope": {
    "write_globs": [
      "src/itsdangerous/encoding.py",
      "tests/test_itsdangerous/test_encoding.py"
    ],
    "read_globs": [
      "src/itsdangerous/encoding.py",
      "src/itsdangerous/exc.py",
      "tests/test_itsdangerous/test_encoding.py"
    ],
    "forbidden_globs": [
      "src/itsdangerous/exc.py",
      "src/itsdangerous/__init__.py",
      "pyproject.toml",
      "docs/**"
    ],
    "shared_interfaces": [
      "itsdangerous.encoding.base64_decode behavior",
      "itsdangerous.exc.BadData boundary"
    ],
    "exclusive_resources": [
      "src/itsdangerous/encoding.py:base64_decode",
      "tests/test_itsdangerous/test_encoding.py:base64 tests"
    ],
    "parallel_safe": false,
    "isolation": "manual"
  },
  "required_capabilities": [
    "Python exception-boundary reasoning",
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
      "Return any broader byte-validation or public error-contract decision to the architect."
    ]
  },
  "implementation_instructions": [
    "Change base64_decode to perform want_bytes(string, encoding='ascii') with strict error handling inside the existing try/except boundary.",
    "Retain current padding and urlsafe_b64decode operations and translate conversion/decoder TypeError or ValueError to the existing BadData message with exception chaining.",
    "Add a focused test proving a non-ASCII str raises BadData.",
    "Retain or minimally extend valid str and bytes decoding coverage; do not redefine handling of invalid ASCII bytes."
  ],
  "acceptance_criteria": [
    {
      "id": "AC1",
      "statement": "A non-ASCII str passed to base64_decode raises BadData and is not silently altered.",
      "evidence_required": "Passing regression test using a non-ASCII str, plus the relevant source diff showing strict conversion and translation."
    },
    {
      "id": "AC2",
      "statement": "Valid URL-safe str and bytes inputs continue to decode to the same bytes.",
      "evidence_required": "Passing focused assertions covering both accepted input forms."
    },
    {
      "id": "AC3",
      "statement": "The frozen focused encoding suite passes with changes limited to authorized files.",
      "evidence_required": "Required command exit status 0, concise output, and task-local final diff/status."
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
    "Task-local patch limited to encoding.py and its focused test module.",
    "Required command, exit status, and concise passing output.",
    "Final status that identifies validation-generated caches or bytecode and excludes them from the product patch.",
    "Result evidence at the host-provided external artifact destination."
  ],
  "stop_conditions": [
    "The fix requires changing BadData, public exports, dependencies, or byte-input semantics beyond preserving current behavior.",
    "The frozen validation command cannot run without installation, network, credentials, or expanded permissions.",
    "The base revision or clean status differs from trusted host metadata.",
    "A required write falls outside the two authorized files."
  ],
  "risk": {
    "level": "low",
    "flags": [
      "public decode error behavior",
      "exception translation",
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
