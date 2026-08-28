{
  "schema_version": "1.0",
  "run_id": "V02-REAL-016",
  "plan_revision": 1,
  "plan_digest": "sha256:dcc4b5090331d8ea56a8694385d94729156f8aae815e2c114eae50436d57771b",
  "task_id": "V02-REAL-016-T01",
  "parent_task_id": null,
  "dependencies": [],
  "objective": "Refactor retry array validation through one private helper while preserving normalizeRetryOptions behavior and public types.",
  "rationale": "The two adjacent array guards are structurally duplicated and can share a private implementation without changing the exported surface.",
  "context_manifest": {
    "schema_version": "1.0",
    "summary": "normalizeRetryOptions contains separate methods and statusCodes array guards; focused retry tests already exercise both invalid inputs.",
    "references": [
      {"path": "source/utils/normalize.ts", "symbol": "normalizeRetryOptions", "purpose": "Implementation target and existing defaults/normalization behavior", "digest": null, "trust": "repository"},
      {"path": "test/retry.ts", "symbol": null, "purpose": "Focused regression coverage for validation errors and normalized retry behavior", "digest": null, "trust": "repository"}
    ],
    "trusted_sources": ["case packet", "trusted host metadata", "Eclipse task contract"]
  },
  "decisions": {
    "fixed": [
      "Use one unexported helper for both methods and statusCodes array validation.",
      "Preserve the exact messages 'retry.methods must be an array' and 'retry.statusCodes must be an array'.",
      "Preserve the returned object shape, defaults, lower-casing behavior, and exported/public types."
    ],
    "assumptions": ["Existing local dependencies are sufficient for validation; dependency installation is not permitted."]
  },
  "invariants": [
    "Numeric retry input retains its current shorthand behavior.",
    "Undefined option values continue to be removed before defaults are merged.",
    "No new export or public type is introduced."
  ],
  "non_goals": ["Changing retry policy", "Renaming public options", "Refactoring unrelated normalization utilities", "Adding dependencies"],
  "scope": {
    "write_globs": ["source/utils/normalize.ts", "test/retry.ts"],
    "read_globs": ["source/utils/normalize.ts", "source/types/retry.ts", "source/types/options.ts", "test/retry.ts", "package.json", "tsconfig*.json"],
    "forbidden_globs": ["source/types/**", "source/core/**", "source/index.ts", "package.json", "tsconfig*.json", "readme.md"],
    "shared_interfaces": ["normalizeRetryOptions behavior"],
    "exclusive_resources": [],
    "parallel_safe": false,
    "isolation": "worktree"
  },
  "required_capabilities": ["repository-read", "scoped-write", "TypeScript", "test-execution"],
  "execution_profile": {
    "role": "executor",
    "capability_tier": "bounded-routine",
    "cost_tier": "low",
    "reasoning_effort": "medium",
    "preferred_model": "gpt-5.6-luna",
    "fallback_profiles": ["worker"]
  },
  "implementation_instructions": [
    "Introduce the smallest private helper that accepts the value and option name needed to reproduce the existing messages.",
    "Replace only the duplicate methods/statusCodes guards with helper calls.",
    "Strengthen focused assertions so both invalid inputs prove their exact existing messages and keep representative output/default coverage behaviorally unchanged."
  ],
  "acceptance_criteria": [
    {"id": "AC-1", "statement": "The duplicate methods and statusCodes array checks are represented by one private helper.", "evidence_required": "Patch excerpt and changed-file list show one helper used for both fields with no export change."},
    {"id": "AC-2", "statement": "Invalid methods and statusCodes values throw their exact pre-refactor messages.", "evidence_required": "Focused test assertions and a passing focused test command for both messages."},
    {"id": "AC-3", "statement": "normalizeRetryOptions returns the same defaults, shape, lower-cased methods, and numeric shorthand results as before.", "evidence_required": "Passing retry test evidence, including representative normalization/default assertions."},
    {"id": "AC-4", "statement": "Only the two authorized files are changed and no dependency or public type changes occur.", "evidence_required": "Final git status/diff summary and build/type-check evidence."}
  ],
  "validation": [
    {"command": "node -e \"const fs=require('fs'); for (const p of ['source/utils/normalize.ts','test/retry.ts']) { if (!fs.readFileSync(p,'utf8').trim()) process.exit(1) }\"", "purpose": "Frozen packet validation: verify both scoped files remain non-empty", "mutating": false, "required": true},
    {"command": "npm test -- --match='throws when retry.* is not an array'", "purpose": "Supplemental lint, build/type-check, and focused invalid-array tests; dependency absence or failure does not by itself block completion", "mutating": true, "required": false}
  ],
  "expected_evidence": [
    "Clean pre-task status supplied by the host",
    "Task-local patch and final changed-file list captured before integration",
    "Exit code and concise output for every required validation command",
    "AC-1 through AC-4 evidence mapping",
    "Any validation-created distribution/cache output identified separately and absent from the product patch"
  ],
  "stop_conditions": [
    "Any behavior, message, default, return shape, or public type would need to change.",
    "Completion requires a file outside the two write globs.",
    "The implementation itself requires a new dependency or installation/network access; absence of dependencies needed only for supplemental validation is not a completion blocker.",
    "The base revision or approved plan identity does not match the contract.",
    "The packet's required frozen validation fails for a reason that cannot be fixed within scope and attempt budget."
  ],
  "risk": {"level": "low", "flags": ["behavior-preserving-refactor", "exact-error-contract"]},
  "complexity": "trivial",
  "budgets": {"max_attempts": 2, "max_review_rounds": 2},
  "authorization": {"network": false, "credentials": false, "external_side_effects": false, "destructive_actions": false, "targets": []},
  "provenance": {
    "base_revision": "3419113b48e034fdcf8fa6bd3be3da7b3d0d758f",
    "created_by": "eclipse-architect",
    "created_at": "2026-08-13T08:28:34Z"
  },
  "metadata": {"case_id": "V02-REAL-016", "artifact_destination": "/workspace/scratch/473866e9940e/repo/evals/v0.2/results/v0.2/V02-REAL-016/result.md"}
}
