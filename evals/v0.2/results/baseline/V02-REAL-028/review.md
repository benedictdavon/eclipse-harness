{
  "schema_version": "1.0",
  "run_id": "V02-REAL-028",
  "plan_revision": 1,
  "plan_digest": "sha256:919f01aa381686f79a092719cb5da56b39c0b1b5bd2156a04a2b30ce1f992342",
  "task_id": "V02-REAL-028-T01",
  "task_contract_digest": "sha256:665119be1366297b703fcdb551541ab07371a9ba5dfb8bb3fc56a1526657b0f5",
  "result_digest": "sha256:97c44ebbd6a622b82444fc851706d6a0e247d367e751621daf62bc644a9ce597",
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
    "enforcement": "No trusted host attestation proved mechanical read-only isolation. The reviewer made no implementation-checkout writes and wrote only this requested review artifact outside the checkout."
  },
  "findings": [
    {
      "id": "V02-REAL-028-R1-F1",
      "severity": "medium",
      "type": "insufficient-evidence",
      "path": "packages/get-version-range-type",
      "criterion_id": "AC-028-1",
      "evidence": "The contract requires passing focused Vitest, project TypeScript, scoped ESLint, and scoped oxfmt checks. Independent replay of all four exact `pnpm exec` commands exited 1 before the requested validator ran: pnpm attempted to install absent workspace dependencies and failed creating `/root/.local`. Both required dependency-free Node checks, direct production-module execution, TypeScript syntax parsing, and `git diff --check` passed, but those supplemental checks do not satisfy the frozen Vitest and TypeScript evidence requirements.",
      "impact": "AC-028-1 through AC-028-4 cannot be accepted under their explicit evidence requirements, and focused-test integration, project type compatibility, lint, and format remain unverified even though no implementation, test-content, documentation, or compatibility defect was found.",
      "correction": "Have the host provide the checkout's already-declared dependencies without changing the task worktree, then rerun all four exact pnpm-backed validations and submit their exit status and relevant output for another review round. Do not install dependencies inside the bounded task.",
      "disposition": "human"
    }
  ],
  "criteria_verdicts": [
    {
      "criterion_id": "AC-028-1",
      "status": "unverified",
      "evidence": "The retained table directly contains the exact `['=1.0.0', '=']` case, and independent execution of the production TypeScript module returned `=` for `=1.0.0`. The required focused Vitest command did not reach Vitest because workspace dependencies are absent."
    },
    {
      "criterion_id": "AC-028-2",
      "status": "unverified",
      "evidence": "The scoped source diff adds only the `=` literal to the explicit `'^' | '~' | '>=' | '<=' | '>' | ''` return union, retaining every prior literal without widening it. Node parsed the TypeScript source and direct runtime assertions passed, but the required project TypeScript command did not reach TypeScript."
    },
    {
      "criterion_id": "AC-028-3",
      "status": "unverified",
      "evidence": "The README names `^`, `~`, `>=`, `<=`, `>`, and `=`, and explicitly states that an unprefixed range returns an empty string; the adjacent table contains the same six operators and unprefixed result. The exact documentation-content check passed, but the required focused Vitest and repository formatter did not run."
    },
    {
      "criterion_id": "AC-028-4",
      "status": "unverified",
      "evidence": "All six original table rows remain byte-for-byte, the source changes only the public union and one leading-`=` branch, and the deprecated default alias is unchanged. Independent execution passed the original operator/fallback cases and named/default reference identity; required Vitest and TypeScript validation remain unavailable."
    },
    {
      "criterion_id": "AC-028-5",
      "status": "satisfied",
      "evidence": "HEAD is the pinned `b4dc91f545ff2afead214278b7b5ebc8d4e96322`. Full tracked, staged, untracked, and ignored inspection reports only modified `README.md`, `src/index.test.ts`, and `src/index.ts` inside `packages/get-version-range-type`; there are no staged, untracked, ignored, metadata, dependency, manifest, or other-package artifacts. The result's changed-file digest is valid and `git diff --check` passed."
    }
  ],
  "validation_summary": "The frozen Task Contract and blocked Result Contract are structurally and semantically valid and canonically hash to `sha256:665119be1366297b703fcdb551541ab07371a9ba5dfb8bb3fc56a1526657b0f5` and `sha256:97c44ebbd6a622b82444fc851706d6a0e247d367e751621daf62bc644a9ce597`; their run, plan, task, base revision, authorized file list, and changed-files digest bindings match. Exact task and staged-result artifact byte digests are `sha256:b638ecd317fcc2bfd18e00148367ec2f433a6190273fc6cda37d33aecd8e31fa` and `sha256:846217401a2156da0584eeaa690ef0bcfc73907de4dd127644a73c7f417edf43`; the packet byte digest matches the provenance digest `sha256:5f3cf947d4496b1b05ad053384b4a038a65d9a8763e5d1981514fe614db880a0`. The host-captured patch equals the live tracked diff plus one terminal blank line; live diff digest is `sha256:47ea774b9885862db4ee777ef5f8ea4fb32f300b4ba3a382f1ab5a2ef6b54489`. Independent inspection found the requested leading-`=` branch, exact public union expansion, complete retained table plus new case, accurate operator/fallback documentation, and unchanged export alias. Both exact dependency-free required commands exited 0. A ten-case direct-runtime sweep, default/named identity assertion, syntax parsing of both TypeScript files, and scoped whitespace check also exited 0. Each exact pnpm-backed command exited 1 before Vitest, TypeScript, ESLint, or oxfmt ran because pnpm attempted to bootstrap missing dependencies and failed creating `/root/.local`; status remained unchanged. No suspicious test weakening, operator-precedence regression, documentation mismatch, scope violation, unauthorized artifact, or security/data/concurrency risk was found.",
  "residual_risk": [
    "Focused Vitest execution and project TypeScript compatibility have not been demonstrated with the repository's declared tools.",
    "Repository ESLint and oxfmt policy have not been executed against the three changed files.",
    "Effective reviewer model, mechanical read-only enforcement, and host isolation were not independently attested."
  ],
  "started_at": "unavailable: no trusted host review start timestamp was provided",
  "finished_at": "2026-08-13T06:56:03Z",
  "metadata": {
    "case_id": "V02-REAL-028",
    "review_budget": "round 1 of 2",
    "base_revision_verified": "b4dc91f545ff2afead214278b7b5ebc8d4e96322",
    "task_file_digest": "sha256:b638ecd317fcc2bfd18e00148367ec2f433a6190273fc6cda37d33aecd8e31fa",
    "result_file_digest": "sha256:846217401a2156da0584eeaa690ef0bcfc73907de4dd127644a73c7f417edf43",
    "packet_file_digest": "sha256:5f3cf947d4496b1b05ad053384b4a038a65d9a8763e5d1981514fe614db880a0",
    "recorded_patch_file_digest": "sha256:2211f110c60d057bac9d320be746c1f035f7bad11e3db02db7e3d1567691d01e",
    "live_tracked_diff_digest": "sha256:47ea774b9885862db4ee777ef5f8ea4fb32f300b4ba3a382f1ab5a2ef6b54489",
    "patch_comparison": "Recorded patch equals the live tracked diff plus one terminal blank line.",
    "independent_behavior_cases": 10,
    "repository_tool_outcome": "Four exact pnpm-backed commands exited 1 before their requested validators ran; both exact dependency-free required commands exited 0."
  }
}

