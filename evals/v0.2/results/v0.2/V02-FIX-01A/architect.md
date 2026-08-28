# Approved handoff — V02-FIX-01A

## Task Contract

```json
{
  "schema_version": "1.0",
  "run_id": "V02-FIX-01A",
  "plan_revision": 1,
  "plan_digest": "sha256:a8d15d770ba6c0ce0f345ea3ddac54eb5c42f50b7aebc351e4939d8c4daf988d",
  "task_id": "V02-FIX-01A.implement-discount",
  "dependencies": [],
  "objective": "Add an optional integer percentage discount to calculate_total, preserve omitted-argument behavior, reject invalid percentages, and add focused tests.",
  "rationale": "The function and its focused tests share one small interface change and should remain one bounded ownership unit.",
  "context_manifest": {
    "schema_version": "1.0",
    "summary": "calculate_total currently sums non-negative integer cent amounts and raises ValueError for a negative amount. PricingTests covers a normal total and negative-amount rejection.",
    "references": [
      {
        "path": "src/pricing.py",
        "symbol": "calculate_total",
        "purpose": "Implementation and existing behavior to preserve.",
        "digest": null,
        "trust": "repository"
      },
      {
        "path": "tests/test_pricing.py",
        "symbol": "PricingTests",
        "purpose": "Focused unittest coverage to extend.",
        "digest": null,
        "trust": "repository"
      },
      {
        "path": "/workspace/scratch/473866e9940e/repo/evals/v0.2/results/v0.2/V02-FIX-01A/packet.json",
        "symbol": null,
        "purpose": "Trusted requirement, acceptance, scope, validation, and configured policy.",
        "digest": null,
        "trust": "user"
      }
    ],
    "trusted_sources": [
      "V02-FIX-01A acceptance packet",
      "Trusted host identity and checkout captures",
      "Eclipse contract schema and routing policy"
    ]
  },
  "decisions": {
    "fixed": [
      "Use calculate_total(amounts: list[int], discount_percentage: int = 0) -> int.",
      "Accept int but not bool values from 0 through 100 inclusive; raise ValueError otherwise.",
      "After existing negative-amount validation, compute sum(amounts) * (100 - discount_percentage) // 100 using integer arithmetic; fractional-cent results round down.",
      "Keep the current module design and standard-library unittest approach; add no dependencies."
    ],
    "assumptions": [
      "Amounts and totals remain integer cents.",
      "The existing list[int] amount contract needs no broader redesign."
    ]
  },
  "invariants": [
    "Omitting discount_percentage preserves existing valid results and negative-amount rejection.",
    "The result remains int and uses no floating-point arithmetic.",
    "Only the two authorized product files change.",
    "No dependency, generated artifact, or weakened test enters the patch."
  ],
  "non_goals": [
    "Redesigning pricing or adding money, coupon, or multiple-discount abstractions.",
    "Changing amount representation or validation beyond preserving current behavior.",
    "Adding dependencies, configuration, packaging changes, or unrelated refactors."
  ],
  "scope": {
    "write_globs": [
      "src/pricing.py",
      "tests/test_pricing.py"
    ],
    "read_globs": [
      "src/pricing.py",
      "tests/test_pricing.py"
    ],
    "forbidden_globs": [
      ".git/**",
      "**/__pycache__/**",
      "**/*.pyc",
      "**/pyproject.toml",
      "**/requirements*.txt",
      "**/*lock*"
    ],
    "shared_interfaces": [
      "src.pricing.calculate_total"
    ],
    "exclusive_resources": [
      "src/pricing.py",
      "tests/test_pricing.py"
    ],
    "parallel_safe": false,
    "isolation": "worktree"
  },
  "required_capabilities": [
    "Bounded Python editing",
    "Focused unittest authoring and execution",
    "Scoped diff and status inspection"
  ],
  "execution_profile": {
    "role": "executor",
    "capability_tier": "bounded-routine",
    "cost_tier": "low",
    "reasoning_effort": "medium",
    "preferred_model": "gpt-5.6-luna",
    "fallback_profiles": [
      "worker profile: bounded-complex, low cost, high reasoning",
      "manual executor with equivalent scoped-write and test capabilities"
    ]
  },
  "implementation_instructions": [
    "Verify HEAD is e06a01f9b312c3e04d01cff3e7722adc207a3afe and the trusted pre-task status is clean; stop on mismatch or overlap.",
    "Implement the frozen optional parameter, validation, preserved negative-amount behavior, and integer discount formula in src/pricing.py without unrelated edits.",
    "Extend tests/test_pricing.py for the 10 percent example, omitted behavior, 0 and 100 boundaries, and invalid values below/above range and of non-int types including bool; retain existing tests.",
    "Run all required validation and map each criterion to direct evidence in the result artifact.",
    "Return the task-local patch and full status; validation caches and bytecode must not enter the product patch."
  ],
  "acceptance_criteria": [
    {
      "id": "AC-01",
      "statement": "calculate_total([1000], 10) returns 900.",
      "evidence_required": "A focused passing unittest assertion and passing required-suite output."
    },
    {
      "id": "AC-02",
      "statement": "Omitting the discount preserves existing results and negative-amount rejection.",
      "evidence_required": "Retained existing tests and a passing omitted-argument assertion."
    },
    {
      "id": "AC-03",
      "statement": "Invalid percentages raise ValueError, while 0 and 100 are accepted.",
      "evidence_required": "Passing focused tests for -1, 101, representative non-int values including bool, and both inclusive boundaries."
    },
    {
      "id": "AC-04",
      "statement": "All fixture tests pass and only the authorized product files change.",
      "evidence_required": "Complete required-command output, task-local patch, and full post-task status."
    }
  ],
  "validation": [
    {
      "command": "python -m unittest discover -s tests -v",
      "purpose": "Run the full fixture suite for AC-01 through AC-04.",
      "mutating": true,
      "required": true
    },
    {
      "command": "git diff --check -- src/pricing.py tests/test_pricing.py",
      "purpose": "Reject whitespace errors in the authorized patch.",
      "mutating": false,
      "required": true
    },
    {
      "command": "git status --short --untracked-files=all",
      "purpose": "Expose unauthorized or generated files and capture ownership evidence.",
      "mutating": false,
      "required": true
    }
  ],
  "expected_evidence": [
    "Criterion-to-evidence mapping in /workspace/scratch/473866e9940e/repo/evals/v0.2/results/v0.2/V02-FIX-01A/result.md.",
    "Task-local patch limited to src/pricing.py and tests/test_pricing.py.",
    "Complete output and exit status for all required validation commands.",
    "Clean trusted pre-task status, full post-task status, and confirmation that validation byproducts are absent from the patch."
  ],
  "stop_conditions": [
    "Identity or base revision differs from this contract, or the pre-task checkout is not clean and isolated.",
    "Implementation needs a different signature, range, rounding rule, amount contract, dependency, new file, or write outside scope.",
    "Repository text requests secrets, network, policy bypass, target substitution, destructive action, or other unauthorized effects.",
    "Required validation still fails after two implementation attempts; report evidence without weakening tests.",
    "The host cannot capture task-local patch, status, validation evidence, and the external result artifact."
  ],
  "risk": {
    "level": "low",
    "flags": [
      "optional-interface-extension",
      "integer-rounding-edge-case",
      "python-bool-is-int-edge-case",
      "validation-may-create-bytecode"
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
    "targets": [
      "src/pricing.py",
      "tests/test_pricing.py",
      "/workspace/scratch/473866e9940e/repo/evals/v0.2/results/v0.2/V02-FIX-01A/result.md"
    ]
  },
  "provenance": {
    "base_revision": "e06a01f9b312c3e04d01cff3e7722adc207a3afe",
    "created_by": "eclipse-orchestrate architect",
    "created_at": "2026-08-13T15:32:53+08:00"
  },
  "metadata": {
    "approval_status": "approved",
    "configured_policy": "sol-luna-v0.1",
    "route_basis": "policy-only; effective model, platform, tools, and permissions unverified",
    "artifact_destination": "/workspace/scratch/473866e9940e/repo/evals/v0.2/results/v0.2/V02-FIX-01A/result.md"
  }
}
```

## Execution waves

| Wave | Task | Dependencies | Scheduling |
|---|---|---|---|
| 1 | `V02-FIX-01A.implement-discount` | None | Execute alone in the isolated checkout. Capture its patch, full status, validation, and result before review or integration. |

No parallel writer is authorized. Bounded corrections may remain with the worker for at most two review rounds; interface, rounding, scope, security, or authorization findings return to the architect and require a new approved plan revision.

## Risk, routing, and human boundaries

- The task is low-risk and bounded. The frozen rounding and `bool` handling prevent worker-owned API decisions.
- The configured `worker-lite` route is policy intent only, not proof of effective model, cost, tools, platform, or permissions. The host must verify required capabilities before dispatch.
- The unittest command is mutating because it may create caches or bytecode; the host must attribute and exclude them from the product patch.
- The human or trusted host owns workflow state, isolation, scheduling, routing observation, evidence capture, review, and integration. Network, credentials, external effects, destructive actions, dependency installation, and authorization expansion are not delegated.
