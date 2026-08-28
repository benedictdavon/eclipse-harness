```json
{
  "schema_version": "1.0",
  "run_id": "V02-REAL-004",
  "plan_revision": 1,
  "plan_digest": "sha256:7510b56e4cabf0a91b31715ba7f9530b2b0462068c533cf6afdc01a1133d94d5",
  "task_id": "V02-REAL-004-T1",
  "dependencies": [],
  "objective": "Refactor base64_decode to delegate its existing Base64 padding calculation to a private helper without changing any public behavior or tests.",
  "rationale": "A narrow extraction centralizes the padding calculation while avoiding public API or decoding-semantic changes.",
  "context_manifest": {
    "schema_version": "1.0",
    "summary": "base64_decode converts input to ASCII bytes, appends b'=' * (-len(string) % 4), then calls urlsafe_b64decode inside a TypeError/ValueError-to-BadData boundary. Focused tests cover valid encode/decode and BadData.",
    "references": [
      {
        "path": "src/itsdangerous/encoding.py",
        "symbol": "base64_decode",
        "purpose": "Extract only the existing padding expression into a private helper.",
        "digest": null,
        "trust": "repository"
      },
      {
        "path": "tests/test_itsdangerous/test_encoding.py",
        "symbol": "test_base64",
        "purpose": "Read-only regression coverage for behavior preservation.",
        "digest": null,
        "trust": "repository"
      }
    ],
    "trusted_sources": [
      "/workspace/scratch/473866e9940e/repo/evals/v0.2/results/v0.2/V02-REAL-004/packet.json",
      "/workspace/scratch/473866e9940e/repo/evals/v0.2/results/v0.2/V02-REAL-004/host-metadata.json"
    ]
  },
  "decisions": {
    "fixed": [
      "The helper is module-private, accepts bytes, returns bytes, and implements exactly string + b'=' * (-len(string) % 4).",
      "base64_decode delegates only padding to the helper; its signature, conversion, decoder, exception type, and message remain unchanged.",
      "Do not export or directly test the private helper."
    ],
    "assumptions": [
      "Existing focused tests adequately detect public behavior regression for this mechanical extraction.",
      "The trusted clean base remains current at task start."
    ]
  },
  "invariants": [
    "Every input yields the same padded bytes before decoding as at the pinned base.",
    "Valid decoded values and BadData behavior remain identical.",
    "No public symbol or import surface changes."
  ],
  "non_goals": [
    "Changing input validation or ASCII conversion behavior.",
    "Generalizing padding for other encodings.",
    "Editing tests, documentation, exports, or dependencies."
  ],
  "scope": {
    "write_globs": [
      "src/itsdangerous/encoding.py"
    ],
    "read_globs": [
      "src/itsdangerous/encoding.py",
      "tests/test_itsdangerous/test_encoding.py"
    ],
    "forbidden_globs": [
      "tests/**",
      "src/itsdangerous/__init__.py",
      "docs/**",
      "pyproject.toml"
    ],
    "shared_interfaces": [
      "itsdangerous.encoding.base64_decode behavior"
    ],
    "exclusive_resources": [
      "src/itsdangerous/encoding.py:base64 padding and decode path"
    ],
    "parallel_safe": false,
    "isolation": "manual"
  },
  "required_capabilities": [
    "deterministic Python refactoring",
    "behavior-preservation review",
    "pytest regression testing"
  ],
  "execution_profile": {
    "role": "worker",
    "capability_tier": "tiny-deterministic-edit",
    "cost_tier": "lowest",
    "reasoning_effort": "medium",
    "preferred_model": null,
    "fallback_profiles": [
      "Return any non-mechanical behavior decision to the architect."
    ]
  },
  "implementation_instructions": [
    "Define a clearly named module-private bytes-to-bytes helper near base64_decode that returns the input plus exactly the existing required '=' padding.",
    "Replace only base64_decode's inline padding expression with a call to that helper.",
    "Do not move the helper into exports, change exception handling, or edit tests."
  ],
  "acceptance_criteria": [
    {
      "id": "AC1",
      "statement": "A module-private helper contains the existing Base64 padding calculation and base64_decode uses it.",
      "evidence_required": "Task-local source diff showing the private helper and single call site."
    },
    {
      "id": "AC2",
      "statement": "base64_decode's signature, decoded values, and exception type/message remain unchanged.",
      "evidence_required": "Passing existing focused tests and diff review showing no other decode-path semantic change."
    },
    {
      "id": "AC3",
      "statement": "The frozen focused encoding test command passes with only encoding.py changed.",
      "evidence_required": "Required command exit status 0, concise output, and final task-local diff/status."
    }
  ],
  "validation": [
    {
      "command": "PYTHONPATH=src python -m pytest tests/test_itsdangerous/test_encoding.py -q",
      "purpose": "Run the packet's frozen focused regression suite.",
      "mutating": true,
      "required": true
    }
  ],
  "expected_evidence": [
    "Task-local patch limited to src/itsdangerous/encoding.py.",
    "Required command, exit status, and concise passing output.",
    "Final status excluding validation-generated caches and bytecode from the product patch.",
    "Result evidence at the host-provided destination outside the checkout."
  ],
  "stop_conditions": [
    "The refactor would change conversion, padding output, decoded results, exception semantics, signature, or exports.",
    "A test, dependency, documentation, or unrelated-module edit appears necessary.",
    "The frozen validation command cannot run without installation, network, credentials, or permission expansion.",
    "The trusted base revision or clean status no longer matches."
  ],
  "risk": {
    "level": "low",
    "flags": [
      "behavior-preserving public decode path",
      "validation may create caches or bytecode"
    ]
  },
  "complexity": "trivial",
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
      "src/itsdangerous/encoding.py"
    ]
  },
  "provenance": {
    "base_revision": "672971d66a2ef9f85151e53283113f33d642dabd",
    "created_by": "eclipse-architect",
    "created_at": "2026-08-13T00:00:00+08:00"
  }
}
```
