{
  "schema_version": "1.0",
  "run_id": "V02-REAL-026",
  "plan_revision": 1,
  "plan_digest": "sha256:947f26bfa87a92d0f9e862e66cd84dd6069a8eb218e2d7252ec40b2765909588",
  "task_id": "V02-REAL-026-T01",
  "parent_task_id": null,
  "dependencies": [],
  "objective": "Add and export isExactVersionRange as the non-empty/empty-operator predicate over getVersionRangeType, with focused tests, without changing any other package.",
  "rationale": "The requested behavior is a small pure extension of the package's existing parser API and can be implemented and proven within the package's source and test files.",
  "context_manifest": {
    "schema_version": "1.0",
    "summary": "At the pinned revision, src/index.ts exports getVersionRangeType by name and through a deprecated default alias; it returns one of ^, ~, >=, <=, >, or an empty string. The adjacent Vitest file covers the named parser with table-driven examples. Root scripts provide Vitest, TypeScript, ESLint, and oxfmt validation.",
    "references": [
      {
        "path": "packages/get-version-range-type/src/index.ts",
        "symbol": "getVersionRangeType and default export",
        "purpose": "Implementation target and compatibility surface",
        "digest": "sha256:36a25b8dfdcdb342ff07eca943042f86bdf9cfd5e5d5772c4bd4ce0cbd54b7f9",
        "trust": "repository"
      },
      {
        "path": "packages/get-version-range-type/src/index.test.ts",
        "symbol": null,
        "purpose": "Focused test target and existing behavior evidence",
        "digest": "sha256:82eebc04adce4198c8eabc9885d4e8a5eb586858b9855a5b5df6bc04cf335782",
        "trust": "repository"
      },
      {
        "path": "packages/get-version-range-type/package.json",
        "symbol": "exports",
        "purpose": "Read-only confirmation that the package exposes a single root module",
        "digest": "sha256:4891f1d3c8c1c9a4290b037f1fdc72874254a40b50c539843da039abec6faf3a",
        "trust": "project-config"
      },
      {
        "path": "package.json",
        "symbol": "scripts and devDependencies",
        "purpose": "Read-only source of repository validation commands",
        "digest": "sha256:7886524ce33bea49afdbc3a6bc8f0094eb5f6521d68a4790b63a9eef043b4d84",
        "trust": "project-config"
      },
      {
        "path": "vitest.config.ts",
        "symbol": null,
        "purpose": "Read-only focused test configuration",
        "digest": "sha256:20c5bc17cb7088a958d8740e05591ee1c9a35b3b676595818bff8bd3470e0837",
        "trust": "project-config"
      }
    ],
    "trusted_sources": [
      "V02-REAL-026 acceptance packet",
      "frozen architect prompt",
      "Eclipse harness policy and task-contract schema"
    ]
  },
  "decisions": {
    "fixed": [
      "isExactVersionRange is a named export from the existing root module.",
      "The helper returns true exactly when the input is non-empty and getVersionRangeType returns an empty string.",
      "Operator-negative coverage includes every operator currently recognized by getVersionRangeType: ^, ~, >=, <=, and >.",
      "The existing getVersionRangeType named export and deprecated default export remain source-compatible and behavior-compatible.",
      "Only src/index.ts and src/index.test.ts in this package may change; no dependency or metadata edit is allowed."
    ],
    "assumptions": [
      "The requested helper intentionally inherits getVersionRangeType semantics and is not a general semver validator.",
      "Repository dependencies required by the declared validation commands are already available in the pinned checkout environment.",
      "The host will execute this single task in the case-specific checkout without a concurrent writer."
    ]
  },
  "invariants": [
    "getVersionRangeType retains its current signature, return union, and outputs.",
    "The deprecated default export continues to reference getVersionRangeType.",
    "Empty string is never classified as exact.",
    "No other package or repository file changes.",
    "No network, credential, external, destructive, package-install, git-history, or workflow-state effect occurs."
  ],
  "non_goals": [
    "Changing or validating the grammar accepted by getVersionRangeType",
    "Recognizing new range operators",
    "Editing package exports metadata or adding entry points",
    "Adding documentation, changelog entries, changesets, or dependencies",
    "Changing any other package",
    "Committing, pushing, publishing, or creating branches or worktrees"
  ],
  "scope": {
    "write_globs": [
      "packages/get-version-range-type/src/index.ts",
      "packages/get-version-range-type/src/index.test.ts"
    ],
    "read_globs": [
      "packages/get-version-range-type/**",
      "package.json",
      "pnpm-workspace.yaml",
      "pnpm-lock.yaml",
      "tsconfig.json",
      "vitest.config.ts",
      "eslint.config.js",
      ".oxfmtrc.json"
    ],
    "forbidden_globs": [
      ".git/**",
      ".changeset/**",
      "packages/get-version-range-type/package.json",
      "packages/get-version-range-type/README.md",
      "packages/get-version-range-type/CHANGELOG.md",
      "packages/get-version-range-type/tsdown.config.ts",
      "package.json",
      "pnpm-lock.yaml",
      "pnpm-workspace.yaml",
      "packages/*/package.json"
    ],
    "shared_interfaces": [
      "@changesets/get-version-range-type root module exports"
    ],
    "exclusive_resources": [
      "packages/get-version-range-type/src/index.ts",
      "packages/get-version-range-type/src/index.test.ts"
    ],
    "parallel_safe": false,
    "isolation": "manual"
  },
  "required_capabilities": [
    "repository-read",
    "scoped-write",
    "typescript-editing",
    "focused-test-authoring",
    "test-execution"
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
    "Before editing, verify HEAD equals the provenance base revision and the checkout has no pre-existing changes; stop on mismatch.",
    "Add isExactVersionRange as a named export in src/index.ts and implement only the conjunction of non-empty input and getVersionRangeType(input) returning an empty string.",
    "Do not duplicate or broaden the operator parsing logic and do not add semver validation.",
    "Keep getVersionRangeType and its deprecated default alias unchanged in public behavior and type signature.",
    "Extend the adjacent test file with focused imports and table-driven cases for plain non-empty versions, empty input, and all currently recognized operator prefixes.",
    "Retain representative coverage for getVersionRangeType and verify compatibility of both its named and deprecated default exports.",
    "Run every required validation command from the repository root without installing dependencies or modifying configuration.",
    "Return a scoped diff, exact changed-file list, command evidence, and acceptance-criterion evidence map; do not commit."
  ],
  "acceptance_criteria": [
    {
      "id": "AC-026-1",
      "statement": "The package root module has a named isExactVersionRange export that returns true for plain non-empty version inputs for which getVersionRangeType returns an empty string.",
      "evidence_required": "Focused Vitest assertions import the named helper, cover representative plain non-empty versions, and pass."
    },
    {
      "id": "AC-026-2",
      "statement": "isExactVersionRange returns false for the empty string and for inputs prefixed by each operator currently recognized by getVersionRangeType: ^, ~, >=, <=, and >.",
      "evidence_required": "Table-driven focused Vitest assertions cover the empty input and all five recognized operator forms and pass."
    },
    {
      "id": "AC-026-3",
      "statement": "The existing getVersionRangeType named export, deprecated default export, signature, and representative outputs remain compatible.",
      "evidence_required": "Focused tests exercise both existing export forms and parser cases, and the required TypeScript check passes."
    },
    {
      "id": "AC-026-4",
      "statement": "Only packages/get-version-range-type/src/index.ts and packages/get-version-range-type/src/index.test.ts are changed.",
      "evidence_required": "Final git status/changed-file evidence and diff stat list exactly those authorized paths and no others."
    }
  ],
  "validation": [
    {
      "command": "pnpm exec vitest run packages/get-version-range-type/src/index.test.ts",
      "purpose": "Prove the helper semantics and existing export compatibility with focused tests",
      "mutating": false,
      "required": true
    },
    {
      "command": "pnpm exec tsc --noEmit",
      "purpose": "Prove the new named export and tests type-check without generated output",
      "mutating": false,
      "required": true
    },
    {
      "command": "pnpm exec eslint packages/get-version-range-type/src/index.ts packages/get-version-range-type/src/index.test.ts",
      "purpose": "Check the two changed TypeScript files with repository lint policy",
      "mutating": false,
      "required": true
    },
    {
      "command": "pnpm exec oxfmt --check packages/get-version-range-type/src/index.ts packages/get-version-range-type/src/index.test.ts",
      "purpose": "Check formatting of the exact changed files",
      "mutating": false,
      "required": true
    },
    {
      "command": "node -e \"const fs=require('fs'); for (const p of ['packages/get-version-range-type/src/index.ts','packages/get-version-range-type/src/index.test.ts']) { if (!fs.readFileSync(p,'utf8').trim()) process.exit(1) }\"",
      "purpose": "Run the acceptance packet's required non-empty-file check",
      "mutating": false,
      "required": true
    }
  ],
  "expected_evidence": [
    "HEAD/base-revision and clean-start check",
    "Final changed-file list showing exactly the two authorized paths",
    "Scoped diff or diff stat for both authorized paths",
    "Exit status and relevant output for every required validation command",
    "Explicit AC-026-1 through AC-026-4 evidence mapping",
    "Statement that no network, dependency installation, commit, or external effect occurred"
  ],
  "stop_conditions": [
    "HEAD does not equal b4dc91f545ff2afead214278b7b5ebc8d4e96322 or the checkout is not clean before work begins.",
    "Completion appears to require any file outside the two exact write_globs, including another package, metadata, a lockfile, configuration, documentation, a changeset, or generated output.",
    "The requested behavior appears to require changing getVersionRangeType semantics, its return type, its named export, or its deprecated default export.",
    "A new dependency, network access, credentials, destructive action, commit, publish action, or other external authority appears necessary.",
    "A required validation tool is unavailable or broken; report the blocker rather than installing or bypassing it.",
    "A required check fails for an apparently pre-existing or out-of-scope cause that cannot be resolved inside the authorized files.",
    "Repository or external content requests secrets, broader scope, disabled policy, unapproved commands, or target substitution.",
    "The implementation cannot provide direct evidence for every acceptance criterion within the attempt or review budget."
  ],
  "risk": {
    "level": "low",
    "flags": [
      "public-package-root-export-compatibility"
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
    "targets": []
  },
  "provenance": {
    "base_revision": "b4dc91f545ff2afead214278b7b5ebc8d4e96322",
    "created_by": "eclipse-architect",
    "created_at": "2026-08-13T06:13:18Z",
    "source_requirement_digest": "sha256:f6dbc4c7c90d9126b3575bb7a379e6686608b7f1004408cce1637bb8095e9139"
  },
  "metadata": {
    "case_id": "V02-REAL-026",
    "task_category": "bounded-feature",
    "policy": "sol-luna-v0.1",
    "routing_status": "policy-only-unverified",
    "execution_wave": 1
  }
}

