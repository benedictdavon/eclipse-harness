{
  "schema_version": "1.0",
  "run_id": "V02-REAL-022",
  "plan_revision": 1,
  "plan_digest": "sha256:67f185f55eb073743e01fee877a73529b10fabfd7df03466657b217d8b1d9c6c",
  "task_id": "V02-REAL-022-T1",
  "task_contract_digest": "sha256:bd3c3e6f371271ab59ea5b8f774b15b295ffe9bd7bbd87e36159cd1da6537822",
  "result_digest": "sha256:5314685fdd7e1b12f76dcc471a239639cb487d9f00fbcac93528ba15d4e72517",
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
    "enforcement": "The review was conducted without repository mutation, but no trusted host attestation proved mechanical read-only enforcement."
  },
  "findings": [
    {
      "id": "F-022-1",
      "severity": "medium",
      "type": "insufficient-evidence",
      "path": "dashboard/starter-example/app/ui/invoices/status.tsx",
      "symbol": "InvoiceStatus",
      "criterion_id": "AC-022-1",
      "evidence": "The exact required command `pnpm --dir dashboard/starter-example exec tsc --noEmit` exited 1 before compilation because pnpm attempted unavailable environment provisioning. The Result Contract consequently marks AC-022-1 and AC-022-3 not-tested. Direct source review supports the intended mapping and unchanged signature, but cannot substitute for the contract-required compiler evidence.",
      "impact": "Type compatibility of the new mapping and unchanged public component API is not established, so the task cannot be accepted.",
      "correction": "Provide a clean environment with the already-declared dependencies preprovisioned, without network access or repository mutation, rerun the exact TypeScript command, and issue fresh result evidence. If compilation reveals a code error, route only that bounded correction to the worker.",
      "disposition": "human"
    },
    {
      "id": "F-022-2",
      "severity": "medium",
      "type": "insufficient-evidence",
      "path": "evals/v0.2/results/baseline/V02-REAL-022/patch.diff",
      "symbol": null,
      "criterion_id": "AC-022-4",
      "evidence": "The changed-file list and live run tree identify `status.test.tsx` as an untracked task output, but `patch.diff` contains only the tracked `status.tsx` edit and no content for the new test. Moreover, `git diff --check -- .../status.test.tsx` does not inspect an untracked file, so its exit 0 does not establish the claimed whitespace check for that output. The reviewer could inspect the live file, but the recorded exact-diff artifact is incomplete.",
      "impact": "The durable review packet does not fully represent the result's two-file change, so the claimed focused coverage cannot be independently reconstructed from the actual-patch artifact and its whitespace validation is overstated.",
      "correction": "Regenerate the recorded patch so it includes the complete new `status.test.tsx` content as well as the production edit, then bind any refreshed result/review evidence to the exact complete artifacts.",
      "disposition": "worker"
    }
  ],
  "criteria_verdicts": [
    {
      "criterion_id": "AC-022-1",
      "status": "unverified",
      "evidence": "Direct review finds one private `Record<InvoiceStatusKey, StatusPresentation>` with exactly pending and paid and one guarded presentation lookup/render path; the declared required TypeScript corroboration did not run."
    },
    {
      "criterion_id": "AC-022-2",
      "status": "satisfied",
      "evidence": "The live source preserves Pending/ClockIcon/gray pill and icon classes, Paid/CheckIcon/green pill and white icon classes, the exact shared base classes, and label-before-icon ordering. Independent review reran `node --test dashboard/starter-example/app/ui/invoices/status.test.tsx`: all 3 tests passed."
    },
    {
      "criterion_id": "AC-022-3",
      "status": "unverified",
      "evidence": "Direct diff and live-source review show the unchanged default export and `{ status: string }` prop, no new status, and an own-property guard preserving the empty fallback for every other string. Required TypeScript validation is nevertheless absent."
    },
    {
      "criterion_id": "AC-022-4",
      "status": "satisfied",
      "evidence": "Live `git status --short` at the pinned revision shows only modified `status.tsx` and untracked `status.test.tsx`; both are non-empty and the packet presence command passed. The scoped `git diff --check` exited 0 for the tracked production diff but did not inspect the untracked test. The separate incomplete-patch finding prevents overall acceptance."
    }
  ],
  "validation_summary": "Task and Result Contracts are schema-valid and their canonical digests match the declared binding. Host-observed validation only proves the two authorized files are non-empty. The reviewer independently reran the focused node:test (3/3 passed), the file-presence command (passed), and the declared scoped git diff check (exit 0), and confirmed the live status is scope-compliant; however, git diff did not inspect the untracked test. The required TypeScript command failed before compilation in the worker run and could not establish AC-022-1 or AC-022-3. The recorded patch also omits the untracked test file.",
  "residual_risk": [
    "TypeScript compatibility remains unknown until the exact required compiler command runs in a preprovisioned environment.",
    "The durable patch artifact is incomplete even though the live run tree contains the test.",
    "Effective reviewer model identity and mechanical read-only enforcement were not host-observed."
  ],
  "started_at": "unavailable: no trusted host review-start timestamp was provided",
  "finished_at": "2026-08-13T05:53:24Z",
  "metadata": {
    "case_id": "V02-REAL-022",
    "review_scope": "exact task/result binding, live run tree, recorded patch, changed-file list, and validation evidence",
    "independent_validation": {
      "focused_node_test_exit_code": 0,
      "focused_node_test_passed": 3,
      "presence_exit_code": 0,
      "diff_check_exit_code": 0
    }
  }
}
