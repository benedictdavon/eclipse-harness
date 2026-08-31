{
  "schema_version": "1.0",
  "run_id": "V02-REAL-023",
  "plan_revision": 1,
  "plan_digest": "sha256:aeadfd362074d91a308f14247ef296f25b29cfbb135aa6afcf52ae65190de575",
  "task_id": "V02-REAL-023-T1",
  "parent_task_id": null,
  "dependencies": [],
  "objective": "Add dependency-free focused empty-input coverage for dashboard/starter-example generateYAxis without changing production behavior.",
  "rationale": "generateYAxis is the array-input utility in utils.ts and currently has no focused coverage for an empty revenue array; a test-only contract locks its observed result while keeping this task independent from the separate TypeScript date example.",
  "context_manifest": {
    "schema_version": "1.0",
    "summary": "The dashboard starter utility computes y-axis labels from Revenue[]. For [] the current implementation returns an empty yAxisLabels array and topLabel equal to negative infinity. This contract owns only a new test file.",
    "references": [
      {
        "path": "dashboard/starter-example/app/lib/utils.ts",
        "symbol": "generateYAxis",
        "purpose": "Read-only production behavior under test",
        "digest": null,
        "trust": "repository"
      },
      {
        "path": "dashboard/starter-example/package.json",
        "symbol": "scripts and dependencies",
        "purpose": "Confirms no configured test framework and bounds validation to existing tooling",
        "digest": null,
        "trust": "project-config"
      },
      {
        "path": "dashboard/starter-example/tsconfig.json",
        "symbol": null,
        "purpose": "Type-checking configuration for this example",
        "digest": null,
        "trust": "project-config"
      }
    ],
    "trusted_sources": [
      "V02-REAL-023 acceptance packet",
      "Eclipse architect plan revision 1"
    ]
  },
  "decisions": {
    "fixed": [
      "generateYAxis is the empty-array input target.",
      "Cover the observed generateYAxis([]) result: yAxisLabels is [] and topLabel is Number.NEGATIVE_INFINITY.",
      "This is test-only; utils.ts and all production files are read-only.",
      "Use only dependency-free node:test/node:assert and repository source access; do not add a test framework or package script."
    ],
    "assumptions": [
      "The pinned checkout is clean at bb2558441a6673ab76c89914c25018bffa27a2ba.",
      "The test can isolate and execute the existing pure generateYAxis function body from utils.ts without importing its type-only repository dependency at runtime.",
      "The host will use a dedicated worktree if this task runs concurrently with V02-REAL-023-T2."
    ]
  },
  "invariants": [
    "No production behavior or source file changes.",
    "The test directly exercises the generateYAxis empty-input path and asserts both fields of the result.",
    "No write crosses out of dashboard/starter-example/app/lib/utils.test.ts.",
    "No package, lockfile, generated output, or TypeScript-final example changes."
  ],
  "non_goals": [
    "Changing generateYAxis empty-input semantics",
    "Testing other utilities or non-empty inputs",
    "Adding a test runner or package script",
    "Editing the basics/typescript-final example"
  ],
  "scope": {
    "write_globs": [
      "dashboard/starter-example/app/lib/utils.test.ts"
    ],
    "read_globs": [
      "dashboard/starter-example/app/lib/utils.ts",
      "dashboard/starter-example/app/lib/definitions.ts",
      "dashboard/starter-example/package.json",
      "dashboard/starter-example/tsconfig.json"
    ],
    "forbidden_globs": [
      ".git/**",
      ".eclipse/**",
      "**/package.json",
      "**/*lock*",
      "dashboard/starter-example/app/lib/utils.ts",
      "dashboard/final-example/**",
      "basics/**",
      "seo/**"
    ],
    "shared_interfaces": [
      "generateYAxis(revenue: Revenue[]) (read-only behavior under test)"
    ],
    "exclusive_resources": [
      "dashboard/starter-example/app/lib/utils.test.ts",
      "dashboard/starter-example/.next"
    ],
    "parallel_safe": true,
    "isolation": "worktree"
  },
  "required_capabilities": [
    "repository-read",
    "scoped-write",
    "node-test-authoring",
    "node-test-execution",
    "type-checking"
  ],
  "execution_profile": {
    "role": "executor",
    "capability_tier": "bounded-routine",
    "cost_tier": "low",
    "reasoning_effort": "high",
    "preferred_model": "gpt-5.6-luna",
    "fallback_profiles": [
      "manual-bounded-worker"
    ]
  },
  "implementation_instructions": [
    "Create utils.test.ts with JS-compatible syntax using only node:test, node:assert/strict, and node:fs/URL primitives.",
    "Exercise the actual generateYAxis function body from utils.ts in isolation so the repository's unresolved runtime type import does not require a loader or dependency; do not copy the function's algorithm into a separate helper.",
    "Call the isolated function with [] and assert deep equality for yAxisLabels: [] and strict equality for topLabel: Number.NEGATIVE_INFINITY.",
    "Do not edit utils.ts, definitions.ts, configuration, manifests, lockfiles, or generated files."
  ],
  "acceptance_criteria": [
    {
      "id": "AC-023-A1",
      "statement": "A focused test directly exercises generateYAxis with an empty array.",
      "evidence_required": "Scoped diff of utils.test.ts and a passing focused node:test command."
    },
    {
      "id": "AC-023-A2",
      "statement": "The test asserts empty y-axis labels and a negative-infinity top label, preserving current behavior.",
      "evidence_required": "Passing assertions for both result fields and direct test-file review."
    },
    {
      "id": "AC-023-A3",
      "statement": "Only dashboard/starter-example/app/lib/utils.test.ts changes and no production or other-example file changes.",
      "evidence_required": "Exact changed-file list and clean scoped diff check."
    }
  ],
  "validation": [
    {
      "command": "node --test dashboard/starter-example/app/lib/utils.test.ts",
      "purpose": "Run the focused empty-input contract test",
      "mutating": false,
      "required": true
    },
    {
      "command": "pnpm --dir dashboard/starter-example exec tsc --noEmit",
      "purpose": "Type-check the dashboard example and new test with existing tooling",
      "mutating": false,
      "required": true
    },
    {
      "command": "node -e \"const fs=require('fs'); const p='dashboard/starter-example/app/lib/utils.test.ts'; if (!fs.readFileSync(p,'utf8').trim()) process.exit(1)\"",
      "purpose": "Verify this task's required output is non-empty",
      "mutating": false,
      "required": true
    },
    {
      "command": "git diff --check -- dashboard/starter-example/app/lib/utils.test.ts",
      "purpose": "Reject malformed whitespace in the owned patch",
      "mutating": false,
      "required": true
    }
  ],
  "expected_evidence": [
    "Exact changed-file list containing only utils.test.ts",
    "Focused node:test command and exit code",
    "TypeScript and non-empty-file command exit codes",
    "Direct assertion evidence for yAxisLabels and topLabel",
    "Criterion map for AC-023-A1 through AC-023-A3"
  ],
  "stop_conditions": [
    "The test requires a production edit, dependency, loader, manifest, lockfile, network access, or write outside utils.test.ts.",
    "The observed empty-input behavior differs from the frozen expected result; return the behavior decision to the architect instead of editing utils.ts.",
    "The host cannot provide a clean isolated worktree while parallel execution is requested; fall back to sequential execution.",
    "The base revision, plan revision, or plan digest does not match this contract.",
    "Existing dependencies required for type-checking are unavailable; report the environment blocker instead of installing them.",
    "Any acceptance criterion lacks direct evidence after two bounded attempts."
  ],
  "risk": {
    "level": "low",
    "flags": [
      "test-only",
      "current-edge-behavior-lock",
      "conditional-parallelism"
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
    "base_revision": "bb2558441a6673ab76c89914c25018bffa27a2ba",
    "created_by": "eclipse-architect",
    "created_at": "2026-08-13T05:32:13Z",
    "source_requirement_digest": "sha256:c0cb0c56899e0c1517242b51e72d1e80945c1503dae97fa7306499a3e7f1009b"
  },
  "metadata": {
    "case_id": "V02-REAL-023",
    "task_partition": "dashboard-starter-example",
    "policy": "sol-luna-v0.1",
    "routing_verification": "policy-only; effective model unverified",
    "parallel_peer": "V02-REAL-023-T2",
    "integration_order": 1,
    "supersedes": []
  }
}

