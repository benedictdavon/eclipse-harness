{
  "schema_version": "1.0",
  "run_id": "V02-REAL-014-baseline",
  "plan_revision": 1,
  "plan_digest": "6a6cbc007a883d02624017a449c342abe91af301829e3eeef900e11fe2b487e8",
  "task_id": "V02-REAL-014-implement-minimum-retry-delay",
  "parent_task_id": null,
  "dependencies": [],
  "objective": "Add retry.minimumDelayMs as an optional public number, normalize it to a non-negative value, and use it as the floor for Ky's built-in retry delay while preserving custom delay, jitter, backoffLimit, maxRetryAfter, and server retry-header behavior.",
  "rationale": "The public option and its normalization belong in the existing retry type and normalizeRetryOptions boundary. The existing core retry pipeline already consumes the normalized delay function before applying jitter and backoffLimit, while retry timing headers take a separate maxRetryAfter path, so no core timing change is authorized.",
  "context_manifest": {
    "schema_version": "1.0",
    "summary": "One bounded public-option change in the pinned Ky checkout. The worker may edit only the retry type, retry normalization, and focused retry tests.",
    "references": [
      {
        "path": "repo/evals/v0.2/results/baseline/V02-REAL-014/packet.json",
        "symbol": null,
        "purpose": "Original requirement, acceptance criteria, repository revision, and authorized write scope.",
        "digest": "b27663bedac4c996f7710ef9c05e5d0c8214c25f26be95bff9ba2f4bd5b88151",
        "trust": "user"
      },
      {
        "path": "source/types/retry.ts",
        "symbol": "RetryOptions",
        "purpose": "Public retry option contract to extend.",
        "digest": "e94030e12384ac501071fd5212ef5660969ea00bbdf4717bdf635521d4b30556",
        "trust": "repository"
      },
      {
        "path": "source/utils/normalize.ts",
        "symbol": "normalizeRetryOptions",
        "purpose": "Normalization boundary and built-in retry delay definition.",
        "digest": "3ac353db9ae677df5789da451377621c958c4e3e66f03cdd86b66b17ebc7c95e",
        "trust": "repository"
      },
      {
        "path": "source/core/Ky.ts",
        "symbol": "Ky.#calculateDelay",
        "purpose": "Read-only confirmation that normalized delay is followed by the existing jitter and backoffLimit stages and that retry headers use maxRetryAfter separately.",
        "digest": "94a6e80411c77663c5fe272d9fccb942bab7290d7e10fdd9ef89f99d3c01ab25",
        "trust": "repository"
      },
      {
        "path": "test/retry.ts",
        "symbol": null,
        "purpose": "Existing retry coverage and location for focused minimumDelayMs tests.",
        "digest": "85d931705ff50366a2d96da4fd557f7a31cf01c7109904ca0e1e8d9327599d0d",
        "trust": "repository"
      }
    ],
    "trusted_sources": [
      "Frozen architect prompt",
      "eclipse-orchestrate skill and task-contract schema",
      "V02-REAL-014 packet"
    ]
  },
  "decisions": {
    "fixed": [
      "minimumDelayMs is optional in RetryOptions and its documented/default normalized value is 0 milliseconds.",
      "A finite negative minimumDelayMs is clamped to 0 during normalizeRetryOptions; it is not surfaced as a negative internal value and does not cause a new exception.",
      "The normalized minimum is a floor for the built-in exponential retry delay only. An explicitly supplied retry.delay function remains authoritative and is not wrapped or clamped by minimumDelayMs.",
      "For the built-in delay, the minimum is applied before the existing jitter and backoffLimit stages. Those stages keep their current behavior, so jitter or an upper backoffLimit may still produce a final scheduled delay below minimumDelayMs.",
      "Server-provided retry timing continues to bypass the default delay and jitter path and remains governed only by existing maxRetryAfter behavior.",
      "No production file outside the three paths named by the packet may change. In particular, source/core/Ky.ts and source/core/retry-timing.ts remain untouched."
    ],
    "assumptions": [
      "The packet's phrase 'normalize it to a non-negative value' means clamping finite negative inputs to zero rather than throwing.",
      "The requested lower bound applies to Ky's built-in delay calculation, not custom delay callbacks or server-provided retry timing.",
      "Configured or requested routing is policy-only; the effective model and permissions are unverified by trusted host metadata."
    ]
  },
  "invariants": [
    "Existing retry limit, retry method, retry status-code, timeout, and hook behavior remains unchanged.",
    "maxRetryAfter and retry timing-header interpretation remain unchanged.",
    "Boolean and custom-function jitter behavior, validation, and call ordering remain unchanged.",
    "backoffLimit remains the final upper clamp on calculated default retry delays.",
    "Numeric retry shorthand and undefined retry fields retain their current defaults.",
    "The pinned base revision remains 3419113b48e034fdcf8fa6bd3be3da7b3d0d758f."
  ],
  "non_goals": [
    "Changing the retry algorithm, exponential factor, retry count, or eligible errors.",
    "Applying minimumDelayMs to a user-provided retry.delay callback.",
    "Applying minimumDelayMs after jitter or backoffLimit.",
    "Applying minimumDelayMs to Retry-After, RateLimit-Reset, or other server timing headers.",
    "Changing maxRetryAfter, jitter, backoffLimit, or retry timing parsing.",
    "Updating documentation, changelogs, package metadata, generated distribution files, or lockfiles."
  ],
  "scope": {
    "write_globs": [
      "source/types/retry.ts",
      "source/utils/normalize.ts",
      "test/retry.ts"
    ],
    "read_globs": [
      "source/types/retry.ts",
      "source/utils/normalize.ts",
      "source/core/Ky.ts",
      "source/core/retry-timing.ts",
      "test/retry.ts",
      "test/helpers/**",
      "package.json",
      "tsconfig*.json"
    ],
    "forbidden_globs": [
      ".git/**",
      ".github/**",
      "source/core/**",
      "package.json",
      "package-lock.json",
      "pnpm-lock.yaml",
      "yarn.lock",
      "distribution/**",
      "**/.env*"
    ],
    "shared_interfaces": [
      "source/types/retry.ts::RetryOptions",
      "source/utils/normalize.ts::normalizeRetryOptions"
    ],
    "exclusive_resources": [
      "source/types/retry.ts",
      "source/utils/normalize.ts",
      "test/retry.ts"
    ],
    "parallel_safe": false,
    "isolation": "branch"
  },
  "required_capabilities": [
    "TypeScript public API evolution",
    "bounded option normalization",
    "retry timing semantics",
    "AVA test authoring",
    "read-only git verification"
  ],
  "execution_profile": {
    "role": "worker",
    "capability_tier": "normal-bounded-implementation",
    "cost_tier": "standard",
    "reasoning_effort": "high",
    "preferred_model": "luna",
    "fallback_profiles": [
      "luna-max-for-concrete-local-reasoning-blocker",
      "architect-escalation-for-semantics-or-scope-change"
    ]
  },
  "implementation_instructions": [
    "Add minimumDelayMs?: number to RetryOptions with concise documentation that states the 0 millisecond default and that it floors only the built-in retry delay.",
    "Extend InternalRetryOptions/defaultRetryOptions so normalized retry options always contain minimumDelayMs, including numeric retry shorthand and omitted or undefined fields.",
    "Normalize a finite negative minimumDelayMs to 0. Preserve a non-negative configured value.",
    "When retry.delay is absent, make the normalized built-in delay return the greater of the existing exponential result and normalized minimumDelayMs. When retry.delay is present, preserve that callback unchanged.",
    "Do not edit core retry calculation or retry timing-header code; rely on the existing pipeline to apply jitter and backoffLimit after the normalized built-in delay.",
    "Add focused tests in test/retry.ts whose names include minimumDelayMs. Cover public option acceptance, a positive minimum raising the built-in delay, a negative input normalizing to zero, and preservation of the custom-delay boundary. Prefer deterministic inspection/captured scheduling over wall-clock-only assertions where practical.",
    "Keep all unrelated retry tests and semantics intact and avoid formatting or refactoring outside the touched logic."
  ],
  "acceptance_criteria": [
    {
      "id": "AC-01",
      "statement": "RetryOptions exposes optional minimumDelayMs as a number with an effective default of 0.",
      "evidence_required": "Diff hunk for RetryOptions plus successful TypeScript validation and a compiling test that supplies retry.minimumDelayMs without suppression."
    },
    {
      "id": "AC-02",
      "statement": "normalizeRetryOptions always produces a non-negative minimumDelayMs for omitted, undefined, numeric-shorthand, and finite negative inputs; a negative input becomes 0.",
      "evidence_required": "Focused assertions demonstrating the normalized default and negative-input result, plus the implementation diff."
    },
    {
      "id": "AC-03",
      "statement": "A positive minimumDelayMs floors the built-in exponential retry delay before existing jitter and backoffLimit processing.",
      "evidence_required": "Focused test evidence observing a built-in retry delay raised to the configured minimum without changing the exponential formula."
    },
    {
      "id": "AC-04",
      "statement": "An explicitly supplied retry.delay callback is not modified by minimumDelayMs.",
      "evidence_required": "Focused test showing a custom delay below minimumDelayMs remains the delay value passed into the existing downstream pipeline."
    },
    {
      "id": "AC-05",
      "statement": "maxRetryAfter, server retry-header timing, jitter, and backoffLimit semantics remain unchanged.",
      "evidence_required": "No diff under source/core/** and a passing complete test/retry.ts run, including existing maxRetryAfter and jitter coverage."
    },
    {
      "id": "AC-06",
      "statement": "Only source/types/retry.ts, source/utils/normalize.ts, and test/retry.ts are modified.",
      "evidence_required": "git diff --name-only output containing no other path and a clean git diff --check result."
    }
  ],
  "validation": [
    {
      "command": "node -e \"const fs=require('fs'); for (const p of ['source/types/retry.ts','source/utils/normalize.ts','test/retry.ts']) { if (!fs.readFileSync(p,'utf8').trim()) process.exit(1) }\"",
      "purpose": "Run the exact packet-mandated file-presence validation.",
      "mutating": false,
      "required": true
    },
    {
      "command": "npx xo source/types/retry.ts source/utils/normalize.ts test/retry.ts",
      "purpose": "Lint the complete authorized write scope.",
      "mutating": false,
      "required": true
    },
    {
      "command": "npx tsc --noEmit --project tsconfig.json",
      "purpose": "Verify the public type and implementation compile without generating distribution artifacts.",
      "mutating": false,
      "required": true
    },
    {
      "command": "npx ava test/retry.ts --match='*minimumDelayMs*'",
      "purpose": "Run the focused feature tests.",
      "mutating": false,
      "required": true
    },
    {
      "command": "npx ava test/retry.ts",
      "purpose": "Run the complete retry regression suite, including existing maxRetryAfter and jitter coverage.",
      "mutating": false,
      "required": true
    },
    {
      "command": "git diff --check && git diff --name-only",
      "purpose": "Verify patch hygiene and the authorized three-file scope.",
      "mutating": false,
      "required": true
    }
  ],
  "expected_evidence": [
    "Base revision and pre-work git status.",
    "A criterion-by-criterion result mapping for AC-01 through AC-06.",
    "Relevant diff hunks for the type, normalization, and focused tests.",
    "Exit status and concise output for every required validation command.",
    "Final git diff --name-only and git diff --check output.",
    "Any unverified routing or permission assumptions explicitly labeled as such."
  ],
  "stop_conditions": [
    "HEAD is not 3419113b48e034fdcf8fa6bd3be3da7b3d0d758f or the checkout has pre-existing changes overlapping an authorized path.",
    "Implementing the requested behavior appears to require editing source/core/** or any path outside the three write globs.",
    "A product decision is required about throwing on negative values, flooring custom delays, applying the minimum after jitter/backoffLimit, or applying it to server timing headers; return to the architect rather than choosing a new semantic.",
    "A required validation cannot run because dependencies or tools are unavailable; do not install packages or enable network access without new authority.",
    "Tests expose an existing failure unrelated to this task that cannot be separated from the change within the authorized scope.",
    "Credentials, external network access, destructive actions, generated-file changes, or external side effects become necessary."
  ],
  "risk": {
    "level": "medium",
    "flags": [
      "public-type-change",
      "retry-timing-behavior",
      "jitter-and-backoff-interaction",
      "server-header-semantics-must-remain-unchanged"
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
      "source/types/retry.ts",
      "source/utils/normalize.ts",
      "test/retry.ts",
      "ephemeral local test servers started by test/retry.ts"
    ]
  },
  "provenance": {
    "base_revision": "3419113b48e034fdcf8fa6bd3be3da7b3d0d758f",
    "created_by": "baseline-eclipse-architect",
    "created_at": "2026-08-13T04:38:11Z",
    "source_requirement_digest": "b27663bedac4c996f7710ef9c05e5d0c8214c25f26be95bff9ba2f4bd5b88151"
  },
  "metadata": {
    "case_id": "V02-REAL-014",
    "policy": "sol-luna-v0.1",
    "route_verification": "unverified-policy-only",
    "plan_digest_basis": "SHA-256 of canonical JSON containing base_revision, plan_revision, run_id, source_requirement_digest, and ordered task_ids"
  }
}

