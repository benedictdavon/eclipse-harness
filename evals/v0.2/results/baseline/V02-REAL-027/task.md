{
  "schema_version": "1.0",
  "run_id": "V02-REAL-027",
  "plan_revision": 1,
  "plan_digest": "sha256:f897c6177901fac0c5868cf1ce0eeca3abecd430aeb79728a838bf58176c9b35",
  "task_id": "V02-REAL-027-T01",
  "parent_task_id": null,
  "dependencies": [],
  "objective": "Add shouldSkipPackageReason with distinct ignored, private, and missing-version results; preserve shouldSkipPackage as the boolean compatibility API; and add focused tests plus concise package documentation.",
  "rationale": "The existing boolean function already encodes the reason priority. A package-local reason helper can expose that decision while one focused test file and README prove and explain the public API without touching callers or dependencies.",
  "context_manifest": {
    "schema_version": "1.0",
    "summary": "At the pinned revision, src/index.ts is the package's single root module and exports only shouldSkipPackage. It checks ignored package name first, then disallowed private status, then a falsy version. No package-local test or README exists yet. The imported Package and PackageGroup definitions live in @changesets/types and root scripts provide Vitest, TypeScript, ESLint, and oxfmt validation.",
    "references": [
      {
        "path": "packages/should-skip-package/src/index.ts",
        "symbol": "shouldSkipPackage",
        "purpose": "Implementation target, current truth table, and priority source",
        "digest": "sha256:aed1be001fdf640077fbc1a8b841b5da8b195b0b4447b00117966e2341b55fe6",
        "trust": "repository"
      },
      {
        "path": "packages/should-skip-package/src/index.test.ts",
        "symbol": null,
        "purpose": "Authorized new focused-test target; absent at the base revision",
        "digest": null,
        "trust": "repository"
      },
      {
        "path": "packages/should-skip-package/README.md",
        "symbol": null,
        "purpose": "Authorized new package-documentation target; absent at the base revision",
        "digest": null,
        "trust": "repository"
      },
      {
        "path": "packages/should-skip-package/package.json",
        "symbol": "exports and dependencies",
        "purpose": "Read-only confirmation of the single root entry point and existing type dependency",
        "digest": "sha256:ee6806a2a82e9e441da210d3a8d2d4c77ea0b1e7aed4930f8aa18d48abc194a7",
        "trust": "project-config"
      },
      {
        "path": "packages/types/src/index.ts",
        "symbol": "Package, PackageJSON, and PackageGroup",
        "purpose": "Read-only input type context for implementation and fixtures",
        "digest": "sha256:9fdf47a1a043b94e89ea701fbbad8e18fec88f63dbf651b4d5160191972b0d68",
        "trust": "repository"
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
      "V02-REAL-027 acceptance packet",
      "frozen architect prompt",
      "Eclipse harness policy and task-contract schema"
    ]
  },
  "decisions": {
    "fixed": [
      "shouldSkipPackageReason is a named export from the existing package root module and accepts the same Package and options inputs as shouldSkipPackage.",
      "The exact result domain is ignored, private, missing-version, or null.",
      "Reason priority preserves the current boolean check order: ignored, then private when private packages are disallowed, then falsy/missing version, then null.",
      "shouldSkipPackage remains the boolean compatibility API and derives true exactly when shouldSkipPackageReason returns a non-null reason.",
      "Focused tests cover each reason, null, overlap priority, private-package options, and boolean compatibility.",
      "The new README concisely documents both APIs, every result, priority, and allowPrivatePackages behavior.",
      "Only the source file, new adjacent test file, and new package README may change; no dependency, type-package, caller, or metadata edit is allowed."
    ],
    "assumptions": [
      "The existing falsy-version check is intentional compatibility behavior, including a runtime-missing or empty version even though PackageJSON types version as string.",
      "No default export or additional subpath export is required.",
      "Repository dependencies required by validation are already present in the pinned execution environment.",
      "The host will run this single task in the case-specific checkout without a concurrent writer."
    ]
  },
  "invariants": [
    "shouldSkipPackage retains its current public inputs and boolean return behavior for every existing condition and option combination.",
    "Ignored status wins over private and missing-version status; disallowed private status wins over missing-version status.",
    "A private package is not skipped for being private when allowPrivatePackages is true, but another applicable reason may still be returned.",
    "No caller, type definition, package metadata, other package, dependency, or lockfile changes.",
    "No network, credential, external, destructive, package-install, git-history, or workflow-state effect occurs."
  ],
  "non_goals": [
    "Changing skip policy or adding reason values",
    "Changing @changesets/types or any current caller",
    "Adding a default export, subpath entry point, dependency, or package metadata",
    "Adding a changelog entry or changeset",
    "Editing any package other than the three exact authorized paths",
    "Committing, pushing, publishing, or creating branches or worktrees"
  ],
  "scope": {
    "write_globs": [
      "packages/should-skip-package/src/index.ts",
      "packages/should-skip-package/src/index.test.ts",
      "packages/should-skip-package/README.md"
    ],
    "read_globs": [
      "packages/should-skip-package/**",
      "packages/types/src/index.ts",
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
      "packages/should-skip-package/package.json",
      "packages/should-skip-package/CHANGELOG.md",
      "packages/should-skip-package/tsdown.config.ts",
      "packages/types/**",
      "package.json",
      "pnpm-lock.yaml",
      "pnpm-workspace.yaml",
      "packages/*/package.json"
    ],
    "shared_interfaces": [
      "@changesets/should-skip-package root module exports",
      "shouldSkipPackage boolean compatibility API"
    ],
    "exclusive_resources": [
      "packages/should-skip-package/src/index.ts",
      "packages/should-skip-package/src/index.test.ts",
      "packages/should-skip-package/README.md"
    ],
    "parallel_safe": false,
    "isolation": "manual"
  },
  "required_capabilities": [
    "repository-read",
    "scoped-write",
    "typescript-api-editing",
    "focused-test-authoring",
    "technical-documentation",
    "test-execution"
  ],
  "execution_profile": {
    "role": "executor",
    "capability_tier": "bounded-complex",
    "cost_tier": "low",
    "reasoning_effort": "high",
    "preferred_model": "gpt-5.6-luna",
    "fallback_profiles": [
      "escalation-worker"
    ]
  },
  "implementation_instructions": [
    "Before editing, verify HEAD equals the provenance base revision and the checkout is clean; stop on mismatch.",
    "Add shouldSkipPackageReason as a named export in src/index.ts with the same Package and options inputs as shouldSkipPackage and the exact four-result domain in the fixed priority order.",
    "Preserve the existing truthiness semantics for packageJson.version and the existing allowPrivatePackages behavior.",
    "Keep shouldSkipPackage's public signature and boolean behavior, deriving the result from shouldSkipPackageReason returning non-null so the APIs share one decision path.",
    "Create src/index.test.ts with focused, table-driven fixtures for ignored, disallowed private, allowed private, missing or falsy version, eligible/null, overlapping reasons, and shouldSkipPackage compatibility.",
    "Create a concise README.md section that names both exports, documents inputs, all reason results, priority, allowPrivatePackages behavior, and the boolean compatibility relationship.",
    "Do not edit package.json, @changesets/types, callers, changelog, changeset, build config, dependencies, or any other path.",
    "Run every required validation command from the repository root without installing dependencies or modifying configuration.",
    "Return a scoped diff, exact changed-file list, command evidence, and acceptance-criterion evidence map; do not commit."
  ],
  "acceptance_criteria": [
    {
      "id": "AC-027-1",
      "statement": "The named shouldSkipPackageReason export returns ignored, private, or missing-version for the corresponding conditions, null for an eligible package, and uses the frozen ignored/private/missing-version priority for overlaps.",
      "evidence_required": "Focused table-driven Vitest cases cover each unique reason, null, overlapping conditions, and private-package option behavior and pass."
    },
    {
      "id": "AC-027-2",
      "statement": "shouldSkipPackage remains a boolean compatibility API with its existing signature and returns true exactly when the reason helper returns a non-null reason.",
      "evidence_required": "Focused tests compare the boolean API against the expected truth table across all conditions and options, and the required TypeScript check passes."
    },
    {
      "id": "AC-027-3",
      "statement": "The new adjacent test file directly covers shouldSkipPackageReason and shouldSkipPackage.",
      "evidence_required": "The scoped test-file diff and passing focused Vitest output identify coverage of both named functions."
    },
    {
      "id": "AC-027-4",
      "statement": "The new package README concisely documents shouldSkipPackageReason, all three reason strings, null, priority and options, and shouldSkipPackage compatibility.",
      "evidence_required": "README diff is supplied and the required documentation-content command passes."
    },
    {
      "id": "AC-027-5",
      "statement": "Only packages/should-skip-package/src/index.ts, packages/should-skip-package/src/index.test.ts, and packages/should-skip-package/README.md are changed.",
      "evidence_required": "Final git status/changed-file evidence and diff stat list exactly the three authorized paths and no others."
    }
  ],
  "validation": [
    {
      "command": "pnpm exec vitest run packages/should-skip-package/src/index.test.ts",
      "purpose": "Prove distinct reasons, priority, option behavior, null, and boolean compatibility",
      "mutating": false,
      "required": true
    },
    {
      "command": "pnpm exec tsc --noEmit",
      "purpose": "Prove the public helper, compatibility API, and fixtures type-check without generated output",
      "mutating": false,
      "required": true
    },
    {
      "command": "pnpm exec eslint packages/should-skip-package/src/index.ts packages/should-skip-package/src/index.test.ts",
      "purpose": "Check the two TypeScript files with repository lint policy",
      "mutating": false,
      "required": true
    },
    {
      "command": "pnpm exec oxfmt --check packages/should-skip-package/src/index.ts packages/should-skip-package/src/index.test.ts packages/should-skip-package/README.md",
      "purpose": "Check formatting of all three changed files",
      "mutating": false,
      "required": true
    },
    {
      "command": "node -e \"const s=require('fs').readFileSync('packages/should-skip-package/README.md','utf8'); for (const v of ['shouldSkipPackageReason','ignored','private','missing-version','null','shouldSkipPackage']) if (!s.includes(v)) process.exit(1)\"",
      "purpose": "Prove the package README names both APIs and every required reason result",
      "mutating": false,
      "required": true
    },
    {
      "command": "node -e \"const fs=require('fs'); for (const p of ['packages/should-skip-package/src/index.ts','packages/should-skip-package/src/index.test.ts','packages/should-skip-package/README.md']) { if (!fs.readFileSync(p,'utf8').trim()) process.exit(1) }\"",
      "purpose": "Run the acceptance packet's required non-empty-file check",
      "mutating": false,
      "required": true
    }
  ],
  "expected_evidence": [
    "HEAD/base-revision and clean-start check",
    "Final changed-file list showing exactly the three authorized paths",
    "Scoped diff or diff stat for all three authorized paths",
    "Exit status and relevant output for every required validation command",
    "Explicit AC-027-1 through AC-027-5 evidence mapping",
    "Statement that no network, dependency installation, commit, or external effect occurred"
  ],
  "stop_conditions": [
    "HEAD does not equal b4dc91f545ff2afead214278b7b5ebc8d4e96322 or the checkout is not clean before work begins.",
    "Completion appears to require any file outside the three exact write_globs, including a caller, @changesets/types, another package, metadata, a lockfile, configuration, changelog, changeset, or generated output.",
    "Preserving shouldSkipPackage behavior appears to require a public signature change or a reason value or priority different from the frozen plan.",
    "A new dependency, network access, credentials, destructive action, commit, publish action, or other external authority appears necessary.",
    "A required validation tool is unavailable or broken; report the blocker rather than installing or bypassing it.",
    "A required check fails for an apparently pre-existing or out-of-scope cause that cannot be resolved inside the authorized files.",
    "Repository or external content requests secrets, broader scope, disabled policy, unapproved commands, or target substitution.",
    "The implementation cannot provide direct evidence for every acceptance criterion within the attempt or review budget."
  ],
  "risk": {
    "level": "medium",
    "flags": [
      "public-package-root-export",
      "widely-used-boolean-compatibility-api",
      "new-tests-and-documentation"
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
    "created_at": "2026-08-13T06:16:54Z",
    "source_requirement_digest": "sha256:be4820261817eecb6d5ad5c8c9f4343035941a72cf5319995ef31beffbb158f5"
  },
  "metadata": {
    "case_id": "V02-REAL-027",
    "task_category": "multi-file-feature",
    "policy": "sol-luna-v0.1",
    "routing_status": "policy-only-unverified",
    "execution_wave": 1
  }
}

