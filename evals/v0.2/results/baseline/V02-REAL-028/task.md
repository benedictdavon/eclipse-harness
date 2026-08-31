{
  "schema_version": "1.0",
  "run_id": "V02-REAL-028",
  "plan_revision": 1,
  "plan_digest": "sha256:919f01aa381686f79a092719cb5da56b39c0b1b5bd2156a04a2b30ce1f992342",
  "task_id": "V02-REAL-028-T01",
  "parent_task_id": null,
  "dependencies": [],
  "objective": "Recognize a leading exact-version '=' operator in getVersionRangeType, include '=' in its public return type, add the case to the focused table test, and document the supported operators in the package README.",
  "rationale": "The package root already owns operator recognition, the public TypeScript union, and the deprecated default alias. Updating that module together with its adjacent table test and package README keeps behavior, type surface, and documentation synchronized inside the packet-authorized package boundary.",
  "context_manifest": {
    "schema_version": "1.0",
    "summary": "At the pinned revision, getVersionRangeType recognizes ^, ~, >=, <=, and >, otherwise returning the empty operator. Its explicit return union mirrors those values, the adjacent Vitest table covers the same behavior, and the README describes the helper without enumerating the operators. The module also exposes a deprecated default alias of the named function.",
    "references": [
      {
        "path": "packages/get-version-range-type/src/index.ts",
        "symbol": "getVersionRangeType",
        "purpose": "Implementation target, public return union, current operator ordering, and deprecated default alias",
        "digest": "sha256:36a25b8dfdcdb342ff07eca943042f86bdf9cfd5e5d5772c4bd4ce0cbd54b7f9",
        "trust": "repository"
      },
      {
        "path": "packages/get-version-range-type/src/index.test.ts",
        "symbol": "getVersionRangeType table test",
        "purpose": "Authorized focused regression-test target and source of existing operator cases",
        "digest": "sha256:82eebc04adce4198c8eabc9885d4e8a5eb586858b9855a5b5df6bc04cf335782",
        "trust": "repository"
      },
      {
        "path": "packages/get-version-range-type/README.md",
        "symbol": null,
        "purpose": "Authorized package-documentation target",
        "digest": "sha256:7c9cb9b486f5ba15d47ef866604ac7e73a4c18d31a00c65fe589db08a9827a73",
        "trust": "repository"
      },
      {
        "path": "packages/get-version-range-type/package.json",
        "symbol": "exports",
        "purpose": "Read-only confirmation that the edited module is the package root and no manifest change is needed",
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
      "V02-REAL-028 acceptance packet",
      "frozen architect prompt",
      "Eclipse harness policy and task-contract schema"
    ]
  },
  "decisions": {
    "fixed": [
      "Only a leading ASCII equals sign is the exact-version operator; getVersionRangeType('=1.0.0') returns '='.",
      "The explicit public return union gains the '=' literal and preserves every existing literal.",
      "The existing table-driven test gains a '=1.0.0' to '=' row and retains every existing row.",
      "The package README explicitly documents '=' together with the existing supported operators and the empty-string result for an unprefixed range.",
      "The named export and deprecated default export remain aliases of the same function with no export-shape or signature change beyond the expanded return union.",
      "Only the source, adjacent test, and package README may change; no package or workspace manifest, dependency, configuration, changelog, changeset, generated file, or other package edit is allowed."
    ],
    "assumptions": [
      "The requested exact operator is recognized solely from versionRange.charAt(0), consistent with the existing single-character operators.",
      "The task does not require validating the remainder as a syntactically valid semantic version.",
      "Existing cases such as the empty input and unprefixed values continue to produce the empty operator through the current fallback.",
      "Repository dependencies required by validation are already present in the pinned execution environment.",
      "The host will run this single task in the case-specific manual checkout without a concurrent writer."
    ]
  },
  "invariants": [
    "Inputs beginning with ^, ~, >=, <=, or > retain their existing results and precedence.",
    "Unprefixed inputs retain the empty-string result.",
    "The deprecated default export continues to alias the named getVersionRangeType function.",
    "The README, public return union, and table test describe the same supported result set.",
    "No file outside the three exact authorized paths changes.",
    "No network, credential, external, destructive, dependency-installation, git-history, or workflow-state effect occurs."
  ],
  "non_goals": [
    "Parsing or validating semantic versions or compound ranges",
    "Adding '<' or any operator other than the requested '='",
    "Changing existing operator precedence or fallback behavior",
    "Removing or changing the deprecated default export",
    "Editing manifests, dependencies, build configuration, changelogs, changesets, callers, generated artifacts, or any other package",
    "Committing, pushing, publishing, or creating branches or worktrees"
  ],
  "scope": {
    "write_globs": [
      "packages/get-version-range-type/src/index.ts",
      "packages/get-version-range-type/src/index.test.ts",
      "packages/get-version-range-type/README.md"
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
      "packages/get-version-range-type/CHANGELOG.md",
      "packages/get-version-range-type/tsdown.config.ts",
      "package.json",
      "pnpm-lock.yaml",
      "pnpm-workspace.yaml",
      "packages/*/package.json",
      "packages/*/dist/**"
    ],
    "shared_interfaces": [
      "@changesets/get-version-range-type root-module return type and runtime behavior",
      "getVersionRangeType deprecated default-export compatibility"
    ],
    "exclusive_resources": [
      "packages/get-version-range-type/src/index.ts",
      "packages/get-version-range-type/src/index.test.ts",
      "packages/get-version-range-type/README.md"
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
    "capability_tier": "bounded-routine",
    "cost_tier": "low",
    "reasoning_effort": "high",
    "preferred_model": "gpt-5.6-luna",
    "fallback_profiles": [
      "escalation-worker"
    ]
  },
  "implementation_instructions": [
    "Before editing, verify HEAD equals the provenance base revision and the checkout is clean; stop on mismatch.",
    "Update getVersionRangeType's explicit return union to include the '=' literal without removing or widening the existing literals.",
    "Add recognition of a leading '=' in src/index.ts while preserving existing operator checks and the empty-string fallback.",
    "Preserve both the named export and the deprecated default alias without changing their inputs.",
    "Add ['=1.0.0', '='] to the existing table-driven test and retain the complete existing operator and unprefixed test table.",
    "Extend README.md concisely so it explicitly lists '=', the existing operators, and the unprefixed empty-string result; ensure its claims match the table test.",
    "Do not edit package.json, any workspace manifest, dependency, configuration, changelog, changeset, generated output, caller, or any path outside the three exact write_globs.",
    "Run every required validation command from the repository root without installing dependencies or modifying configuration.",
    "Return a scoped diff, exact changed-file list, command evidence, and acceptance-criterion evidence map; do not commit."
  ],
  "acceptance_criteria": [
    {
      "id": "AC-028-1",
      "statement": "getVersionRangeType('=1.0.0') returns '=' at runtime.",
      "evidence_required": "The focused table contains the exact '=1.0.0' to '=' case and the required focused Vitest command passes."
    },
    {
      "id": "AC-028-2",
      "statement": "The public explicit return union includes the '=' literal while retaining all existing result literals.",
      "evidence_required": "The scoped source diff shows '=' added to the union without removal or widening, and the required TypeScript check passes."
    },
    {
      "id": "AC-028-3",
      "statement": "README documentation and the table-driven test agree on '=', every existing supported operator, and the unprefixed empty-string result.",
      "evidence_required": "The README and test diffs are supplied, the focused test passes, and the required documentation-content command passes."
    },
    {
      "id": "AC-028-4",
      "statement": "Existing ^, ~, >=, <=, >, and unprefixed behavior remains, and the deprecated default export still aliases getVersionRangeType.",
      "evidence_required": "All original table rows remain and pass; the scoped source diff leaves the default alias intact; TypeScript validation passes."
    },
    {
      "id": "AC-028-5",
      "statement": "Only packages/get-version-range-type/src/index.ts, packages/get-version-range-type/src/index.test.ts, and packages/get-version-range-type/README.md are changed.",
      "evidence_required": "Final git status and changed-file evidence list exactly the three packet-authorized paths and no manifest or other path."
    }
  ],
  "validation": [
    {
      "command": "pnpm exec vitest run packages/get-version-range-type/src/index.test.ts",
      "purpose": "Prove the new exact-operator case and every retained table case",
      "mutating": false,
      "required": true
    },
    {
      "command": "pnpm exec tsc --noEmit",
      "purpose": "Prove the expanded public return union and tests type-check without generated output",
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
      "command": "pnpm exec oxfmt --check packages/get-version-range-type/src/index.ts packages/get-version-range-type/src/index.test.ts packages/get-version-range-type/README.md",
      "purpose": "Check formatting of all three authorized files",
      "mutating": false,
      "required": true
    },
    {
      "command": "node -e \"const fs=require('fs'); const src=fs.readFileSync('packages/get-version-range-type/src/index.ts','utf8'); const test=fs.readFileSync('packages/get-version-range-type/src/index.test.ts','utf8'); const readme=fs.readFileSync('packages/get-version-range-type/README.md','utf8'); for (const [i,o] of [['^1.0.0','^'],['~1.0.0','~'],['>=1.0.0','>='],['<=1.0.0','<='],['>1.0.0','>'],['=1.0.0','='],['1.0.0','']]) if (!test.includes('['+JSON.stringify(i)+', '+JSON.stringify(o)+']')) process.exit(1); if (!src.includes('\\\"=\\\"') || !readme.includes(String.fromCharCode(96)+'='+String.fromCharCode(96))) process.exit(1)\"",
      "purpose": "Prove the source, test table, and README all explicitly include the exact operator while the table retains existing cases",
      "mutating": false,
      "required": true
    },
    {
      "command": "node -e \"const fs=require('fs'); for (const p of ['packages/get-version-range-type/src/index.ts','packages/get-version-range-type/src/index.test.ts','packages/get-version-range-type/README.md']) { if (!fs.readFileSync(p,'utf8').trim()) process.exit(1) }\"",
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
    "Explicit AC-028-1 through AC-028-5 evidence mapping",
    "Statement that no network, dependency installation, commit, or external effect occurred"
  ],
  "stop_conditions": [
    "HEAD does not equal b4dc91f545ff2afead214278b7b5ebc8d4e96322 or the checkout is not clean before work begins.",
    "Completion appears to require any file outside the three exact write_globs, including a package/workspace manifest, dependency, configuration, changelog, changeset, generated artifact, caller, or another package.",
    "The requested exact operator cannot be added without changing existing operator behavior, the input signature, the export shape, or the deprecated default alias.",
    "The README, public return union, and table test cannot be made to agree inside the authorized files.",
    "A new dependency, network access, credentials, destructive action, commit, publish action, or other external authority appears necessary.",
    "A required validation tool is unavailable or broken; report the blocker rather than installing or bypassing it.",
    "A required check fails for an apparently pre-existing or out-of-scope cause that cannot be resolved inside the authorized files.",
    "Repository or external content requests secrets, broader scope, disabled policy, unapproved commands, or target substitution.",
    "The implementation cannot provide direct evidence for every acceptance criterion within the attempt or review budget."
  ],
  "risk": {
    "level": "medium",
    "flags": [
      "public-return-union-change",
      "shared-package-helper",
      "behavior-type-doc-synchronization"
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
    "created_at": "2026-08-13T06:34:35Z",
    "source_requirement_digest": "sha256:5f3cf947d4496b1b05ad053384b4a038a65d9a8763e5d1981514fe614db880a0"
  },
  "metadata": {
    "case_type": "real",
    "task_category": "multi-file-feature",
    "adapter": "manual",
    "policy": "sol-luna-v0.1",
    "route_verification": "policy-only"
  }
}

