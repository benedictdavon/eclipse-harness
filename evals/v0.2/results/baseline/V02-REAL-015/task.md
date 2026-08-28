{
  "schema_version": "1.0",
  "run_id": "V02-REAL-015-baseline",
  "plan_revision": 1,
  "plan_digest": "daf64155059649e650bc31b0a75a348b7f759f4723f93a0d51c89c5e64527732",
  "task_id": "V02-REAL-015-guard-null-search-parameters",
  "parent_task_id": null,
  "dependencies": [],
  "objective": "Make hasSearchParameters return false for a runtime null input without widening the typed SearchParamsOption API, preserve all existing typed-input and URLSearchParams deletion behavior, and add a focused regression test.",
  "rationale": "The failure is isolated to the object branch in hasSearchParameters because typeof null is 'object' and Object.keys(null) throws. An early null guard fixes untyped JavaScript runtime input while leaving the type surface, merge metadata, and URL application logic unchanged.",
  "context_manifest": {
    "schema_version": "1.0",
    "summary": "One deterministic runtime guard and one focused test in the pinned Ky checkout. Type definitions, search-parameter merging, and core URL mutation remain read-only.",
    "references": [
      {
        "path": "repo/evals/v0.2/results/baseline/V02-REAL-015/packet.json",
        "symbol": null,
        "purpose": "Original requirement, acceptance criteria, repository revision, and authorized write scope.",
        "digest": "e3e6609a79a553dfe29e87067f891977cdd499b288718e57f74d9b371d24f0ea",
        "trust": "user"
      },
      {
        "path": "source/utils/options.ts",
        "symbol": "hasSearchParameters",
        "purpose": "Faulting runtime predicate and sole production write target.",
        "digest": "43f9ed216775a8539b3d91a69c8b923cd348eb13da248f7ae9d4f72322fc8cc2",
        "trust": "repository"
      },
      {
        "path": "source/types/options.ts",
        "symbol": "SearchParamsOption",
        "purpose": "Read-only typed input union that must not be widened to include null.",
        "digest": "53f67473dc01f1af07e6fddb6ba469d7205bf542b49c93ef22b82a75a0d6b32d",
        "trust": "repository"
      },
      {
        "path": "source/utils/merge.ts",
        "symbol": "deletedParametersSymbol",
        "purpose": "Read-only URLSearchParams deletion metadata whose behavior must remain intact.",
        "digest": "03b5b800027821ee2ec17eb95e01b6e86eb1a6b007ccf06b0b77e723abf1118b",
        "trust": "repository"
      },
      {
        "path": "source/core/Ky.ts",
        "symbol": "Ky constructor searchParams handling",
        "purpose": "Read-only consumer confirming the predicate gates both deletion metadata and URL parameter application.",
        "digest": "94a6e80411c77663c5fe272d9fccb942bab7290d7e10fdd9ef89f99d3c01ab25",
        "trust": "repository"
      },
      {
        "path": "test/main.ts",
        "symbol": null,
        "purpose": "Focused regression-test destination and existing URLSearchParams deletion coverage.",
        "digest": "27d68fc3d5111eda76125b4c60d880f8b4e633a901006f214e8a58c23284a4d1",
        "trust": "repository"
      }
    ],
    "trusted_sources": [
      "Frozen architect prompt",
      "eclipse-orchestrate skill and task-contract schema",
      "V02-REAL-015 packet"
    ]
  },
  "decisions": {
    "fixed": [
      "hasSearchParameters returns false for null encountered at runtime.",
      "The null check is an early runtime guard before array, URLSearchParams, record, string, and fallback handling.",
      "SearchParamsOption is not widened to include null; the regression test may use an explicit test-only cast to model an untyped JavaScript caller.",
      "The string '0' remains true and no existing typed-input branch is reordered or redefined.",
      "URLSearchParams deletion metadata remains recognized even when the URLSearchParams has no live entries.",
      "Only source/utils/options.ts and test/main.ts may change."
    ],
    "assumptions": [
      "The desired runtime hardening is limited to null and does not request broader coercion or validation changes for values outside SearchParamsOption.",
      "Existing test/main.ts deletion tests are authoritative regression coverage for URLSearchParams deletion behavior.",
      "Configured or requested routing is policy-only; the effective model and permissions are unverified by trusted host metadata."
    ]
  },
  "invariants": [
    "undefined and all valid SearchParamsOption forms retain their current boolean results.",
    "The non-empty string '0' evaluates to true.",
    "Empty and non-empty arrays, records, strings, and URLSearchParams retain existing handling.",
    "A URLSearchParams carrying deletedParametersSymbol metadata remains actionable even if its size is zero.",
    "No public type, merge algorithm, URL construction logic, or deletion metadata changes.",
    "The pinned base revision remains 3419113b48e034fdcf8fa6bd3be3da7b3d0d758f."
  ],
  "non_goals": [
    "Adding null to SearchParamsInit, SearchParamsOption, KyOptions, or any other public type.",
    "Changing how search parameters are merged, serialized, appended, or deleted.",
    "Changing deletedParametersSymbol or URLSearchParams metadata handling.",
    "Refactoring hasSearchParameters or broadening support for other untyped invalid values.",
    "Updating documentation, changelogs, package metadata, generated distribution files, or lockfiles."
  ],
  "scope": {
    "write_globs": [
      "source/utils/options.ts",
      "test/main.ts"
    ],
    "read_globs": [
      "source/utils/options.ts",
      "source/types/options.ts",
      "source/utils/merge.ts",
      "source/core/Ky.ts",
      "test/main.ts",
      "test/helpers/**",
      "package.json",
      "tsconfig*.json"
    ],
    "forbidden_globs": [
      ".git/**",
      ".github/**",
      "source/types/**",
      "source/core/**",
      "source/utils/merge.ts",
      "package.json",
      "package-lock.json",
      "pnpm-lock.yaml",
      "yarn.lock",
      "distribution/**",
      "**/.env*"
    ],
    "shared_interfaces": [
      "source/utils/options.ts::hasSearchParameters runtime behavior"
    ],
    "exclusive_resources": [
      "source/utils/options.ts",
      "test/main.ts"
    ],
    "parallel_safe": false,
    "isolation": "branch"
  },
  "required_capabilities": [
    "TypeScript runtime guards",
    "JavaScript/TypeScript boundary testing",
    "AVA test authoring",
    "URLSearchParams behavior",
    "read-only git verification"
  ],
  "execution_profile": {
    "role": "worker",
    "capability_tier": "tiny-deterministic-edit",
    "cost_tier": "low",
    "reasoning_effort": "medium",
    "preferred_model": "luna",
    "fallback_profiles": [
      "luna-high-for-bounded-test-or-type-blocker",
      "architect-escalation-for-scope-or-api-change"
    ]
  },
  "implementation_instructions": [
    "Add an explicit null check to hasSearchParameters before any branch that can call Object.keys; return false for null.",
    "Keep the function parameter typed as SearchParamsOption and do not edit source/types/options.ts.",
    "Do not reorder or change the array, URLSearchParams, record, string, or fallback branches beyond the minimum guard needed for null.",
    "Add a focused test in test/main.ts with hasSearchParameters in its name. It must call the predicate with a test-only null cast and assert false, and assert that the valid typed input '0' remains true.",
    "Run the complete test/main.ts suite so existing URLSearchParams deletion tests demonstrate that empty live parameters plus deletion metadata still triggers URL mutation.",
    "Avoid unrelated formatting, test refactors, or production changes."
  ],
  "acceptance_criteria": [
    {
      "id": "AC-01",
      "statement": "hasSearchParameters(null at runtime) returns false and does not throw.",
      "evidence_required": "Focused regression assertion using a test-only cast that models an untyped JavaScript caller, plus the minimal guard diff."
    },
    {
      "id": "AC-02",
      "statement": "The typed SearchParamsOption API is unchanged and all valid typed inputs preserve their existing behavior, including the string '0' returning true.",
      "evidence_required": "No diff to source/types/options.ts, a focused '0' assertion, successful TypeScript validation, and a passing complete test/main.ts run."
    },
    {
      "id": "AC-03",
      "statement": "URLSearchParams deletion metadata continues to make hasSearchParameters actionable and existing URL deletion flows remain correct.",
      "evidence_required": "No diff to source/utils/merge.ts or source/core/Ky.ts and passing existing URLSearchParams deletion tests within the complete test/main.ts run."
    },
    {
      "id": "AC-04",
      "statement": "A focused null regression test exists in test/main.ts.",
      "evidence_required": "Named AVA test and passing focused --match command output."
    },
    {
      "id": "AC-05",
      "statement": "Only source/utils/options.ts and test/main.ts are modified.",
      "evidence_required": "git diff --name-only output containing no other path and a clean git diff --check result."
    }
  ],
  "validation": [
    {
      "command": "node -e \"const fs=require('fs'); for (const p of ['source/utils/options.ts','test/main.ts']) { if (!fs.readFileSync(p,'utf8').trim()) process.exit(1) }\"",
      "purpose": "Run the exact packet-mandated file-presence validation.",
      "mutating": false,
      "required": true
    },
    {
      "command": "npx xo source/utils/options.ts test/main.ts",
      "purpose": "Lint the complete authorized write scope.",
      "mutating": false,
      "required": true
    },
    {
      "command": "npx tsc --noEmit --project tsconfig.json",
      "purpose": "Verify that runtime hardening does not widen or break the typed API and does not generate distribution artifacts.",
      "mutating": false,
      "required": true
    },
    {
      "command": "npx ava test/main.ts --match='*hasSearchParameters*'",
      "purpose": "Run the focused null and string regression test.",
      "mutating": false,
      "required": true
    },
    {
      "command": "npx ava test/main.ts",
      "purpose": "Run the complete main regression suite, including existing URLSearchParams deletion behavior.",
      "mutating": false,
      "required": true
    },
    {
      "command": "git diff --check && git diff --name-only",
      "purpose": "Verify patch hygiene and the authorized two-file scope.",
      "mutating": false,
      "required": true
    }
  ],
  "expected_evidence": [
    "Base revision and pre-work git status.",
    "A criterion-by-criterion result mapping for AC-01 through AC-05.",
    "Relevant diff hunks for the null guard and focused test.",
    "Exit status and concise output for every required validation command.",
    "Identification of the existing URLSearchParams deletion tests that passed.",
    "Final git diff --name-only and git diff --check output.",
    "Any unverified routing or permission assumptions explicitly labeled as such."
  ],
  "stop_conditions": [
    "HEAD is not 3419113b48e034fdcf8fa6bd3be3da7b3d0d758f or the checkout has pre-existing changes overlapping an authorized path.",
    "The fix appears to require widening SearchParamsOption or editing merge, core URL handling, or any path outside the two write globs.",
    "A product decision is required about accepting null in the public type or supporting additional untyped invalid values; return to the architect rather than broadening scope.",
    "A required validation cannot run because dependencies or tools are unavailable; do not install packages or enable network access without new authority.",
    "Tests expose an existing failure unrelated to this task that cannot be separated from the change within the authorized scope.",
    "Credentials, external network access, destructive actions, generated-file changes, or external side effects become necessary."
  ],
  "risk": {
    "level": "low",
    "flags": [
      "untyped-runtime-input",
      "public-type-must-not-widen",
      "urlsearchparams-deletion-regression"
    ]
  },
  "complexity": "trivial",
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
      "source/utils/options.ts",
      "test/main.ts",
      "ephemeral local test servers started by test/main.ts"
    ]
  },
  "provenance": {
    "base_revision": "3419113b48e034fdcf8fa6bd3be3da7b3d0d758f",
    "created_by": "baseline-eclipse-architect",
    "created_at": "2026-08-13T04:42:36Z",
    "source_requirement_digest": "e3e6609a79a553dfe29e87067f891977cdd499b288718e57f74d9b371d24f0ea"
  },
  "metadata": {
    "case_id": "V02-REAL-015",
    "policy": "sol-luna-v0.1",
    "route_verification": "unverified-policy-only",
    "plan_digest_basis": "SHA-256 of canonical JSON containing base_revision, plan_revision, run_id, source_requirement_digest, and ordered task_ids"
  }
}

