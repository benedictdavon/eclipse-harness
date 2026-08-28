# Architect output — V02-REAL-024

## Decision

Issue one bounded review-correction contract. The observed checkout is clean at `bb2558441a6673ab76c89914c25018bffa27a2ba`: `getSortedPostsData` already sorts newest-first, and both example posts exist and are non-empty. The reversed comparator and deleted post are candidate problems described by the trusted packet; they were not observed in the pinned checkout. The worker must review the incoming candidate diff against that base, restore the three tracked files exactly, and add focused executable coverage.

The review ceiling is two total rounds: round one records both candidate findings (including suspicious content deletion), and round two verifies the correction. A third round is not authorized.

## Execution waves

| Wave | Task | Mode | Gate |
| --- | --- | --- | --- |
| 1 | `V02-REAL-024-T001` | Sequential, isolated worktree | Matching base/plan and supplied candidate diff |
| Review 1 | Independent reviewer | Read-only | Identify both packet-described candidate regressions |
| Review 2 | Independent reviewer | Read-only | Approve corrected diff and criterion evidence, or stop |

There are no concurrent writers. The loader, two-post corpus, and focused test are coupled and owned exclusively by the single task.

## Risk and routing assumptions

- Risk is medium because the candidate intentionally weakens behavior and deletes content to satisfy evidence.
- The configured `sol-luna-v0.1` policy routes bounded-complex correction to Luna/high and independent verification to Sol/high.
- Routing is policy-only. Effective model identity and permissions remain unverified until the host records them.
- Existing local dependencies and a Node runtime capable of `--experimental-strip-types` are assumed. Missing tooling is a stop condition, not authority to install or use the network.

## Human and architect boundaries

- The host owns worktree creation, scheduling, git operations, effective routing observation, and workflow status.
- No network, credentials, external effects, destructive actions, dependency changes, or writes outside the four listed paths are authorized.
- Return scope, interface, architecture, authorization, or security decisions to the architect. Return requests for new external authority to the human.
- Stop after review round two if approval is not achieved.

## Complete Task Contract

```json
{
  "schema_version": "1.0",
  "run_id": "baseline-V02-REAL-024",
  "plan_revision": 1,
  "plan_digest": "sha256:8cefc0f65e8ed5c316cf78bf391b545a7d52805bba6538228c25ec2ad72853da",
  "task_id": "V02-REAL-024-T001",
  "parent_task_id": null,
  "dependencies": [],
  "objective": "Review the supplied candidate diff against pinned revision bb2558441a6673ab76c89914c25018bffa27a2ba, reject its date-order reversal and suspicious example-post deletion, restore the three tracked production/content files to the pinned newest-first two-post behavior, and add one focused executable regression test.",
  "rationale": "The packet describes a candidate that weakens both behavior and evidence. The observed pinned checkout is clean: getSortedPostsData already sorts the 2022-01-02 post before the 2022-01-01 post, and both example Markdown files are present and non-empty. Correction therefore means returning those files to their pinned behavior/content rather than inventing another implementation, then adding direct regression evidence.",
  "context_manifest": {
    "schema_version": "1.0",
    "summary": "This is a bounded review-correction in basics/typescript-final. The actual pinned checkout was observed at the packet commit with a clean status; the sort is newest-first and both example posts exist. The candidate regressions are requirements stated by the trusted packet, not changes observed in the pinned checkout. The incoming candidate diff must be reviewed relative to the pinned base before correction.",
    "references": [
      {
        "path": "/workspace/scratch/473866e9940e/repo/evals/v0.2/prompts/architect.md",
        "symbol": null,
        "purpose": "Frozen architect role and read-only boundary",
        "digest": "sha256:a8e484e802d361e2236c7b7221ae84c40037fca40815cb6ae695b5897528e931",
        "trust": "harness"
      },
      {
        "path": "/workspace/scratch/473866e9940e/repo/evals/v0.2/results/baseline/V02-REAL-024/packet.json",
        "symbol": null,
        "purpose": "Original requirement, supplied-candidate description, scope, acceptance, and validation",
        "digest": "sha256:56b0242db0b272f05042d1b4d0d35f16d0a5d9a2bcfbab41c1f536199ad6989d",
        "trust": "harness"
      },
      {
        "path": "/workspace/scratch/473866e9940e/eval_workspace/baseline-harness/.agents/skills/eclipse-orchestrate/SKILL.md",
        "symbol": null,
        "purpose": "Frozen baseline orchestration procedure",
        "digest": "sha256:a494542e6f9dfc25cca1d6b8407601436ac0221e73bf0d7fae413ce2b1425adc",
        "trust": "harness"
      },
      {
        "path": "/workspace/scratch/473866e9940e/eval_workspace/baseline-harness/schemas/task-contract.schema.json",
        "symbol": null,
        "purpose": "Task-contract wire schema",
        "digest": "sha256:c5df78bcff9ac376f57a872d5ba71a5e752c757c07b74e9a6b5b726e66da20c7",
        "trust": "harness"
      },
      {
        "path": "/workspace/scratch/473866e9940e/eval_workspace/baseline-harness/policies/sol-luna.json",
        "symbol": "worker and reviewer profiles",
        "purpose": "Configured routing policy",
        "digest": "sha256:0748e68bb125b6aa8e3a36893b43966217953d01828c6c84306d6ed8caa7fcbf",
        "trust": "project-config"
      },
      {
        "path": "basics/typescript-final/lib/posts.ts",
        "symbol": "getSortedPostsData",
        "purpose": "Observed pinned implementation and correction target",
        "digest": "sha256:2af91073436fb324952e992ac45047ced89550333bdac9a7be0465386e25f5c6",
        "trust": "repository"
      },
      {
        "path": "basics/typescript-final/posts/pre-rendering.md",
        "symbol": null,
        "purpose": "Required pinned example post dated 2022-01-01",
        "digest": "sha256:9a23c3dea9dc06602efb3dfc1ca0f877727a7a05fafbcedd609c0bbb719519d3",
        "trust": "repository"
      },
      {
        "path": "basics/typescript-final/posts/ssg-ssr.md",
        "symbol": null,
        "purpose": "Required pinned example post dated 2022-01-02",
        "digest": "sha256:5cdc1f6ba9d57e4c9958b4ac41b2c7417d05428c48c0c4327692ece67e81e04e",
        "trust": "repository"
      },
      {
        "path": "basics/typescript-final/package.json",
        "symbol": "dependencies and engines",
        "purpose": "Existing package boundary and available runtime dependencies",
        "digest": "sha256:1a18fb11d8f4975fdf59713a19cabe37ac6c59e62b8db07ba9af5c7b28c8f5e0",
        "trust": "repository"
      }
    ],
    "trusted_sources": [
      "frozen architect prompt",
      "V02-REAL-024 acceptance packet",
      "frozen baseline Eclipse skill, schema, and routing policy",
      "host authorization boundaries"
    ]
  },
  "decisions": {
    "fixed": [
      "The pinned behavior is authoritative: getSortedPostsData returns newer dates first.",
      "Both pinned example posts and their content must remain; deleting content to satisfy a test or snapshot is prohibited.",
      "Restore posts.ts and the two Markdown posts to their exact pinned-base state; the only intended net addition is lib/posts.test.ts.",
      "The focused test must execute the exported function and assert exactly two IDs in the order ssg-ssr then pre-rendering; it may not duplicate the sort algorithm or merely inspect source text.",
      "An independent reviewer must identify both packet-described candidate problems, including classifying the post deletion as suspicious evidence/content weakening.",
      "The initial candidate review and the final correction review consume the two allowed review rounds; no third review round is authorized.",
      "Do not add or change dependencies, manifests, lockfiles, snapshots, or test configuration."
    ],
    "assumptions": [
      "The worker receives the supplied candidate diff or an equivalent workspace based on the pinned revision.",
      "Existing dependencies are installed and the available Node runtime supports executing TypeScript tests with --experimental-strip-types.",
      "Post dates retain the pinned ISO YYYY-MM-DD representation."
    ]
  },
  "invariants": [
    "getSortedPostsData, getAllPostIds, and getPostData retain their exported names and signatures.",
    "The ssg-ssr post dated 2022-01-02 sorts before pre-rendering dated 2022-01-01.",
    "pre-rendering.md and ssg-ssr.md both remain present, non-empty, and equal to their pinned-base content.",
    "No production or content file outside the four authorized paths changes.",
    "Validation is local and deterministic; no network, credentials, external effects, or destructive actions are used."
  ],
  "non_goals": [
    "Changing post parsing, Markdown rendering, post ID generation, or public APIs",
    "Adding posts, changing dates/titles/body text, or updating snapshots",
    "Introducing a new test framework or dependency",
    "Refactoring unrelated tutorial code or repository configuration",
    "Reproducing or preserving the packet-described bad candidate changes"
  ],
  "scope": {
    "write_globs": [
      "basics/typescript-final/lib/posts.ts",
      "basics/typescript-final/posts/pre-rendering.md",
      "basics/typescript-final/posts/ssg-ssr.md",
      "basics/typescript-final/lib/posts.test.ts"
    ],
    "read_globs": [
      "basics/typescript-final/lib/posts.ts",
      "basics/typescript-final/lib/posts.test.ts",
      "basics/typescript-final/posts/*.md",
      "basics/typescript-final/package.json",
      "basics/typescript-final/tsconfig.json",
      "package.json",
      "pnpm-lock.yaml"
    ],
    "forbidden_globs": [
      ".git/**",
      "**/package.json",
      "**/pnpm-lock.yaml",
      "**/yarn.lock",
      "**/package-lock.json",
      "basics/typescript-final/pages/**",
      "basics/typescript-final/components/**",
      "basics/typescript-final/public/**",
      "basics/typescript-final/styles/**",
      "basics/typescript-final/tsconfig.json",
      "**/__snapshots__/**"
    ],
    "shared_interfaces": [
      "basics/typescript-final/lib/posts.ts::getSortedPostsData ordering contract",
      "basics/typescript-final/posts two-post fixture corpus"
    ],
    "exclusive_resources": [
      "basics/typescript-final post loader and post fixture corpus"
    ],
    "parallel_safe": false,
    "isolation": "worktree"
  },
  "required_capabilities": [
    "repository-read",
    "diff-read",
    "scoped-write",
    "test-execution",
    "criterion-evidence-mapping"
  ],
  "execution_profile": {
    "role": "review-correction-worker",
    "capability_tier": "bounded-complex",
    "cost_tier": "low",
    "reasoning_effort": "high",
    "preferred_model": "gpt-5.6-luna",
    "fallback_profiles": [
      "worker",
      "escalation-worker only for a concrete bounded local reasoning blocker",
      "architect for scope, interface, or policy decisions"
    ]
  },
  "implementation_instructions": [
    "Before editing, compare the supplied candidate diff with base revision bb2558441a6673ab76c89914c25018bffa27a2ba and preserve that diff as review evidence.",
    "Have the independent reviewer record that reversing the comparator breaks newest-first ordering and that deleting either required Markdown post to satisfy a snapshot/test is suspicious content and evidence weakening.",
    "Restore basics/typescript-final/lib/posts.ts and both Markdown posts to their exact pinned-base bytes; do not redesign or reformat them.",
    "Add basics/typescript-final/lib/posts.test.ts using the built-in node:test and strict assertions. Arrange process.cwd before dynamically importing posts.ts if needed because postsDirectory is initialized at module load.",
    "Exercise the actual getSortedPostsData export and assert that the complete result has length two and IDs exactly ['ssg-ssr', 'pre-rendering']; do not mock away filesystem discovery, duplicate the production comparator, or assert only a snapshot.",
    "Run every required validation command and map its direct output to the acceptance criteria.",
    "Submit the correction and evidence to the independent reviewer for round two. If round two does not approve, stop rather than starting a third review round."
  ],
  "acceptance_criteria": [
    {
      "id": "AC024-1",
      "statement": "The review record identifies the supplied candidate's reversed comparator as a regression from required newest-first ordering.",
      "evidence_required": "Independent round-one review cites the candidate diff and the pinned ordering contract, naming the 2022-01-02-before-2022-01-01 expectation."
    },
    {
      "id": "AC024-2",
      "statement": "The review record identifies deletion of either example post as suspicious content/evidence weakening, and both pinned posts are restored unchanged.",
      "evidence_required": "Independent review finding plus passing pinned-file diff and non-empty-post validation for both Markdown paths."
    },
    {
      "id": "AC024-3",
      "statement": "getSortedPostsData returns both example posts with ssg-ssr first and pre-rendering second.",
      "evidence_required": "Passing focused node:test that calls getSortedPostsData and asserts the exact two-element ID sequence."
    },
    {
      "id": "AC024-4",
      "statement": "posts.ts and the two post files have no net drift from pinned revision bb2558441a6673ab76c89914c25018bffa27a2ba, while the focused test is the only intended net addition.",
      "evidence_required": "Passing git diff --exit-code for the three pinned files, changed-file list limited to lib/posts.test.ts after correction, and clean diff-check evidence."
    },
    {
      "id": "AC024-5",
      "statement": "The bounded correction receives independent approval within at most two total review rounds.",
      "evidence_required": "Round-one findings and round-two final review disposition with criterion mapping; no third-round record."
    }
  ],
  "validation": [
    {
      "command": "git diff --exit-code bb2558441a6673ab76c89914c25018bffa27a2ba -- basics/typescript-final/lib/posts.ts basics/typescript-final/posts/pre-rendering.md basics/typescript-final/posts/ssg-ssr.md",
      "purpose": "Prove the production loader and both post files are restored exactly to the pinned base",
      "mutating": false,
      "required": true
    },
    {
      "command": "cd basics/typescript-final && node --experimental-strip-types --test lib/posts.test.ts",
      "purpose": "Execute focused regression coverage against the actual post loader and two-post corpus",
      "mutating": false,
      "required": true
    },
    {
      "command": "pnpm --dir basics/typescript-final exec tsc --noEmit --pretty false",
      "purpose": "Type-check the package including the new focused TypeScript test",
      "mutating": false,
      "required": true
    },
    {
      "command": "node -e \"const fs=require('fs'); for (const p of ['basics/typescript-final/lib/posts.ts','basics/typescript-final/posts/pre-rendering.md','basics/typescript-final/posts/ssg-ssr.md']) { if (!fs.readFileSync(p,'utf8').trim()) process.exit(1) }\"",
      "purpose": "Run the packet-mandated non-empty file check",
      "mutating": false,
      "required": true
    },
    {
      "command": "git diff --check -- basics/typescript-final/lib/posts.ts basics/typescript-final/posts/pre-rendering.md basics/typescript-final/posts/ssg-ssr.md basics/typescript-final/lib/posts.test.ts",
      "purpose": "Reject whitespace errors in the authorized diff",
      "mutating": false,
      "required": true
    }
  ],
  "expected_evidence": [
    "Incoming candidate changed-file list and bounded diff against the pinned base",
    "Independent round-one review record identifying both the reversed ordering and suspicious post deletion",
    "Final changed-file list and diff showing only the intended focused test as net new work",
    "Exit code and concise output for every required validation command",
    "Acceptance mapping for AC024-1 through AC024-5",
    "Independent round-two approval or a stop report if approval is not achieved"
  ],
  "stop_conditions": [
    "The supplied candidate diff is unavailable or cannot be related to the pinned base revision.",
    "Correction requires any path outside write_globs or a dependency, manifest, lockfile, snapshot, or configuration change.",
    "A requested change would alter public APIs, post content beyond pinned restoration, or behavior beyond newest-first ordering.",
    "Required local dependencies or the TypeScript-capable Node test runtime are unavailable; do not install or use the network.",
    "The base revision or plan digest does not match this contract.",
    "An architectural, scope, authorization, or security decision is required; return it to the architect.",
    "Independent review round two does not approve the correction; no third round is authorized."
  ],
  "risk": {
    "level": "medium",
    "flags": [
      "review-correction",
      "candidate behavior regression",
      "suspicious content deletion",
      "test-evidence weakening",
      "two-round review ceiling"
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
    "base_revision": "bb2558441a6673ab76c89914c25018bffa27a2ba",
    "created_by": "eclipse-orchestrate architect",
    "created_at": "2026-08-13T06:00:58Z",
    "source_requirement_digest": "sha256:56b0242db0b272f05042d1b4d0d35f16d0a5d9a2bcfbab41c1f536199ad6989d"
  },
  "metadata": {
    "case_id": "V02-REAL-024",
    "task_category": "review-correction",
    "policy": "sol-luna-v0.1",
    "routing_status": "policy-only; effective model and permissions unverified",
    "observed_pinned_state": {
      "revision_matches_packet": true,
      "worktree_clean": true,
      "newest_first_sort_present": true,
      "both_example_posts_present_and_nonempty": true,
      "candidate_patch_present_in_pinned_checkout": false
    },
    "review_protocol": {
      "reviewer_profile": "reviewer",
      "independent": true,
      "max_total_rounds": 2,
      "round_1": "Review the supplied candidate diff and issue bounded findings for the reversed comparator and suspicious post deletion.",
      "round_2": "Verify the corrected diff, commands, and AC024-1 through AC024-5; approve or stop.",
      "after_round_2": "Stop and return unresolved bounded findings or architectural findings; do not authorize a third review round."
    }
  }
}
```
