{
  "schema_version": "1.0",
  "run_id": "V02-REAL-021-baseline",
  "plan_revision": 1,
  "plan_digest": "be6d616af29d42569557741711c651ec50fbcca86cb7d247c72e9e751b26ab66",
  "task_id": "V02-REAL-021-fix-empty-y-axis",
  "parent_task_id": null,
  "dependencies": [],
  "objective": "Make generateYAxis return exactly { yAxisLabels: ['$0K'], topLabel: 0 } for an empty revenue array, preserve every non-empty output, and add focused regression tests.",
  "rationale": "Math.max over an empty spread is the sole source of -Infinity. An explicit empty-array return before the existing calculation fixes the bug without altering the non-empty loop, output shape, export, imports, or other utilities.",
  "context_manifest": {
    "schema_version": "1.0",
    "summary": "One deterministic guard and one focused test file in the clean pinned dashboard starter. The app has no configured unit-test runner, so the regression test must use Node's built-in test/assert APIs and the already-declared TypeScript dependency without manifest or lockfile changes.",
    "references": [
      {
        "path": "repo/evals/v0.2/results/baseline/V02-REAL-021/packet.json",
        "symbol": null,
        "purpose": "Original bug statement, exact expected empty result, preservation requirement, write scope, and required validation.",
        "digest": "8b8c0210969386c01c0dca0df5f642a48550dcb0e022299eb6a2e61374633ea4",
        "trust": "harness"
      },
      {
        "path": "dashboard/starter-example/app/lib/utils.ts",
        "symbol": "generateYAxis",
        "purpose": "Implementation target containing the empty-spread bug and the non-empty algorithm to preserve.",
        "digest": "2e3670f6b215739427cb9316973603a99d4115109dba96317d47aed812231f80",
        "trust": "repository"
      },
      {
        "path": "dashboard/starter-example/app/lib/placeholder-data.ts",
        "symbol": "revenue",
        "purpose": "Read-only representative non-empty revenue fixture whose current $5K-to-$0K labels must remain unchanged.",
        "digest": "24a3f69adce9cbdef636278d85161623dcad04db008372f21f2f6bc9af89e670",
        "trust": "repository"
      },
      {
        "path": "dashboard/starter-example/package.json",
        "symbol": null,
        "purpose": "Read-only evidence of the declared TypeScript dependency and absence of a unit-test script.",
        "digest": "e5cdd822022c1340da463cb8d78842814de80d6b4482b803a318c4fd7dc4ac4e",
        "trust": "project-config"
      },
      {
        "path": "dashboard/starter-example/tsconfig.json",
        "symbol": null,
        "purpose": "Read-only strict TypeScript project configuration for the implementation and new test.",
        "digest": "4e6268d243a233e8ce945a54703bbe002dd71ebf183ff285a8b3b1a551c9ce0c",
        "trust": "project-config"
      }
    ],
    "trusted_sources": [
      "Frozen architect prompt",
      "eclipse-orchestrate skill and task-contract schema",
      "V02-REAL-021 acceptance packet"
    ]
  },
  "decisions": {
    "fixed": [
      "When revenue.length is 0, return a fresh object exactly equal to { yAxisLabels: ['$0K'], topLabel: 0 } before calling Math.max.",
      "For every non-empty Revenue[] input, retain the existing highest-record, ceiling-to-next-thousand, descending-label-loop, object key names, and output ordering behavior.",
      "Preserve the generateYAxis named export and Revenue[] parameter contract.",
      "Do not refactor formatCurrency, formatDateToLocal, generatePagination, or shared type definitions.",
      "Create utils.test.ts as a focused Node built-in test entrypoint that executes the real generateYAxis implementation by transpiling utils.ts in memory with the already-declared TypeScript dependency; add no runner, loader, dependency, or package script."
    ],
    "assumptions": [
      "Revenue values for non-empty inputs continue to follow the existing data contract; negative, NaN, and infinite revenues are outside this bug fix.",
      "A direct early guard is sufficient and preferable to introducing an initial value into Math.max because it states the exact empty result without perturbing the non-empty path.",
      "Configured routing is policy-only; effective model identity, permissions, and cost are unverified by trusted host metadata."
    ]
  },
  "invariants": [
    "A non-empty input with maximum revenue 4800 returns topLabel 5000 and labels ['$5K', '$4K', '$3K', '$2K', '$1K', '$0K'].",
    "A non-empty input whose maximum is an exact thousand retains that exact topLabel rather than adding another thousand.",
    "generateYAxis does not mutate the revenue array or its entries.",
    "The returned object continues to contain only yAxisLabels and topLabel in the established shape.",
    "All utility exports other than the empty-input branch of generateYAxis remain unchanged.",
    "The pinned base revision remains bb2558441a6673ab76c89914c25018bffa27a2ba."
  ],
  "non_goals": [
    "Changing label formatting, step size, rounding, top-label calculation, or descending order for non-empty input.",
    "Defining new behavior for negative, NaN, infinite, sparse, null, undefined, or non-array input.",
    "Refactoring generateYAxis beyond the explicit empty guard.",
    "Changing Revenue types, fixtures, chart components, pagination, currency/date helpers, or final-example code.",
    "Adding dependencies, package scripts, test configuration, loader configuration, snapshots, or lockfile changes."
  ],
  "scope": {
    "write_globs": [
      "dashboard/starter-example/app/lib/utils.ts",
      "dashboard/starter-example/app/lib/utils.test.ts"
    ],
    "read_globs": [
      "dashboard/starter-example/app/lib/utils.ts",
      "dashboard/starter-example/app/lib/definitions.ts",
      "dashboard/starter-example/app/lib/placeholder-data.ts",
      "dashboard/starter-example/app/ui/dashboard/revenue-chart.tsx",
      "dashboard/starter-example/package.json",
      "dashboard/starter-example/pnpm-lock.yaml",
      "dashboard/starter-example/tsconfig.json"
    ],
    "forbidden_globs": [
      ".git/**",
      ".github/**",
      "dashboard/starter-example/package.json",
      "dashboard/starter-example/pnpm-lock.yaml",
      "dashboard/starter-example/pnpm-workspace.yaml",
      "dashboard/starter-example/tsconfig.json",
      "dashboard/starter-example/app/lib/definitions.ts",
      "dashboard/starter-example/app/lib/placeholder-data.ts",
      "dashboard/starter-example/app/ui/**",
      "dashboard/final-example/**",
      "basics/**",
      "seo/**",
      "**/.env*"
    ],
    "shared_interfaces": [
      "generateYAxis export, input contract, and return shape"
    ],
    "exclusive_resources": [
      "dashboard/starter-example/app/lib/utils.ts",
      "dashboard/starter-example/app/lib/utils.test.ts"
    ],
    "parallel_safe": false,
    "isolation": "branch"
  },
  "required_capabilities": [
    "bounded TypeScript bug fixing",
    "empty-collection boundary reasoning",
    "Node built-in regression testing",
    "strict scoped-write discipline",
    "criterion evidence reporting"
  ],
  "execution_profile": {
    "role": "worker",
    "capability_tier": "tiny-deterministic-implementation",
    "cost_tier": "low",
    "reasoning_effort": "medium",
    "preferred_model": "luna",
    "fallback_profiles": [
      "luna-high-for-concrete-local-test-harness-blocker",
      "architect-escalation-for-semantics-or-scope-change"
    ]
  },
  "implementation_instructions": [
    "At the start of generateYAxis, add an explicit revenue.length === 0 guard returning { yAxisLabels: ['$0K'], topLabel: 0 }.",
    "Leave the existing Math.max calculation, topLabel expression, descending loop, return statement, export name, parameter type, and all neighboring utilities unchanged for non-empty input.",
    "Create utils.test.ts as a Node built-in test entrypoint written so Node can execute it without a new loader. It may transpile the sibling utils.ts in memory with the project's declared TypeScript dependency, but must call the real exported generateYAxis rather than a copied function body.",
    "Assert deep exact equality for empty input. Add exact non-empty regression cases for a maximum on a thousand boundary and a non-boundary maximum; include the existing fixture-equivalent 4800 maximum and full $5K-through-$0K labels.",
    "Do not weaken tests to checking only finiteness, array length, or membership, and do not add behavior for input classes outside the stated assumptions.",
    "Run every required validation, report exit status and concise output, and map direct evidence to AC-01 through AC-04."
  ],
  "acceptance_criteria": [
    {
      "id": "AC-01",
      "statement": "generateYAxis([]) returns exactly { yAxisLabels: ['$0K'], topLabel: 0 } and no -Infinity value.",
      "evidence_required": "Implementation diff showing the explicit pre-Math.max guard plus a passing deep-equality regression assertion for the exact object."
    },
    {
      "id": "AC-02",
      "statement": "Every non-empty input continues through the unchanged existing algorithm and preserves topLabel and label arrays.",
      "evidence_required": "Minimal source diff confined to the empty guard plus passing exact assertions for an exact-thousand maximum, a non-boundary maximum, and the 4800-to-$5K fixture case."
    },
    {
      "id": "AC-03",
      "statement": "A focused executable utils.test.ts regression file covers the empty failure and representative non-empty behavior by invoking the real exported function.",
      "evidence_required": "Test-file diff and successful Node built-in test command output with all focused cases passing."
    },
    {
      "id": "AC-04",
      "statement": "The generateYAxis export/signature and all unrelated utilities remain unchanged, and only utils.ts and utils.test.ts are modified.",
      "evidence_required": "Diff inspection, git diff --name-only limited to the two authorized paths, a passing TypeScript check, and clean git diff --check output."
    }
  ],
  "validation": [
    {
      "command": "node -e \"const fs=require('fs'); for (const p of ['dashboard/starter-example/app/lib/utils.ts','dashboard/starter-example/app/lib/utils.test.ts']) { if (!fs.readFileSync(p,'utf8').trim()) process.exit(1) }\"",
      "purpose": "Run the packet-mandated non-empty implementation-and-test validation exactly.",
      "mutating": false,
      "required": true
    },
    {
      "command": "pnpm --dir dashboard/starter-example exec node --test app/lib/utils.test.ts",
      "purpose": "Run focused exact regression assertions against the real generateYAxis export without adding a test runner.",
      "mutating": false,
      "required": true
    },
    {
      "command": "pnpm --dir dashboard/starter-example exec tsc --noEmit --incremental false --project tsconfig.json",
      "purpose": "Type-check the utility and new regression test without generating incremental output.",
      "mutating": false,
      "required": true
    },
    {
      "command": "git diff --check -- dashboard/starter-example/app/lib/utils.ts dashboard/starter-example/app/lib/utils.test.ts",
      "purpose": "Reject whitespace errors in the exact authorized patch.",
      "mutating": false,
      "required": true
    },
    {
      "command": "git diff --name-only",
      "purpose": "Prove the changed-file set is confined to the two authorized paths.",
      "mutating": false,
      "required": true
    }
  ],
  "expected_evidence": [
    "Base revision and pre-work git status.",
    "Exact changed-file list and concise diff summary.",
    "The minimal empty-guard diff and focused exact-output test diff.",
    "Command, exit status, and concise output for every required validation.",
    "A criterion-by-criterion mapping for AC-01 through AC-04.",
    "Any unavailable local dependency or unverified routing/permission assumption explicitly labeled."
  ],
  "stop_conditions": [
    "HEAD is not bb2558441a6673ab76c89914c25018bffa27a2ba or either authorized path has overlapping pre-existing changes.",
    "The fix or focused test appears to require a write outside utils.ts and utils.test.ts.",
    "Preserving non-empty behavior would require changing the existing calculation, loop, output shape, export, or Revenue type.",
    "A package manifest, lockfile, TypeScript configuration, chart consumer, fixture, dependency, runner, or loader change appears necessary.",
    "The focused test cannot execute the real function with already-declared local dependencies; do not install packages or enable network access.",
    "Required tools or dependencies are unavailable, an unrelated baseline failure cannot be separated, or any criterion lacks direct evidence after the attempt budget.",
    "Credentials, external effects, destructive actions, generated-file changes, or outbound network access become necessary."
  ],
  "risk": {
    "level": "low",
    "flags": [
      "empty-array-boundary",
      "non-empty-output-must-remain-identical",
      "no-configured-test-runner"
    ]
  },
  "complexity": "bounded",
  "budgets": {
    "max_attempts": 2,
    "max_review_rounds": 1
  },
  "authorization": {
    "network": false,
    "credentials": false,
    "external_side_effects": false,
    "destructive_actions": false,
    "targets": [
      "dashboard/starter-example/app/lib/utils.ts",
      "dashboard/starter-example/app/lib/utils.test.ts"
    ]
  },
  "provenance": {
    "base_revision": "bb2558441a6673ab76c89914c25018bffa27a2ba",
    "created_by": "baseline-eclipse-architect",
    "created_at": "2026-08-13T05:32:47Z",
    "source_requirement_digest": "8b8c0210969386c01c0dca0df5f642a48550dcb0e022299eb6a2e61374633ea4"
  },
  "metadata": {
    "case_id": "V02-REAL-021",
    "case_type": "real",
    "task_category": "bug-diagnosis-fix",
    "policy": "sol-luna-v0.1",
    "route_verification": "unverified-policy-only",
    "plan_digest_basis": "SHA-256 of canonical JSON containing base_revision, plan_revision, run_id, source_requirement_digest, and ordered task_ids",
    "integration_order": [
      "V02-REAL-021-fix-empty-y-axis implementation and focused regression tests",
      "read-only acceptance review"
    ]
  }
}

