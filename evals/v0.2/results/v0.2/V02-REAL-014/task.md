```json
{
  "schema_version": "1.0",
  "run_id": "V02-REAL-014",
  "plan_revision": 1,
  "plan_digest": "sha256:2969279d0fbcca61e07c37675aa918cf758afefdf011fec5c512ed86644da937",
  "task_id": "V02-REAL-014-T1",
  "dependencies": [],
  "objective": "Add RetryOptions.minimumDelayMs, validate and normalize it, and bound the built-in exponential retry delay below by it without changing custom delay, jitter, backoffLimit, or server-header semantics.",
  "rationale": "The lower bound can be composed during normalization of the default delay, avoiding any change to the established core jitter/cap/header pipeline.",
  "context_manifest": {
    "schema_version": "1.0",
    "summary": "RetryOptions defines delay/backoff/jitter fields. normalizeRetryOptions fills a required internal shape with a default exponential delay. Ky later applies jitter, then backoffLimit; retry timing headers separately use maxRetryAfter.",
    "references": [
      {"path": "source/types/retry.ts", "symbol": "RetryOptions", "purpose": "Add and document minimumDelayMs.", "digest": null, "trust": "repository"},
      {"path": "source/utils/normalize.ts", "symbol": "defaultRetryOptions and normalizeRetryOptions", "purpose": "Default, validate, and compose the lower-bounded default delay.", "digest": null, "trust": "repository"},
      {"path": "source/core/Ky.ts", "symbol": "#calculateDelay and retry-header path", "purpose": "Read-only invariant for jitter, cap, and maxRetryAfter semantics.", "digest": null, "trust": "repository"},
      {"path": "test/retry.ts", "symbol": null, "purpose": "Add focused type/normalization/delay tests.", "digest": null, "trust": "repository"}
    ],
    "trusted_sources": ["/workspace/scratch/473866e9940e/repo/evals/v0.2/results/v0.2/V02-REAL-014/packet.json", "/workspace/scratch/473866e9940e/repo/evals/v0.2/results/v0.2/V02-REAL-014/host-metadata.json"]
  },
  "decisions": {"fixed": ["minimumDelayMs is optional number with normalized default 0.", "Negative supplied value throws exactly Error('retry.minimumDelayMs must be non-negative').", "If retry.delay is undefined, normalized delay(attempt) is Math.max(minimumDelayMs, existing exponential delay); a supplied delay is unchanged.", "Do not modify core jitter/backoff/header code."], "assumptions": ["Finite/integer validation beyond negativity is not requested; trusted clean base remains current."]},
  "invariants": ["Default behavior with omission is unchanged.", "Jitter still runs after delay and may reduce it; backoffLimit still caps afterward.", "Server retry timing and maxRetryAfter paths never use minimumDelayMs.", "Custom delay functions retain identity/return behavior."],
  "non_goals": ["Applying the lower bound after jitter or backoffLimit.", "Applying it to Retry-After/rate-limit headers or custom delay.", "Changing maxRetryAfter, jitter, core runtime files, dependencies, or locks."],
  "scope": {"write_globs": ["source/types/retry.ts", "source/utils/normalize.ts", "test/retry.ts"], "read_globs": ["source/types/retry.ts", "source/utils/normalize.ts", "source/core/Ky.ts", "test/retry.ts"], "forbidden_globs": ["source/core/**", "source/types/options.ts", "package.json", "package-lock.json", "pnpm-lock.yaml", "yarn.lock"], "shared_interfaces": ["RetryOptions", "normalizeRetryOptions internal result"], "exclusive_resources": ["source/types/retry.ts:RetryOptions", "source/utils/normalize.ts:retry defaults/normalization", "test/retry.ts:minimum delay tests"], "parallel_safe": false, "isolation": "manual"},
  "required_capabilities": ["TypeScript API typing", "retry timing semantics", "AVA focused testing"],
  "execution_profile": {"role": "worker", "capability_tier": "bounded-local-implementation", "cost_tier": "low", "reasoning_effort": "high", "preferred_model": null, "fallback_profiles": ["Return timing-order or validation expansion to architect."]},
  "implementation_instructions": ["Add the documented optional field to RetryOptions.", "Add minimumDelayMs: 0 to defaults; reject retry.minimumDelayMs < 0 before result construction.", "Build the normalized object as today, then only for an object without a supplied delay assign a delay function using the normalized minimum and existing formula; do not mutate caller input.", "Add direct normalizer tests for omission, negative error, below/above-minimum attempts, custom delay preservation, and representative jitter/maxRetryAfter fields."],
  "acceptance_criteria": [
    {"id": "AC1", "statement": "RetryOptions exposes documented optional minimumDelayMs and normalization defaults it to 0.", "evidence_required": "Type and normalizer diff plus direct assertion."},
    {"id": "AC2", "statement": "Negative minimumDelayMs throws the fixed exact Error.", "evidence_required": "Direct exact-error test."},
    {"id": "AC3", "statement": "The built-in delay respects the lower bound while a custom delay remains unchanged.", "evidence_required": "Focused tests on normalized delay at multiple attempts and custom delay."},
    {"id": "AC4", "statement": "Jitter and maxRetryAfter values/paths are unchanged and all authorized files pass frozen validation.", "evidence_required": "Representative preservation assertions, no core diff, and required command exit 0."}
  ],
  "validation": [{"command": "node -e \"const fs=require('fs'); for (const p of ['source/types/retry.ts','source/utils/normalize.ts','test/retry.ts']) { if (!fs.readFileSync(p,'utf8').trim()) process.exit(1) }\"", "purpose": "Run the packet's exact frozen file validation; it is the only required command.", "mutating": false, "required": true}],
  "expected_evidence": ["Patch limited to the three authorized files.", "Required command/output/status.", "Focused source tests covering fixed semantics and final external result evidence."],
  "stop_conditions": ["Core, options.ts, dependency, lockfile, or other out-of-scope write becomes necessary.", "Semantics require applying the floor after jitter/cap or to server headers/custom delay.", "Frozen command needs installation/network/credentials/expanded permission.", "Trusted base/clean status differs."],
  "risk": {"level": "medium", "flags": ["public option type", "retry timing behavior", "jitter/cap order preservation"]},
  "complexity": "bounded",
  "budgets": {"max_attempts": 2, "max_review_rounds": 2},
  "authorization": {"network": false, "credentials": false, "external_side_effects": false, "destructive_actions": false, "targets": ["source/types/retry.ts", "source/utils/normalize.ts", "test/retry.ts"]},
  "provenance": {"base_revision": "3419113b48e034fdcf8fa6bd3be3da7b3d0d758f", "created_by": "eclipse-architect", "created_at": "2026-08-13T00:00:00+08:00"}
}
```
