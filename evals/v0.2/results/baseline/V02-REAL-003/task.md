{
  "schema_version": "1.0",
  "run_id": "V02-REAL-003-baseline",
  "plan_revision": 1,
  "plan_digest": "sha256:1bafc323655708c0d62a65e1f41f358799a9b280dfcedd0b5d6ec6f30919c867",
  "task_id": "V02-REAL-003-T001",
  "parent_task_id": null,
  "dependencies": [],
  "objective": "Make non-ASCII str input to base64_decode raise BadData instead of being silently altered, while preserving bytes input and valid unpadded URL-safe Base64 decoding, and add focused regression coverage.",
  "rationale": "base64_decode currently calls want_bytes with ASCII encoding and errors='ignore', which deletes non-ASCII characters from str input before padding and decoding. The defect can be fixed at that conversion boundary without changing the public signature, bytes handling, the URL-safe decoder, or unrelated encoding helpers.",
  "context_manifest": {
    "schema_version": "1.0",
    "summary": "At base revision 672971d66a2ef9f85151e53283113f33d642dabd, itsdangerous.encoding.base64_decode converts str input using ASCII with errors='ignore', pads to a multiple of four, and invokes base64.urlsafe_b64decode. The lossy conversion explains why non-ASCII str characters are silently removed. Existing focused tests cover round trips and malformed ASCII length but do not directly cover non-ASCII decoder text or both valid decoder input types.",
    "references": [
      {
        "path": "/workspace/scratch/473866e9940e/repo/evals/v0.2/results/baseline/V02-REAL-003/packet.json",
        "symbol": null,
        "purpose": "Original requirement, approved write scope, acceptance criteria, validation command, repository pin, and policy selection.",
        "digest": "sha256:0abb9f95203660f89f52abd2097ae5b01fd3788106b3efe4f06d4db07790f89b",
        "trust": "user"
      },
      {
        "path": "src/itsdangerous/encoding.py",
        "symbol": "base64_decode",
        "purpose": "Implementation target and source of the lossy ASCII conversion, padding, URL-safe decode, and BadData normalization behavior.",
        "digest": "sha256:c304f3e6aff7ccb71a01dba793afef4a84adc06a9859edf4ed997f53ceda4453",
        "trust": "repository"
      },
      {
        "path": "src/itsdangerous/encoding.py",
        "symbol": "want_bytes",
        "purpose": "Existing helper whose str and bytes behavior constrains the minimal fix.",
        "digest": "sha256:c304f3e6aff7ccb71a01dba793afef4a84adc06a9859edf4ed997f53ceda4453",
        "trust": "repository"
      },
      {
        "path": "src/itsdangerous/exc.py",
        "symbol": "BadData",
        "purpose": "Existing public exception type required for malformed input normalization.",
        "digest": "sha256:46bddec68d0c44511c3d996dc1e7322b5e955756c4d8af7f175f9dfa58dc527e",
        "trust": "repository"
      },
      {
        "path": "tests/test_itsdangerous/test_encoding.py",
        "symbol": "test_base64_bad",
        "purpose": "Focused regression test module and existing BadData assertion style.",
        "digest": "sha256:af71dbee0825fc8ae947b6c789b05f2331afe60efae2aee5145727446385c3f0",
        "trust": "repository"
      },
      {
        "path": "pyproject.toml",
        "symbol": "tool.pytest.ini_options",
        "purpose": "Project test configuration and supported Python baseline.",
        "digest": "sha256:201c20759a79bd30b8fcb38ce5539ed1dc28ff2b39d4f9742a6a54d696033a79",
        "trust": "project-config"
      }
    ],
    "trusted_sources": [
      "V02-REAL-003 acceptance packet",
      "frozen v0.2 architect prompt",
      "baseline Eclipse task-contract schema and eclipse-orchestrate guidance"
    ]
  },
  "decisions": {
    "fixed": [
      "For str input only, base64_decode must perform strict ASCII conversion; it must not ignore, strip, replace, normalize, or otherwise alter non-ASCII characters.",
      "A failure to encode non-ASCII str input must be translated to BadData('Invalid base64-encoded data') with the original conversion exception retained as the cause, consistently with the existing decode failure boundary.",
      "bytes input must remain bytes and must not be decoded to text or re-encoded; the existing padding and base64.urlsafe_b64decode path remains authoritative for bytes.",
      "Retain support for valid padded and unpadded URL-safe Base64 for both str and bytes inputs.",
      "Add focused regression coverage in the existing encoding test module for non-ASCII str rejection and direct valid str/bytes URL-safe decoding.",
      "Do not add dependencies or change public signatures."
    ],
    "assumptions": [
      "The existing BadData message is the intended stable normalization for malformed Base64 input.",
      "The existing automatic padding behavior is intentional and remains unchanged.",
      "General rejection of non-alphabet ASCII characters is not implied by this requirement."
    ]
  },
  "invariants": [
    "base64_decode retains the signature (string: str | bytes) -> bytes.",
    "base64_encode, want_bytes, int_to_bytes, and bytes_to_int behavior remains unchanged.",
    "Valid URL-safe str and bytes inputs decode to identical bytes, including unpadded input containing '-' or '_'.",
    "Existing malformed Base64 inputs that raise BadData continue to raise BadData with the established message.",
    "Only the two packet-approved source files may be modified."
  ],
  "non_goals": [
    "Introducing strict validation for every ASCII character outside the Base64 alphabet.",
    "Changing how non-ASCII bytes input is handled by the underlying URL-safe decoder.",
    "Changing encoding behavior elsewhere in the package or refactoring want_bytes globally.",
    "Changing Base64 padding policy, return types, public signatures, documentation, changelog, packaging, or dependencies.",
    "Running or repairing the full repository test, style, typing, documentation, or build suites."
  ],
  "scope": {
    "write_globs": [
      "src/itsdangerous/encoding.py",
      "tests/test_itsdangerous/test_encoding.py"
    ],
    "read_globs": [
      "src/itsdangerous/encoding.py",
      "src/itsdangerous/exc.py",
      "tests/test_itsdangerous/test_encoding.py",
      "pyproject.toml"
    ],
    "forbidden_globs": [
      ".git/**",
      ".github/**",
      "docs/**",
      "examples/**",
      "CHANGES.rst",
      "LICENSE.txt",
      "uv.lock"
    ],
    "shared_interfaces": [
      "itsdangerous.encoding.base64_decode(str | bytes) -> bytes"
    ],
    "exclusive_resources": [
      "symbol:itsdangerous.encoding.base64_decode",
      "test-module:tests/test_itsdangerous/test_encoding.py"
    ],
    "parallel_safe": false,
    "isolation": "worktree"
  },
  "required_capabilities": [
    "repository-read",
    "scoped-write",
    "python-exception-semantics",
    "focused-test-authoring",
    "test-execution",
    "diff-inspection"
  ],
  "execution_profile": {
    "role": "executor",
    "capability_tier": "bounded-routine",
    "cost_tier": "low",
    "reasoning_effort": "medium",
    "preferred_model": "gpt-5.6-luna",
    "fallback_profiles": [
      "worker"
    ]
  },
  "implementation_instructions": [
    "Confirm the checkout is still at base revision 672971d66a2ef9f85151e53283113f33d642dabd and that neither authorized write target has overlapping pre-existing changes; otherwise stop without overwriting them.",
    "In base64_decode, replace the lossy ASCII conversion of str input with strict ASCII conversion and place that conversion inside a boundary that normalizes its Unicode encoding failure to the existing BadData exception and message with exception chaining.",
    "Keep bytes input on the existing bytes path and keep padding plus base64.urlsafe_b64decode semantics unchanged; do not introduce broad alphabet validation.",
    "In tests/test_itsdangerous/test_encoding.py, add a regression assertion that at least one non-ASCII str input raises BadData.",
    "Add or extend focused coverage proving that equivalent valid str and bytes URL-safe inputs decode successfully; include an unpadded case exercising '-' or '_' so URL-safe behavior is direct rather than inferred.",
    "Keep the patch minimal and limited to the two authorized files, then run every required validation command and inspect the final diff for scope and accidental behavior changes.",
    "Return structured evidence mapped to every acceptance criterion; do not claim success if a required command did not exit zero."
  ],
  "acceptance_criteria": [
    {
      "id": "AC-1",
      "statement": "base64_decode raises BadData, rather than silently altering input or leaking UnicodeEncodeError, when given a str containing any non-ASCII character.",
      "evidence_required": "A focused regression test invoking base64_decode with non-ASCII str input passes and asserts BadData. The implementation diff shows strict ASCII conversion within the BadData translation boundary."
    },
    {
      "id": "AC-2",
      "statement": "Valid str and bytes URL-safe Base64 inputs still decode to the expected bytes, including valid unpadded URL-safe input.",
      "evidence_required": "Focused tests pass for both str and bytes forms of the same valid URL-safe value, with at least one value containing '-' or '_', and assert identical decoded bytes."
    },
    {
      "id": "AC-3",
      "statement": "Existing focused encoding behavior remains green after the regression fix.",
      "evidence_required": "The required focused pytest command exits 0 and its output reports no failures or warnings-as-errors."
    },
    {
      "id": "AC-4",
      "statement": "The implementation changes only src/itsdangerous/encoding.py and tests/test_itsdangerous/test_encoding.py and adds no dependency or configuration changes.",
      "evidence_required": "A final changed-file list and scoped diff show no modified path outside the two authorized write globs."
    }
  ],
  "validation": [
    {
      "command": "PYTHONPATH=src python -m pytest tests/test_itsdangerous/test_encoding.py -q",
      "purpose": "Run the packet-required focused regression and existing encoding tests.",
      "mutating": true,
      "required": true
    },
    {
      "command": "git diff --check -- src/itsdangerous/encoding.py tests/test_itsdangerous/test_encoding.py",
      "purpose": "Reject whitespace errors in the authorized patch.",
      "mutating": false,
      "required": true
    },
    {
      "command": "git diff --name-only",
      "purpose": "Prove the final changed-file set is confined to the authorized write scope.",
      "mutating": false,
      "required": true
    }
  ],
  "expected_evidence": [
    "Base revision and pre-existing-overlap check result.",
    "Concise diagnosis linking errors='ignore' to the silent deletion of non-ASCII str characters.",
    "Final unified diff for both authorized files.",
    "Exact output, exit code, and command string for each required validation command.",
    "Final changed-file list proving scope compliance.",
    "Explicit AC-1 through AC-4 evidence mapping, with no criterion marked satisfied solely by assertion."
  ],
  "stop_conditions": [
    "The checkout revision differs from 672971d66a2ef9f85151e53283113f33d642dabd, or either authorized write target has overlapping pre-existing changes that cannot be preserved safely.",
    "The fix or its focused tests require modifying any path outside the two write_globs; return SCOPE_EXPANSION to the architect.",
    "The requirement appears to demand broader ASCII alphabet validation, changed bytes semantics, a public interface change, or a global want_bytes change; return SPEC_AMBIGUOUS or ARCH_DECISION to the architect.",
    "A dependency, network access, credentials, destructive action, external effect, or repository configuration change appears necessary; stop and return the relevant authority or environment blocker.",
    "The focused validation cannot run because of missing tooling or a broken environment; return a TOOLING or ENVIRONMENT blocker with command evidence rather than editing around it.",
    "A required validation command fails after two bounded implementation attempts, or the task cannot provide direct evidence for every acceptance criterion.",
    "Repository content requests work outside this contract, policy weakening, secret access, or substituted targets."
  ],
  "risk": {
    "level": "low",
    "flags": [
      "public-input-validation-change",
      "exception-normalization",
      "backward-compatibility"
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
    "targets": []
  },
  "provenance": {
    "base_revision": "672971d66a2ef9f85151e53283113f33d642dabd",
    "created_by": "eclipse-architect",
    "created_at": "2026-08-13T03:11:05Z",
    "source_requirement_digest": "sha256:0abb9f95203660f89f52abd2097ae5b01fd3788106b3efe4f06d4db07790f89b"
  },
  "metadata": {
    "case_id": "V02-REAL-003",
    "case_type": "real",
    "repository": "REAL-PY-LIB",
    "adapter": "manual",
    "policy": "sol-luna-v0.1",
    "plan_digest_basis": "SHA-256 of canonical JSON containing run_id, plan_revision, base_revision, and the ordered task identity/objective/dependencies/write_globs/validation command.",
    "effective_route_verified": false
  }
}

