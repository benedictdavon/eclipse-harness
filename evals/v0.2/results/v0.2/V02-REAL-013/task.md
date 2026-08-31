```json
{
  "schema_version": "1.0",
  "run_id": "V02-REAL-013",
  "plan_revision": 1,
  "plan_digest": "sha256:f36e58ca0602c3202f5503489aa20ae64b023aa585d5ba864f7a0783d2ee8d10",
  "task_id": "V02-REAL-013-T1",
  "dependencies": [],
  "objective": "Reject negative numeric retry arguments in normalizeRetryOptions with the exact required Error and add focused tests while preserving numeric non-negative and object-form behavior.",
  "rationale": "The numeric shorthand currently accepts a negative limit; a check confined to that branch meets the requirement without redefining RetryOptions.",
  "context_manifest": {
    "schema_version": "1.0",
    "summary": "normalizeRetryOptions has a numeric branch that overlays limit on defaults and a separate object branch that validates arrays, lowercases methods, filters undefined, and overlays defaults. No direct normalizer tests currently exist in test/retry.ts.",
    "references": [
      {"path": "source/utils/normalize.ts", "symbol": "normalizeRetryOptions", "purpose": "Add a numeric-branch negative guard only.", "digest": null, "trust": "repository"},
      {"path": "test/retry.ts", "symbol": null, "purpose": "Add direct focused normalization tests.", "digest": null, "trust": "repository"}
    ],
    "trusted_sources": ["/workspace/scratch/473866e9940e/repo/evals/v0.2/results/v0.2/V02-REAL-013/packet.json", "/workspace/scratch/473866e9940e/repo/evals/v0.2/results/v0.2/V02-REAL-013/host-metadata.json"]
  },
  "decisions": {"fixed": ["Inside typeof retry === 'number', throw new Error('retry limit must be non-negative') when retry < 0.", "Leave zero, positive, default, and object branches unchanged.", "Do not change RetryOptions or public option types."], "assumptions": ["NaN and infinities are not negative under retry < 0 and remain existing behavior; trusted clean base remains current."]},
  "invariants": ["normalizeRetryOptions(0).limit is 0 and positive numeric input is preserved.", "Object methods lowercasing, defaults, custom fields, and validation remain unchanged.", "No public types or exports change."],
  "non_goals": ["Validating object-form limit, NaN, infinity, or integer-ness.", "Changing retry runtime semantics beyond negative numeric shorthand.", "Changing dependencies or lockfiles."],
  "scope": {"write_globs": ["source/utils/normalize.ts", "test/retry.ts"], "read_globs": ["source/utils/normalize.ts", "source/types/retry.ts", "test/retry.ts"], "forbidden_globs": ["source/types/**", "source/index.ts", "package.json", "package-lock.json", "pnpm-lock.yaml", "yarn.lock"], "shared_interfaces": ["normalizeRetryOptions numeric behavior"], "exclusive_resources": ["source/utils/normalize.ts:normalizeRetryOptions", "test/retry.ts:normalizer tests"], "parallel_safe": false, "isolation": "manual"},
  "required_capabilities": ["bounded TypeScript implementation", "AVA focused test editing"],
  "execution_profile": {"role": "worker", "capability_tier": "bounded-local-implementation", "cost_tier": "low", "reasoning_effort": "high", "preferred_model": null, "fallback_profiles": ["Return broader retry validation/type decisions to architect."]},
  "implementation_instructions": ["Add retry < 0 guard at the start of the numeric branch and throw the exact Error.", "Import normalizeRetryOptions directly into test/retry.ts and add focused assertions for -1, 0, a positive value, and a representative object preserving its configured fields/method normalization.", "Do not modify the object branch or option types."],
  "acceptance_criteria": [
    {"id": "AC1", "statement": "normalizeRetryOptions(-1) throws Error('retry limit must be non-negative').", "evidence_required": "Direct exact-error AVA assertion and source guard diff."},
    {"id": "AC2", "statement": "Zero and positive numeric limits normalize with those limits.", "evidence_required": "Focused direct assertions."},
    {"id": "AC3", "statement": "Object-form retry behavior and public types are unchanged.", "evidence_required": "Representative focused object assertion and task-local diff excluding type files."},
    {"id": "AC4", "statement": "Both authorized files remain non-empty and readable.", "evidence_required": "Required frozen command exit 0 and task-local status."}
  ],
  "validation": [{"command": "node -e \"const fs=require('fs'); for (const p of ['source/utils/normalize.ts','test/retry.ts']) { if (!fs.readFileSync(p,'utf8').trim()) process.exit(1) }\"", "purpose": "Run the packet's exact frozen file validation; it is the only required command.", "mutating": false, "required": true}],
  "expected_evidence": ["Patch limited to normalize.ts and test/retry.ts.", "Required command, exit status, and output.", "Focused test source for all required branches.", "Final task-local status and external result evidence."],
  "stop_conditions": ["A type, dependency, lockfile, object-branch, or other out-of-scope change is required.", "Frozen command needs installation/network/credentials/expanded permission.", "Trusted base/clean status differs or tests require semantics beyond fixed decisions."],
  "risk": {"level": "low", "flags": ["public retry shorthand behavior", "object-branch preservation"]},
  "complexity": "bounded",
  "budgets": {"max_attempts": 2, "max_review_rounds": 2},
  "authorization": {"network": false, "credentials": false, "external_side_effects": false, "destructive_actions": false, "targets": ["source/utils/normalize.ts", "test/retry.ts"]},
  "provenance": {"base_revision": "3419113b48e034fdcf8fa6bd3be3da7b3d0d758f", "created_by": "eclipse-architect", "created_at": "2026-08-13T00:00:00+08:00"}
}
```
