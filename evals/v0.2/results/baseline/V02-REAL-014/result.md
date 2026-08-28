{
  "schema_version": "1.0",
  "run_id": "V02-REAL-014-baseline",
  "plan_revision": 1,
  "plan_digest": "6a6cbc007a883d02624017a449c342abe91af301829e3eeef900e11fe2b487e8",
  "task_id": "V02-REAL-014-implement-minimum-retry-delay",
  "task_contract_digest": "sha256:9fe2d6fe7d3a69c97e5483f9e8b19bf35a400480b140b86bad8214c5e14b886d",
  "attempt": 1,
  "status": "blocked",
  "worker_identity": {
    "role": "executor",
    "requested_model": "luna",
    "configured_model": "gpt-5.6-luna",
    "effective_model": null,
    "verification": "unverified"
  },
  "files_changed": [
    "source/types/retry.ts",
    "source/utils/normalize.ts",
    "test/retry.ts"
  ],
  "implementation_summary": "Added the optional public minimumDelayMs retry option, normalized omitted and negative values to 0, floored only the built-in exponential delay, and added focused normalization, built-in-delay, and custom-delay tests. Validation is blocked because this isolated checkout has no local lint, TypeScript, or AVA dependencies and package installation/network access is not authorized.",
  "decisions": [
    "Kept the default exponential delay function unchanged and wrapped it only when no custom retry.delay callback is supplied.",
    "Applied Math.max(0, configured minimum) during normalization so finite negative values clamp to 0 while non-negative values are preserved.",
    "Used the existing jitter callback boundary in focused tests to inspect pre-jitter delay values without wall-clock assertions."
  ],
  "commands": [
    {
      "command": "node -e \"const fs=require('fs'); for (const p of ['source/types/retry.ts','source/utils/normalize.ts','test/retry.ts']) { if (!fs.readFileSync(p,'utf8').trim()) process.exit(1) }\"",
      "purpose": "Run the exact packet-mandated file-presence validation.",
      "exit_code": 0,
      "outcome": "passed",
      "summary": "All three authorized files exist and are non-empty."
    },
    {
      "command": "npx xo source/types/retry.ts source/utils/normalize.ts test/retry.ts",
      "purpose": "Lint the complete authorized write scope.",
      "exit_code": null,
      "outcome": "not-run",
      "summary": "The checkout has no local xo dependency or executable; running npx would require an unauthorized package fetch."
    },
    {
      "command": "npx tsc --noEmit --project tsconfig.json",
      "purpose": "Verify the public type and implementation compile without generating distribution artifacts.",
      "exit_code": null,
      "outcome": "not-run",
      "summary": "The checkout has no local TypeScript dependency or executable; running npx would require an unauthorized package fetch."
    },
    {
      "command": "npx ava test/retry.ts --match='*minimumDelayMs*'",
      "purpose": "Run the focused feature tests.",
      "exit_code": null,
      "outcome": "not-run",
      "summary": "The checkout has no local AVA dependency or executable; running npx would require an unauthorized package fetch."
    },
    {
      "command": "npx ava test/retry.ts",
      "purpose": "Run the complete retry regression suite, including existing maxRetryAfter and jitter coverage.",
      "exit_code": null,
      "outcome": "not-run",
      "summary": "The checkout has no local AVA dependency or executable; running npx would require an unauthorized package fetch."
    },
    {
      "command": "git diff --check && git diff --name-only",
      "purpose": "Verify patch hygiene and the authorized three-file scope.",
      "exit_code": 0,
      "outcome": "passed",
      "summary": "git diff --check passed; changed paths are source/types/retry.ts, source/utils/normalize.ts, and test/retry.ts only."
    }
  ],
  "criteria_evidence": [
    {
      "criterion_id": "AC-01",
      "status": "not-tested",
      "evidence": "The RetryOptions diff adds minimumDelayMs?: number with a documented default of 0, and focused tests supply the option without suppression; required TypeScript validation could not run."
    },
    {
      "criterion_id": "AC-02",
      "status": "not-tested",
      "evidence": "The normalization diff adds a default of 0 and clamps via Math.max(0, value); focused assertions cover omitted, undefined, numeric shorthand, finite negative, and positive values, but AVA could not run."
    },
    {
      "criterion_id": "AC-03",
      "status": "not-tested",
      "evidence": "The built-in delay wrapper returns the greater of the existing default delay and minimumDelayMs, and a focused test captures 1000 before jitter; AVA could not run."
    },
    {
      "criterion_id": "AC-04",
      "status": "not-tested",
      "evidence": "The implementation preserves normalizedRetry.delay when supplied, and a focused test captures the custom 100 millisecond delay despite a 1000 millisecond minimum; AVA could not run."
    },
    {
      "criterion_id": "AC-05",
      "status": "not-tested",
      "evidence": "No source/core path changed and the existing downstream jitter, backoffLimit, maxRetryAfter, and retry-header code is untouched; the complete retry regression suite could not run."
    },
    {
      "criterion_id": "AC-06",
      "status": "satisfied",
      "evidence": "git diff --check exited 0 and git diff --name-only listed exactly source/types/retry.ts, source/utils/normalize.ts, and test/retry.ts."
    }
  ],
  "unresolved_issues": [
    "Lint, TypeScript compilation, focused tests, and the complete retry suite remain unexecuted until local project dependencies are provisioned without network access."
  ],
  "blockers": [
    "ENV_FAILURE: node_modules is absent and xo, tsc, and ava are unavailable locally; the task forbids installing packages or enabling network access."
  ],
  "deviations": [
    "Four required tool-dependent validation commands were not run because their executables were unavailable under the task authorization."
  ],
  "observed_risks": [
    "The patch has not been linted, type-checked, or executed by AVA in this isolated checkout."
  ],
  "requested_escalation": {
    "code": "ENV_FAILURE",
    "reason": "Required local xo, TypeScript, and AVA dependencies are unavailable, and fetching or installing them is not authorized.",
    "route_to": "host"
  },
  "git": {
    "base_revision": "3419113b48e034fdcf8fa6bd3be3da7b3d0d758f",
    "changed_files_digest": "sha256:b71e9d3d822ceb0bd11a46e31d684773a8121d0e8811996f1d2da953f38d8f42"
  },
  "usage": {
    "quality": "unavailable",
    "input_tokens": null,
    "output_tokens": null,
    "cost": null,
    "currency": null,
    "source": "Trusted host usage metadata was not provided."
  },
  "started_at": "2026-08-13T04:43:00Z",
  "finished_at": "2026-08-13T04:51:00Z",
  "metadata": {
    "case_id": "V02-REAL-014",
    "policy": "sol-luna-v0.1",
    "route_verification": "unverified-policy-only"
  }
}
