# Approved Task Contracts — V02-REAL-006

## V02-REAL-006-T1

```json
{
  "schema_version": "1.0",
  "run_id": "V02-REAL-006",
  "plan_revision": 1,
  "plan_digest": "sha256:5ce0dfec3f803d55c8f43b1d51eaf4976c54a782843b835ec3a806669b0e0022",
  "task_id": "V02-REAL-006-T1",
  "dependencies": [],
  "objective": "Add 256 as the one-byte-to-two-byte int_to_bytes encoding boundary and verify its exact bytes plus round trip.",
  "rationale": "The focused parameterized test covers zero and uint64 maximum but not a byte-width transition; 256 is the first two-byte representation.",
  "context_manifest": {
    "schema_version": "1.0",
    "summary": "test_int_bytes parameterizes value, exact encoded bytes, and bytes_to_int round trip. Add one tuple for the first value beyond one-byte capacity.",
    "references": [
      {
        "path": "tests/test_itsdangerous/test_encoding.py",
        "symbol": "test_int_bytes",
        "purpose": "Extend the existing boundary parameterization with 256 and b'\\x01\\x00'.",
        "digest": null,
        "trust": "repository"
      }
    ],
    "trusted_sources": [
      "/workspace/scratch/473866e9940e/repo/evals/v0.2/results/v0.2/V02-REAL-006/packet.json",
      "/workspace/scratch/473866e9940e/repo/evals/v0.2/results/v0.2/V02-REAL-006/host-metadata.json"
    ]
  },
  "decisions": {
    "fixed": [
      "Use 256 as the additional boundary because it is the first integer whose minimal big-endian encoding requires two bytes.",
      "Expect exactly b'\\x01\\x00' and use the existing bytes_to_int round-trip assertion.",
      "Do not change production code."
    ],
    "assumptions": [
      "The trusted host's clean base remains current when this task starts."
    ]
  },
  "invariants": [
    "Existing parameter cases and assertions remain intact.",
    "Only the focused test parameterization changes.",
    "The documentation task owns docs/encoding.rst exclusively."
  ],
  "non_goals": [
    "Testing every byte-width boundary.",
    "Changing int_to_bytes or bytes_to_int behavior.",
    "Editing documentation or dependencies."
  ],
  "scope": {
    "write_globs": [
      "tests/test_itsdangerous/test_encoding.py"
    ],
    "read_globs": [
      "tests/test_itsdangerous/test_encoding.py",
      "src/itsdangerous/encoding.py"
    ],
    "forbidden_globs": [
      "src/**",
      "docs/**",
      "pyproject.toml"
    ],
    "shared_interfaces": [],
    "exclusive_resources": [
      "tests/test_itsdangerous/test_encoding.py:test_int_bytes"
    ],
    "parallel_safe": true,
    "isolation": "manual"
  },
  "required_capabilities": [
    "tiny deterministic pytest edit",
    "integer encoding boundary reasoning"
  ],
  "execution_profile": {
    "role": "worker",
    "capability_tier": "tiny-deterministic-edit",
    "cost_tier": "lowest",
    "reasoning_effort": "medium",
    "preferred_model": null,
    "fallback_profiles": [
      "Return unexpected encoding semantics to the architect."
    ]
  },
  "implementation_instructions": [
    "Add exactly the tuple (256, b'\\x01\\x00') to the existing test_int_bytes parameterization.",
    "Use the existing exact-encoding and bytes_to_int round-trip assertions without duplicating the test.",
    "Do not edit docs/encoding.rst; that file is exclusively owned by T2."
  ],
  "acceptance_criteria": [
    {
      "id": "AC1",
      "statement": "The focused test asserts int_to_bytes(256) equals b'\\x01\\x00' and bytes_to_int returns 256.",
      "evidence_required": "Task-local test diff and passing new parameter case."
    },
    {
      "id": "AC2",
      "statement": "All focused encoding tests pass with no production or documentation change in this task.",
      "evidence_required": "Required command exit status 0, concise output, and task-boundary diff/status."
    }
  ],
  "validation": [
    {
      "command": "PYTHONPATH=src python -m pytest tests/test_itsdangerous/test_encoding.py -q",
      "purpose": "Run the packet's exact frozen focused encoding suite.",
      "mutating": true,
      "required": true
    }
  ],
  "expected_evidence": [
    "Task-local patch limited to tests/test_itsdangerous/test_encoding.py.",
    "Required command, exit status, and concise passing output.",
    "Task-boundary status excluding pytest cache and bytecode from the product patch.",
    "Evidence at the host-provided external artifact destination."
  ],
  "stop_conditions": [
    "Production code, documentation, dependencies, or another test file would need modification.",
    "The frozen command cannot run without installation, network, credentials, or expanded permission.",
    "T2 or another task has modified this task's owned file before capture.",
    "The trusted base/clean status does not match."
  ],
  "risk": {
    "level": "low",
    "flags": [
      "test-only edit",
      "shared-checkout host serialization",
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

## V02-REAL-006-T2

```json
{
  "schema_version": "1.0",
  "run_id": "V02-REAL-006",
  "plan_revision": 1,
  "plan_digest": "sha256:5ce0dfec3f803d55c8f43b1d51eaf4976c54a782843b835ec3a806669b0e0022",
  "task_id": "V02-REAL-006-T2",
  "dependencies": [],
  "objective": "Clarify the URL-safe Base64 alphabet and padding behavior in docs/encoding.rst without changing code behavior.",
  "rationale": "The encoding page lists the helpers but does not explain how URL-safe Base64 differs from standard Base64 or how padding is handled.",
  "context_manifest": {
    "schema_version": "1.0",
    "summary": "docs/encoding.rst currently contains the encoding module heading and base64_encode/base64_decode autodoc entries. The code uses urlsafe Base64, strips '=' during encoding, and restores required padding during decoding.",
    "references": [
      {
        "path": "docs/encoding.rst",
        "symbol": null,
        "purpose": "Add one concise alphabet-and-padding clarification beside the helper documentation.",
        "digest": null,
        "trust": "repository"
      },
      {
        "path": "src/itsdangerous/encoding.py",
        "symbol": "base64_encode and base64_decode",
        "purpose": "Read-only source of truth for the documented alphabet and padding behavior.",
        "digest": null,
        "trust": "repository"
      }
    ],
    "trusted_sources": [
      "/workspace/scratch/473866e9940e/repo/evals/v0.2/results/v0.2/V02-REAL-006/packet.json",
      "/workspace/scratch/473866e9940e/repo/evals/v0.2/results/v0.2/V02-REAL-006/host-metadata.json"
    ]
  },
  "decisions": {
    "fixed": [
      "State that URL-safe Base64 uses '-' and '_' in place of '+' and '/'.",
      "State that base64_encode omits '=' padding and base64_decode restores required padding.",
      "Do not change or imply changes to code behavior."
    ],
    "assumptions": [
      "One short paragraph adjacent to the two autodoc entries is the intended clarification.",
      "The trusted host's clean base remains current at task start."
    ]
  },
  "invariants": [
    "The text remains accurate to the pinned implementation.",
    "No source or test code changes in this task.",
    "The test task owns tests/test_itsdangerous/test_encoding.py exclusively."
  ],
  "non_goals": [
    "Documenting URLSafeSerializer or signing envelopes.",
    "Changing API reference directives.",
    "Changing code, tests, or dependencies."
  ],
  "scope": {
    "write_globs": [
      "docs/encoding.rst"
    ],
    "read_globs": [
      "docs/encoding.rst",
      "src/itsdangerous/encoding.py"
    ],
    "forbidden_globs": [
      "src/**",
      "tests/**",
      "pyproject.toml",
      "docs/url_safe.rst"
    ],
    "shared_interfaces": [],
    "exclusive_resources": [
      "docs/encoding.rst"
    ],
    "parallel_safe": true,
    "isolation": "manual"
  },
  "required_capabilities": [
    "tiny deterministic reStructuredText edit",
    "technical documentation accuracy"
  ],
  "execution_profile": {
    "role": "worker",
    "capability_tier": "tiny-deterministic-edit",
    "cost_tier": "lowest",
    "reasoning_effort": "medium",
    "preferred_model": null,
    "fallback_profiles": [
      "Return any requested broader documentation or code behavior change to the architect."
    ]
  },
  "implementation_instructions": [
    "Add one concise paragraph to docs/encoding.rst explaining the fixed alphabet substitution and padding behavior.",
    "Keep the two existing autofunction directives and do not discuss serializer signing formats.",
    "Do not edit the focused test file; it is exclusively owned by T1."
  ],
  "acceptance_criteria": [
    {
      "id": "AC1",
      "statement": "docs/encoding.rst accurately explains '-'/'_' substitution and encoder-omitted, decoder-restored '=' padding.",
      "evidence_required": "Task-local documentation diff showing the concise clarification."
    },
    {
      "id": "AC2",
      "statement": "The packet's frozen focused tests pass and this task changes no code or tests.",
      "evidence_required": "Required command exit status 0, concise output, and task-boundary diff/status limited to docs/encoding.rst."
    }
  ],
  "validation": [
    {
      "command": "PYTHONPATH=src python -m pytest tests/test_itsdangerous/test_encoding.py -q",
      "purpose": "Run the packet's exact frozen focused encoding suite; this is the only required command.",
      "mutating": true,
      "required": true
    }
  ],
  "expected_evidence": [
    "Task-local patch limited to docs/encoding.rst.",
    "Required command, exit status, and concise passing output.",
    "Task-boundary status excluding pytest cache and bytecode from the product patch.",
    "Evidence at the host-provided external artifact destination."
  ],
  "stop_conditions": [
    "Accurate wording would require a code, test, dependency, or second documentation-file change.",
    "The frozen command cannot run without installation, network, credentials, or expanded permission.",
    "T1 or another task has modified this task's owned file before capture.",
    "The trusted base/clean status does not match."
  ],
  "risk": {
    "level": "low",
    "flags": [
      "documentation-only edit",
      "shared-checkout host serialization",
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
