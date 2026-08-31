```json
{
  "schema_version": "1.0",
  "run_id": "V02-REAL-015",
  "plan_revision": 1,
  "plan_digest": "sha256:35dabe163d2790ae148aaa5485a244c6128c3dfd07ae6264bf8e6f8c380428b6",
  "task_id": "V02-REAL-015-T1",
  "dependencies": [],
  "objective": "Make hasSearchParameters return false for runtime null, retain all typed-input behavior including string '0', and preserve URLSearchParams deletion semantics with a focused regression test.",
  "rationale": "A null-specific early return prevents Object.keys(null) while leaving every typed branch and the deletion marker branch intact.",
  "context_manifest": {
    "schema_version": "1.0",
    "summary": "hasSearchParameters handles undefined, arrays, URLSearchParams including deletedParametersSymbol, records, strings, then Boolean fallback. Null enters the record branch and throws. test/main.ts contains extensive searchParams merge/deletion tests.",
    "references": [
      {"path": "source/utils/options.ts", "symbol": "hasSearchParameters", "purpose": "Extend only the early empty guard to null.", "digest": null, "trust": "repository"},
      {"path": "test/main.ts", "symbol": "searchParams tests", "purpose": "Add direct runtime null and '0' regression while retaining deletion integration tests.", "digest": null, "trust": "repository"}
    ],
    "trusted_sources": ["/workspace/scratch/473866e9940e/repo/evals/v0.2/results/v0.2/V02-REAL-015/packet.json", "/workspace/scratch/473866e9940e/repo/evals/v0.2/results/v0.2/V02-REAL-015/host-metadata.json"]
  },
  "decisions": {"fixed": ["Return false when search is null or undefined before Array/Object inspection.", "Keep the SearchParamsOption parameter type unchanged.", "Keep URLSearchParams and its deletedParametersSymbol size check before the generic object branch.", "Keep non-empty trimmed string semantics, including '0' => true."], "assumptions": ["Use a localized @ts-expect-error or explicit runtime cast in the test to represent an untyped JavaScript caller; trusted clean base remains current."]},
  "invariants": ["All SearchParamsOption typed inputs retain current results.", "URLSearchParams deletion markers remain actionable even with no visible entries.", "No merge, core request construction, or public type changes."],
  "non_goals": ["Adding null to SearchParamsOption.", "Changing empty string/array/record handling.", "Refactoring deletion tracking or changing dependencies."],
  "scope": {"write_globs": ["source/utils/options.ts", "test/main.ts"], "read_globs": ["source/utils/options.ts", "source/utils/merge.ts", "source/types/options.ts", "test/main.ts"], "forbidden_globs": ["source/types/**", "source/core/**", "source/utils/merge.ts", "package.json", "package-lock.json", "pnpm-lock.yaml", "yarn.lock"], "shared_interfaces": ["hasSearchParameters runtime behavior"], "exclusive_resources": ["source/utils/options.ts:hasSearchParameters", "test/main.ts:focused search parameter regression"], "parallel_safe": false, "isolation": "manual"},
  "required_capabilities": ["bounded TypeScript bug fix", "runtime/type boundary testing", "AVA test editing"],
  "execution_profile": {"role": "worker", "capability_tier": "bounded-local-implementation", "cost_tier": "low", "reasoning_effort": "high", "preferred_model": null, "fallback_profiles": ["Return public type or deletion design changes to architect."]},
  "implementation_instructions": ["Change the initial guard to return false for null as well as undefined; do not change branch order or other expressions.", "Import hasSearchParameters directly in test/main.ts and add a focused test that passes runtime null with a localized type suppression/cast and asserts false, then asserts '0' is true.", "Retain existing URLSearchParams deletion tests unchanged and do not modify types/merge/core files."],
  "acceptance_criteria": [
    {"id": "AC1", "statement": "Runtime null returns false rather than throwing.", "evidence_required": "Direct focused AVA assertion and minimal guard diff."},
    {"id": "AC2", "statement": "String '0' remains true.", "evidence_required": "Direct focused assertion."},
    {"id": "AC3", "statement": "URLSearchParams deletion behavior is preserved.", "evidence_required": "Unchanged deletion-marker source branch and retained existing deletion integration tests in task-local diff."},
    {"id": "AC4", "statement": "The two authorized files pass frozen validation.", "evidence_required": "Required command exit 0 and task-local status."}
  ],
  "validation": [{"command": "node -e \"const fs=require('fs'); for (const p of ['source/utils/options.ts','test/main.ts']) { if (!fs.readFileSync(p,'utf8').trim()) process.exit(1) }\"", "purpose": "Run the packet's exact frozen file validation; it is the only required command.", "mutating": false, "required": true}],
  "expected_evidence": ["Patch limited to source/utils/options.ts and test/main.ts.", "Required command/output/status.", "Focused null/'0' test and retained deletion tests; external result evidence."],
  "stop_conditions": ["A public type, merge/core, dependency, lockfile, or other out-of-scope change is required.", "Frozen command needs installation/network/credentials/expanded permission.", "Trusted base/clean status differs or deletion behavior would change."],
  "risk": {"level": "low", "flags": ["untyped runtime input", "URLSearchParams deletion invariant"]},
  "complexity": "bounded",
  "budgets": {"max_attempts": 2, "max_review_rounds": 2},
  "authorization": {"network": false, "credentials": false, "external_side_effects": false, "destructive_actions": false, "targets": ["source/utils/options.ts", "test/main.ts"]},
  "provenance": {"base_revision": "3419113b48e034fdcf8fa6bd3be3da7b3d0d758f", "created_by": "eclipse-architect", "created_at": "2026-08-13T00:00:00+08:00"}
}
```
