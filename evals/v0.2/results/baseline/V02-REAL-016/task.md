{
  "schema_version": "1.0",
  "run_id": "V02-REAL-016",
  "plan_revision": 1,
  "plan_digest": "sha256:d8c84f14a62577ed879859129b1bbb0216eec008094ad415ab719da16cf27665",
  "task_id": "V02-REAL-016-T001",
  "parent_task_id": null,
  "dependencies": [],
  "objective": "Refactor normalizeRetryOptions to use one private helper for methods and statusCodes array validation, with focused regression assertions and no observable behavior change.",
  "rationale": "The two adjacent validation branches duplicate the same predicate and differ only by option name and exact error text. A private helper removes that duplication without changing the public surface or retry normalization.",
  "context_manifest": {
    "schema_version": "1.0",
    "summary": "normalizeRetryOptions currently performs separate truthy-and-not-array checks for retry.methods and retry.statusCodes before normalizing defined overrides. test/retry.ts contains focused invalid-value tests for both fields but does not assert their messages.",
    "references": [
      {
        "path": "source/utils/normalize.ts",
        "symbol": "normalizeRetryOptions",
        "purpose": "Private refactor target and source of current validation/default behavior",
        "digest": "sha256:3ac353db9ae677df5789da451377621c958c4e3e66f03cdd86b66b17ebc7c95e",
        "trust": "repository"
      },
      {
        "path": "test/retry.ts",
        "symbol": null,
        "purpose": "Focused regression tests for invalid retry.methods and retry.statusCodes values",
        "digest": "sha256:85d931705ff50366a2d96da4fd557f7a31cf01c7109904ca0e1e8d9327599d0d",
        "trust": "repository"
      },
      {
        "path": "evals/v0.2/results/baseline/V02-REAL-016/packet.json",
        "symbol": null,
        "purpose": "Authorized task requirement and acceptance boundary",
        "digest": "sha256:6237322cbed5f02130200568f70fbda6e699c8869ee98427011ccce5ecfed32a",
        "trust": "harness"
      }
    ],
    "trusted_sources": [
      "user requirement",
      "V02-REAL-016 harness packet",
      "Eclipse task-contract schema and orchestration policy"
    ]
  },
  "decisions": {
    "fixed": [
      "Define exactly one non-exported helper in source/utils/normalize.ts and use it for both methods and statusCodes array validation.",
      "Preserve the current validation predicate: only truthy non-array values are rejected; this refactor must not broaden runtime validation of falsy values.",
      "Preserve the exact messages `retry.methods must be an array` and `retry.statusCodes must be an array`.",
      "Preserve normalizeRetryOptions return shape, defaultRetryOptions values, methods lowercasing, exports, and public TypeScript types.",
      "Tighten the two existing invalid-value tests in test/retry.ts to assert the exact corresponding message."
    ],
    "assumptions": [
      "The checkout remains at repository commit 3419113b48e034fdcf8fa6bd3be3da7b3d0d758f.",
      "Project development dependencies are already available for offline validation.",
      "No production caller relies on a new helper export because the helper is deliberately private."
    ]
  },
  "invariants": [
    "Both option checks run before Object.entries normalization.",
    "Numeric retry shorthand behavior remains unchanged.",
    "Default retry arrays and scalar defaults retain their current values and identity behavior.",
    "Valid arrays, absent values, and current falsy runtime values produce the same normalized output as before.",
    "No public module export or declared public type changes."
  ],
  "non_goals": [
    "Adding validation for other retry fields",
    "Changing which falsy invalid runtime values are accepted",
    "Changing retry defaults or normalization semantics",
    "Exporting or generalizing the helper outside source/utils/normalize.ts",
    "Unrelated test cleanup or formatting",
    "Dependency or build configuration changes"
  ],
  "scope": {
    "write_globs": [
      "source/utils/normalize.ts",
      "test/retry.ts"
    ],
    "read_globs": [
      "source/utils/normalize.ts",
      "source/types/retry.ts",
      "source/types/options.ts",
      "source/core/constants.ts",
      "test/retry.ts",
      "package.json",
      "tsconfig.json",
      "tsconfig.dist.json"
    ],
    "forbidden_globs": [
      ".git/**",
      ".github/**",
      "distribution/**",
      "node_modules/**",
      "package.json",
      "package-lock.json",
      "pnpm-lock.yaml",
      "yarn.lock"
    ],
    "shared_interfaces": [],
    "exclusive_resources": [
      "source/utils/normalize.ts",
      "test/retry.ts"
    ],
    "parallel_safe": false,
    "isolation": "worktree"
  },
  "required_capabilities": [
    "repository-read",
    "scoped-write",
    "typescript-refactor",
    "test-execution",
    "static-analysis"
  ],
  "execution_profile": {
    "role": "executor",
    "capability_tier": "bounded-routine",
    "cost_tier": "low",
    "reasoning_effort": "high",
    "preferred_model": "gpt-5.6-luna",
    "fallback_profiles": [
      "worker"
    ]
  },
  "implementation_instructions": [
    "Verify HEAD equals the provenance base revision and that the approved files have no pre-existing modifications before editing.",
    "Add one private helper near normalizeRetryOptions that accepts only the option-name information and value needed to reproduce the two existing checks.",
    "Keep the helper's runtime predicate equivalent to `value && !Array.isArray(value)`; do not convert this refactor into stricter input validation.",
    "Use the helper once for retry.methods and once for retry.statusCodes, preserving their order before normalizedRetry is constructed.",
    "Construct or select the error text so the two existing messages are byte-for-byte unchanged.",
    "Update only the two existing invalid-array tests to assert the exact respective error messages.",
    "Do not export the helper, modify RetryOptions, change defaults, alter methods mapping, or reformat unrelated code.",
    "Run every required validation command without network access and return criterion-indexed evidence plus the final changed-file list."
  ],
  "acceptance_criteria": [
    {
      "id": "AC-1",
      "statement": "The duplicate methods and statusCodes array-validation branches are replaced by calls to one private helper.",
      "evidence_required": "Scoped diff showing one non-exported helper and both call sites, with no second inline array-check branch."
    },
    {
      "id": "AC-2",
      "statement": "Invalid truthy non-array methods and statusCodes values throw the exact pre-refactor messages.",
      "evidence_required": "Assertions in the two focused tests for `retry.methods must be an array` and `retry.statusCodes must be an array`, plus a passing focused AVA command."
    },
    {
      "id": "AC-3",
      "statement": "normalizeRetryOptions preserves its return shape, defaults, public types, valid-array behavior, and current truthiness semantics.",
      "evidence_required": "Scoped source diff contains no changes to defaultRetryOptions, normalizedRetry construction, exports, or type declarations; focused tests and TypeScript validation pass."
    },
    {
      "id": "AC-4",
      "statement": "The implementation changes no files outside source/utils/normalize.ts and test/retry.ts.",
      "evidence_required": "Final `git status --short` and `git diff --name-only` list only the approved files."
    }
  ],
  "validation": [
    {
      "command": "node -e \"const fs=require('fs'); for (const p of ['source/utils/normalize.ts','test/retry.ts']) { if (!fs.readFileSync(p,'utf8').trim()) process.exit(1) }\"",
      "purpose": "Run the packet-provided non-empty-file smoke check",
      "mutating": false,
      "required": true
    },
    {
      "command": "npx --no-install ava test/retry.ts --match='throws when retry.* is not an array'",
      "purpose": "Verify both focused invalid-array cases and their exact message assertions",
      "mutating": false,
      "required": true
    },
    {
      "command": "npx --no-install xo source/utils/normalize.ts test/retry.ts",
      "purpose": "Lint the only approved files",
      "mutating": false,
      "required": true
    },
    {
      "command": "npx --no-install tsc --noEmit --project tsconfig.json",
      "purpose": "Verify the refactor and tests remain type-correct without generating distribution files",
      "mutating": false,
      "required": true
    },
    {
      "command": "git diff --check && git diff --name-only && git status --short",
      "purpose": "Verify patch hygiene and the authorized two-file boundary",
      "mutating": false,
      "required": true
    }
  ],
  "expected_evidence": [
    "Base revision verification",
    "Final changed-file list",
    "Scoped diff showing one private helper and two call sites",
    "Exact-message assertions for methods and statusCodes",
    "Required validation commands with exit status and relevant output",
    "Explicit AC-1 through AC-4 evidence mapping"
  ],
  "stop_conditions": [
    "HEAD or the inspected source context differs from provenance base revision 3419113b48e034fdcf8fa6bd3be3da7b3d0d758f.",
    "Any required production or test change falls outside the two write_globs.",
    "Preserving behavior would require changing a public export, public type, retry default, return shape, or dependency.",
    "A required validation command cannot run offline because dependencies or tools are unavailable; report the environment blocker rather than installing or using the network.",
    "A required check fails for a reason not caused by the bounded patch or needs architecture/scope judgment.",
    "Credentials, network access, destructive actions, or external side effects become necessary."
  ],
  "risk": {
    "level": "low",
    "flags": [
      "behavior-preservation",
      "exact-error-contract",
      "runtime-invalid-input-semantics"
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
      "source/utils/normalize.ts",
      "test/retry.ts"
    ]
  },
  "provenance": {
    "base_revision": "3419113b48e034fdcf8fa6bd3be3da7b3d0d758f",
    "created_by": "eclipse-architect",
    "created_at": "2026-08-13T05:05:46Z",
    "source_requirement_digest": "sha256:6237322cbed5f02130200568f70fbda6e699c8869ee98427011ccce5ecfed32a"
  },
  "metadata": {
    "case_id": "V02-REAL-016",
    "case_type": "real",
    "repository": "REAL-TS-NODE",
    "policy": "sol-luna-v0.1",
    "routing_status": "policy-only-unverified",
    "execution_wave": 1
  }
}

