{
  "schema_version": "1.0",
  "run_id": "V02-REAL-014-baseline",
  "plan_revision": 1,
  "plan_digest": "6a6cbc007a883d02624017a449c342abe91af301829e3eeef900e11fe2b487e8",
  "task_id": "V02-REAL-014-implement-minimum-retry-delay",
  "task_contract_digest": "sha256:9fe2d6fe7d3a69c97e5483f9e8b19bf35a400480b140b86bad8214c5e14b886d",
  "result_digest": "sha256:a21f72a06a5a8ee742ae41f65c0708804097a08b07f57bbceb106481c016b75f",
  "review_round": 1,
  "outcome": "escalated",
  "reviewer_identity": {
    "role": "reviewer",
    "requested_model": "gpt-5.6-sol",
    "effective_model": null,
    "verification": "unverified"
  },
  "permissions": {
    "desired": "read-only",
    "effective": "unverified",
    "enforcement": "The host supplied no trusted mechanical read-only attestation. The reviewer used read-only checkout inspection and non-mutating validation and wrote only this required review contract outside the checkout."
  },
  "findings": [
    {
      "id": "V02-REAL-014-F01",
      "severity": "high",
      "type": "insufficient-evidence",
      "path": "repo/evals/v0.2/results/baseline/V02-REAL-014/validation.txt",
      "symbol": null,
      "criterion_id": null,
      "evidence": "The only host validation record is the packet-mandated non-empty-file check with exit code 0. The required XO lint, TypeScript no-emit compile, focused AVA feature tests, and complete test/retry.ts regression run were not executed because the isolated checkout has no node_modules or local executables. The worker correctly reports all four commands as not-run and the Result Contract status as blocked.",
      "impact": "AC-01 through AC-05 lack their required executable evidence. Static inspection supports the intended design, but cannot establish that the public type compiles, the added tests execute, or existing maxRetryAfter, retry-header, jitter, and backoffLimit behavior remains regression-free. Acceptance is therefore prohibited.",
      "correction": "Have an authorized human or host provision the pinned project dependencies without modifying the candidate patch, or run the exact four required commands in a trusted equivalent checkout at base revision 3419113b48e034fdcf8fa6bd3be3da7b3d0d758f with this exact patch. Supply exit codes and concise outputs for XO, TypeScript, the focused minimumDelayMs tests, and the complete retry suite before any acceptance decision.",
      "disposition": "human"
    }
  ],
  "criteria_verdicts": [
    {
      "criterion_id": "AC-01",
      "status": "unverified",
      "evidence": "The actual diff adds optional minimumDelayMs?: number with @default 0 and test code supplies it without suppression, but the contract explicitly requires successful TypeScript validation and that command was not run."
    },
    {
      "criterion_id": "AC-02",
      "status": "unverified",
      "evidence": "Static inspection shows defaultRetryOptions.minimumDelayMs = 0 and Math.max(0, configured ?? 0); the focused assertions cover omitted, undefined, numeric shorthand, finite negative, and positive inputs. AVA did not run, so the required assertion evidence is absent."
    },
    {
      "criterion_id": "AC-03",
      "status": "unverified",
      "evidence": "The built-in-only wrapper computes Math.max(defaultRetryOptions.delay(attemptCount), minimumDelayMs), and unchanged Ky.#calculateDelay applies jitter then backoffLimit downstream. The focused test would inspect 1000 before jitter, but it was not executed."
    },
    {
      "criterion_id": "AC-04",
      "status": "unverified",
      "evidence": "The nullish fallback preserves a supplied retry.delay callback, and the focused test would observe its 100 millisecond value despite a 1000 millisecond minimum. The required AVA evidence was not produced."
    },
    {
      "criterion_id": "AC-05",
      "status": "unverified",
      "evidence": "No source/core file changed and static inspection confirms server retry timing still returns Math.min(maxRetryAfter, after) without the default-delay or jitter path. The required complete test/retry.ts run, including existing maxRetryAfter and jitter coverage, was not executed."
    },
    {
      "criterion_id": "AC-06",
      "status": "satisfied",
      "evidence": "Reviewer inspection of the actual checkout found HEAD at the pinned base revision, git diff --check passed, and git diff --name-only listed exactly source/types/retry.ts, source/utils/normalize.ts, and test/retry.ts. The supplied changed-file list agrees."
    }
  ],
  "validation_summary": "The packet-mandated node file-presence command passed with exit code 0. Independent git verification confirmed the pinned HEAD, a clean diff check, and exactly the three authorized changed paths. The Task and Result Contracts validated semantically and bind to canonical digests sha256:9fe2d6fe7d3a69c97e5483f9e8b19bf35a400480b140b86bad8214c5e14b886d and sha256:a21f72a06a5a8ee742ae41f65c0708804097a08b07f57bbceb106481c016b75f. The captured patch differs from the actual diff only by one final blank line. XO, TypeScript, focused AVA, and full retry AVA validation remain not-run because local dependencies are absent; no package installation was authorized.",
  "residual_risk": [
    "The candidate remains unlinted, uncompiled, and unexecuted; all behavioral claims beyond static control-flow inspection remain unverified.",
    "Runtime NaN is accepted by the public number type and Math.max(0, NaN) remains NaN. The frozen task explicitly specifies finite negative normalization but does not decide whether non-finite values should be rejected or clamped.",
    "Effective reviewer model and mechanical read-only enforcement were not established by trusted host metadata."
  ],
  "started_at": "2026-08-13T04:59:22Z",
  "finished_at": "2026-08-13T04:59:29Z",
  "metadata": {
    "case_id": "V02-REAL-014",
    "policy": "sol-luna-v0.1",
    "base_revision": "3419113b48e034fdcf8fa6bd3be3da7b3d0d758f",
    "actual_changed_files": [
      "source/types/retry.ts",
      "source/utils/normalize.ts",
      "test/retry.ts"
    ]
  }
}
