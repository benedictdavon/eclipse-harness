{
  "schema_version": "1.0",
  "run_id": "v02-real-018-baseline",
  "plan_revision": 1,
  "plan_digest": "sha256:fece8bb3982cab52f299b9dffc7cc7db2bb49b33198ae43f953db1af9528b136",
  "task_id": "V02-REAL-018-T1",
  "parent_task_id": null,
  "dependencies": [],
  "objective": "Review the supplied hasSearchParameters candidate behavior, explicitly identify its string-zero and deleted-URLSearchParams-test regressions, and correct it so null is absent, the non-empty string '0' is present, and URLSearchParams deletion coverage remains, within at most two review rounds.",
  "rationale": "The candidate contains one intended null-handling change and two packet-described regressions. A single atomic source-and-test task keeps behavior and regression evidence aligned while a mandatory read-only review gate prevents accepting either regression.",
  "context_manifest": {
    "schema_version": "1.0",
    "summary": "The pinned clean TypeScript repository defines hasSearchParameters in source/utils/options.ts and exercises request/search-parameter behavior in test/main.ts. The acceptance packet describes a supplied candidate that returns false for null but incorrectly treats '0' as false and deletes URLSearchParams deletion coverage.",
    "references": [
      {
        "path": "repo/evals/v0.2/results/baseline/V02-REAL-018/packet.json",
        "symbol": null,
        "purpose": "Trusted task statement, write scope, acceptance criteria, validation, and candidate behavior description",
        "digest": "sha256:af32c21d1f8477a9040756d1513b668ec6d28a6bdacee6c230b6730aed2f3708",
        "trust": "harness"
      },
      {
        "path": "source/utils/options.ts",
        "symbol": "hasSearchParameters",
        "purpose": "Implementation target and existing string/URLSearchParams behavior",
        "digest": null,
        "trust": "repository"
      },
      {
        "path": "test/main.ts",
        "symbol": "init hook preserves merged URLSearchParams deletions",
        "purpose": "Authorized regression-test target and deletion-coverage invariant",
        "digest": null,
        "trust": "repository"
      },
      {
        "path": "source/core/Ky.ts",
        "symbol": "Ky#_retry / search parameter application call site",
        "purpose": "Read-only call-site context for hasSearchParameters",
        "digest": null,
        "trust": "repository"
      },
      {
        "path": "package.json",
        "symbol": null,
        "purpose": "Read-only project test and lint command context",
        "digest": null,
        "trust": "project-config"
      }
    ],
    "trusted_sources": [
      "V02-REAL-018 acceptance packet",
      "Eclipse task contract revision 1"
    ]
  },
  "decisions": {
    "fixed": [
      "Treat null as having no search parameters and return false without throwing.",
      "Treat the non-empty string '0' as having search parameters and return true; do not use numeric or generic truthiness coercion for strings.",
      "Preserve the deletedParametersSymbol-aware URLSearchParams behavior.",
      "Keep the existing test named 'init hook preserves merged URLSearchParams deletions' present and behaviorally meaningful.",
      "Record both packet-described candidate regressions in review evidence before acceptance.",
      "Use at most two review rounds and only the two exact authorized write paths."
    ],
    "assumptions": [
      "The supplied candidate behavior is accurately summarized by the acceptance packet even if its patch is not materialized in the clean pinned checkout.",
      "Required validation can execute with Node and Git alone; absent AVA/XO dependencies do not authorize installation or network access.",
      "The host can provide an independent read-only reviewer after the correction result is available."
    ]
  },
  "invariants": [
    "Existing handling for undefined, arrays, URLSearchParams, records, strings other than '0', and supported scalar inputs remains unchanged except where the null fix necessarily distinguishes null from objects.",
    "URLSearchParams deletion metadata remains effective even when the visible parameter set is empty.",
    "No existing regression test is deleted, skipped, weakened, or converted into a non-asserting test.",
    "The correction and its tests remain an atomic change confined to the exact authorized files."
  ],
  "non_goals": [
    "Changing SearchParamsOption or any public type.",
    "Refactoring unrelated option-merging or request construction logic.",
    "Changing dependencies, scripts, package metadata, lockfiles, documentation, or generated files.",
    "Running more than two review rounds or resolving architectural findings inside the worker task."
  ],
  "scope": {
    "write_globs": [
      "source/utils/options.ts",
      "test/main.ts"
    ],
    "read_globs": [
      "source/utils/options.ts",
      "source/utils/merge.ts",
      "source/core/Ky.ts",
      "source/types/options.ts",
      "test/main.ts",
      "package.json",
      "tsconfig.json",
      "tsconfig.dist.json"
    ],
    "forbidden_globs": [
      "package.json",
      "package-lock.json",
      "npm-shrinkwrap.json",
      "source/types/**",
      "source/core/**",
      "distribution/**",
      ".github/**",
      ".git/**"
    ],
    "shared_interfaces": [
      "hasSearchParameters runtime semantics"
    ],
    "exclusive_resources": [
      "source/utils/options.ts",
      "test/main.ts"
    ],
    "parallel_safe": false,
    "isolation": "manual"
  },
  "required_capabilities": [
    "typescript-repository-read",
    "scoped-write",
    "candidate-diff-review",
    "node-test-execution",
    "criterion-evidence-reporting"
  ],
  "execution_profile": {
    "role": "review-correction-worker",
    "capability_tier": "bounded-routine",
    "cost_tier": "low",
    "reasoning_effort": "high",
    "preferred_model": "gpt-5.6-luna",
    "fallback_profiles": [
      "eclipse_worker"
    ]
  },
  "implementation_instructions": [
    "Before editing or accepting the candidate, record a review finding that treating the non-empty string '0' as false is a regression and a second finding that deleting URLSearchParams deletion coverage is a regression. Attribute these findings to the acceptance packet; do not fabricate prior reviewer notes.",
    "Inspect the supplied candidate behavior against the pinned implementation and relevant test only; retain safe existing behavior rather than reproducing either regression.",
    "Add the smallest explicit null guard needed so hasSearchParameters(null) returns false without reaching Object.keys(null).",
    "Keep string presence based on non-empty string content so '0' returns true; do not parse, numerically coerce, or use generic Boolean conversion for string values.",
    "Preserve the deletedParametersSymbol-aware URLSearchParams branch and keep the existing 'init hook preserves merged URLSearchParams deletions' test intact and meaningful.",
    "Add focused regression assertions in test/main.ts for null returning false and string '0' returning true through observable request behavior or an equivalently direct test supported by the existing test structure.",
      "Run every required offline validation command and report command, exit status, and concise result. Map direct evidence to AC-1 through AC-5. If the host separately supplies installed repository dependencies, an AVA run may be reported as additional evidence but is not authority to install them.",
    "Submit the result to an independent read-only reviewer. Apply only bounded findings inside the existing scope, and do not exceed two total review rounds."
  ],
  "acceptance_criteria": [
    {
      "id": "AC-1",
      "statement": "Before acceptance, review evidence explicitly identifies both supplied-candidate regressions: treating the non-empty string '0' as false and deleting the URLSearchParams deletion test.",
      "evidence_required": "A dated or round-labeled review record names both regressions and distinguishes them from the intended null behavior; the independent reviewer confirms this record before acceptance."
    },
    {
      "id": "AC-2",
      "statement": "hasSearchParameters returns false for null without throwing.",
      "evidence_required": "A focused assertion in test/main.ts exercises null, and the required dependency-free Node behavior check returns false without throwing."
    },
    {
      "id": "AC-3",
      "statement": "hasSearchParameters returns true for the non-empty string '0'.",
      "evidence_required": "A focused assertion in test/main.ts exercises string '0', the required dependency-free Node behavior check returns true, and diff inspection shows no numeric or generic truthiness coercion for strings."
    },
    {
      "id": "AC-4",
      "statement": "URLSearchParams deletion coverage remains present and behaviorally meaningful.",
      "evidence_required": "Diff inspection and the required test-source check show the test named 'init hook preserves merged URLSearchParams deletions' is retained without weakening, while the required behavior check confirms deletion metadata still counts as search state."
    },
    {
      "id": "AC-5",
      "statement": "The correction is limited to source/utils/options.ts and test/main.ts and completes within at most two review rounds.",
      "evidence_required": "Changed-file evidence lists no other path, git diff --check passes, and the independent review record shows no more than two numbered review rounds."
    }
  ],
  "validation": [
    {
      "command": "node -e \"const fs=require('fs'); for (const p of ['source/utils/options.ts','test/main.ts']) { if (!fs.readFileSync(p,'utf8').trim()) process.exit(1) }\"",
      "purpose": "Run the acceptance packet's required non-empty-file validation.",
      "mutating": false,
      "required": true
    },
    {
      "command": "node -e \"const assert=require('node:assert/strict'); const source=require('node:fs').readFileSync('source/utils/options.ts','utf8'); const match=source.match(/export const hasSearchParameters = \\([^)]*\\): boolean => \\{([\\s\\S]*?)\\n\\};\\s*$/); if (!match) throw new Error('hasSearchParameters export not found'); const body=match[1].replace(/\\s+as any/g,''); const deletedParametersSymbol=Symbol('deleted'); const hasSearchParameters=new Function('search','deletedParametersSymbol',body); assert.equal(hasSearchParameters(null,deletedParametersSymbol),false); assert.equal(hasSearchParameters('0',deletedParametersSymbol),true); const deletedOnly=new URLSearchParams(); deletedOnly[deletedParametersSymbol]=new Set(['removed']); assert.equal(hasSearchParameters(deletedOnly,deletedParametersSymbol),true);\"",
      "purpose": "Execute the self-contained utility body with no installed dependencies and verify null, string-zero, and URLSearchParams deletion-metadata behavior.",
      "mutating": false,
      "required": true
    },
    {
      "command": "node -e \"const source=require('node:fs').readFileSync('test/main.ts','utf8'); if (!source.includes(\\\"test('init hook preserves merged URLSearchParams deletions'\\\")) throw new Error('URLSearchParams deletion test missing');\"",
      "purpose": "Prove the existing named URLSearchParams deletion regression test remains in the authorized test file.",
      "mutating": false,
      "required": true
    },
    {
      "command": "git diff --check -- source/utils/options.ts test/main.ts",
      "purpose": "Reject whitespace errors in the exact authorized diff.",
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
    "Pre-acceptance review record explicitly naming the string-zero and deleted-deletion-test regressions",
    "Changed-file list and concise diff summary",
    "Focused null and string-'0' test-source assertions plus passing dependency-free behavior evidence",
    "Retained 'init hook preserves merged URLSearchParams deletions' source evidence plus passing deletion-metadata behavior evidence",
    "Command, exit status, and concise output for every required validation",
    "AC-1 through AC-5 criterion-to-evidence mapping",
    "Independent reviewer verdict with numbered review round no greater than 2"
  ],
  "stop_conditions": [
    "Any acceptance criterion requires a write outside source/utils/options.ts or test/main.ts.",
    "A public type, shared interface, dependency, package script, or architecture decision must change.",
    "Existing URLSearchParams deletion semantics cannot be preserved with a bounded correction.",
    "Required Node or Git tooling is unavailable; missing optional repository dependencies do not authorize network access or installation.",
    "The independent reviewer raises an architectural, authorization, or scope finding.",
    "Any required criterion or command lacks direct passing evidence after the second review round.",
    "Credentials, network access, external effects, or destructive actions become necessary."
  ],
  "risk": {
    "level": "medium",
    "flags": [
      "supplied-candidate-regressions",
      "test-deletion-risk",
      "truthiness-edge-case",
      "mandatory-review-gate"
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
    "base_revision": "3419113b48e034fdcf8fa6bd3be3da7b3d0d758f",
    "created_by": "eclipse-architect",
    "created_at": "2026-08-13T05:05:31Z",
    "source_requirement_digest": "sha256:af32c21d1f8477a9040756d1513b668ec6d28a6bdacee6c230b6730aed2f3708"
  },
  "metadata": {
    "case_id": "V02-REAL-018",
    "case_type": "real",
    "task_category": "review-correction",
    "routing_policy": "sol-luna-v0.1",
    "routing_verification": "policy-only-unverified",
    "review_gate": "independent-read-only",
    "review_findings_source": "acceptance-packet",
    "integration_order": [
      "V02-REAL-018-T1 correction",
      "independent review",
      "bounded correction if returned",
      "final review no later than round 2"
    ]
  }
}

