# V02-REAL-012 review

Combined case outcome: **escalated**. The two approved tasks have disjoint file ownership and were correctly identified as parallel-safe in isolated worktrees. The host had only one checkout, so it safely serialized task 1 then task 2 (`actual_concurrency=false`) and preserved the declared integration order. The final diff is exactly within the packet's union scope: `app/models.py`, `tests.py`, and `app/templates/errors/404.html`.

The implementation hunks satisfy the frozen source-level decisions, but the packet's third acceptance criterion is not proven. Both workers, and this independent review, hit `ModuleNotFoundError: No module named 'flask'` before any behavioral test or rendered request executed. The packet-required compile command and all scope/whitespace checks pass. Host action is required to supply an authorized, preprovisioned dependency environment and rerun the exact behavioral commands; no implementation correction is requested from the present evidence.

The packet, both task contracts, both result contracts, recorded patch, live checkout diff, changed-file record, and validation record were inspected. Both task/result pairs pass Eclipse schema and semantic binding validation. The recorded patch has the same diff hunks as the live checkout and differs only by one extra terminal newline in the artifact.

## Review Contract — avatar validation

```json
{
  "schema_version": "1.0",
  "run_id": "V02-REAL-012-baseline",
  "plan_revision": 1,
  "plan_digest": "60f8dc183ce8814b02e017f1b62ef0d742e54e829a5b26be9d1d618f8c35090f",
  "task_id": "V02-REAL-012-avatar-validation",
  "task_contract_digest": "sha256:962efe8947cd6a096c6a2e85b0d77bf81ab6f2213418ee46c50171871e46b9ec",
  "result_digest": "sha256:235547ee972695d00f98a520d6dfdf94b872854993a888f7f531f63b96da7f7c",
  "review_round": 1,
  "outcome": "escalated",
  "reviewer_identity": {
    "role": "reviewer",
    "requested_model": "gpt-5.6-sol",
    "effective_model": null,
    "verification": "unavailable"
  },
  "permissions": {
    "desired": "read-only",
    "effective": "unverified",
    "enforcement": "The frozen profile requests a read-only sandbox, but no trusted host metadata proves mechanical enforcement. Review activity was procedurally read-only with respect to the checkout and performed no implementation edits."
  },
  "findings": [
    {
      "id": "R012-AVA-VALIDATION",
      "severity": "medium",
      "type": "insufficient-evidence",
      "path": "tests.py",
      "symbol": "UserModelCase.test_avatar and UserModelCase.test_avatar_size_validation",
      "criterion_id": "AVA-3",
      "evidence": "The worker's focused and full UserModelCase commands exited 1 during module import with ModuleNotFoundError for flask. The reviewer reran both exact commands with PYTHONDONTWRITEBYTECODE=1 and reproduced the same import-time failure; zero requested test methods executed. Compileall and git diff checks exited 0.",
      "impact": "AVA-1 and AVA-2 have strong source and test-design evidence but lack the required passing focused execution, and AVA-3 is unsatisfied because the full pre-existing UserModelCase behavior was not shown green. The stricter public avatar contract therefore cannot be accepted yet.",
      "correction": "Provide a trusted, preprovisioned environment containing the repository's pinned dependencies, then rerun the exact focused avatar command and the full UserModelCase command without network access. Attach unabridged outputs and exit statuses. Do not change the implementation merely to bypass the missing dependency.",
      "disposition": "human"
    }
  ],
  "criteria_verdicts": [
    {
      "criterion_id": "AVA-1",
      "status": "unverified",
      "evidence": "The guard accepts non-bool ints in 1..2048, the unchanged valid path preserves the digest/host/query construction, existing size-128 coverage remains, and new boundary assertions cover 1 and 2048. The criterion explicitly requires passing focused tests, but import failed before execution."
    },
    {
      "criterion_id": "AVA-2",
      "status": "unverified",
      "evidence": "The guard precedes digest construction and rejects bool, non-int values, and out-of-range ints with the exact frozen message. Tests include 0, -1, 2049, true, 128.0, '128', and null equivalents with an anchored exact-message assertion. The required focused test execution did not occur."
    },
    {
      "criterion_id": "AVA-3",
      "status": "unsatisfied",
      "evidence": "Compileall passed with exit 0, but the required full `python -m unittest tests.UserModelCase -v` command exited 1 at import and ran no UserModelCase tests, both for the worker and reviewer."
    },
    {
      "criterion_id": "AVA-4",
      "status": "satisfied",
      "evidence": "The task-local result reports only app/models.py and tests.py, its canonical changed-file digest validates against the task, the focused diff only adds the guard and assertions, the existing avatar assertion is retained, and git diff --check passes."
    }
  ],
  "validation_summary": "Task and result schema/semantic binding validation passed. The live source diff implements the exact type/range/message contract and the new test covers every frozen representative without weakening existing tests. Independent focused avatar and full UserModelCase reruns both exited 1 before test execution because flask is absent. Independent compileall exited 0, git diff --check exited 0, HEAD remains a975ef64864354867c88e0ed3a17ba7d17dca752, and the final checkout contains only the three packet-authorized integrated paths.",
  "residual_risk": [
    "Runtime avatar behavior and all pre-existing UserModelCase behavior remain unverified until the exact commands pass in an authorized dependency-complete environment.",
    "Effective reviewer model identity and mechanical read-only enforcement were not proven by trusted host metadata."
  ],
  "started_at": "2026-08-13T04:55:00Z",
  "finished_at": "2026-08-13T05:00:04Z",
  "metadata": {
    "case_id": "V02-REAL-012",
    "case_outcome": "escalated",
    "actual_concurrency": false,
    "integration_order": 1,
    "packet_criterion_ownership": "satisfied",
    "packet_criterion_concurrency_decision": "satisfied",
    "packet_criterion_both_changes": "unverified",
    "routing_status": "Requested reviewer profile is configuration only; effective routing is unverified."
  }
}
```

## Review Contract — 404 copy

```json
{
  "schema_version": "1.0",
  "run_id": "V02-REAL-012-baseline",
  "plan_revision": 1,
  "plan_digest": "60f8dc183ce8814b02e017f1b62ef0d742e54e829a5b26be9d1d618f8c35090f",
  "task_id": "V02-REAL-012-404-copy",
  "task_contract_digest": "sha256:0c8c323231d48ccf051d2adecbabf5417f55ba87a83b82f48e33fc01aa726078",
  "result_digest": "sha256:19aba69a718e0e363691a5531484e85189a9f558897fec80606cc6be31ee0393",
  "review_round": 1,
  "outcome": "escalated",
  "reviewer_identity": {
    "role": "reviewer",
    "requested_model": "gpt-5.6-sol",
    "effective_model": null,
    "verification": "unavailable"
  },
  "permissions": {
    "desired": "read-only",
    "effective": "unverified",
    "enforcement": "The frozen profile requests a read-only sandbox, but no trusted host metadata proves mechanical enforcement. Review activity was procedurally read-only with respect to the checkout and performed no implementation edits."
  },
  "findings": [
    {
      "id": "R012-ERR-VALIDATION",
      "severity": "medium",
      "type": "insufficient-evidence",
      "path": "app/templates/errors/404.html",
      "symbol": "content block",
      "criterion_id": "ERR-1",
      "evidence": "The worker's exact Flask test-client command exited 1 while importing tests/app with ModuleNotFoundError for flask, before creating a request. The reviewer reran the exact command with PYTHONDONTWRITEBYTECODE=1 and reproduced the same failure. Compileall and all diff checks pass.",
      "impact": "The exact source copy and preserved Jinja expressions are visible statically, but no rendered response proves the 404 status, final body, or recovery link. ERR-1 through ERR-3 therefore lack required direct runtime evidence.",
      "correction": "Provide a trusted, preprovisioned environment containing the repository's pinned dependencies, then rerun the exact explicit-Accept Flask test-client command without network access and attach its unabridged output and exit status. Do not change the template merely to bypass the missing dependency.",
      "disposition": "human"
    }
  ],
  "criteria_verdicts": [
    {
      "criterion_id": "ERR-1",
      "status": "unverified",
      "evidence": "The template contains the exact gettext-wrapped heading and explanatory sentence, but the required explicit text/html render/status assertion never executed."
    },
    {
      "criterion_id": "ERR-2",
      "status": "unverified",
      "evidence": "Source inspection confirms the exact gettext-wrapped link text and preserved url_for('main.index') target. The criterion also requires a passing rendered-body assertion, which did not execute."
    },
    {
      "criterion_id": "ERR-3",
      "status": "unverified",
      "evidence": "The task-local diff changes only the 404 template and preserves its base.html inheritance; handlers and API JSON code are unchanged. The required HTML render/status check did not execute, so runtime routing remains unverified."
    },
    {
      "criterion_id": "ERR-4",
      "status": "satisfied",
      "evidence": "The task-local result reports only app/templates/errors/404.html, its canonical changed-file digest validates against the task, compileall exits 0, and git diff --check passes. The final unfiltered checkout contains only the authorized integrated union after serialized execution."
    }
  ],
  "validation_summary": "Task and result schema/semantic binding validation passed. The live template diff contains exactly the three frozen gettext strings and preserves extends base.html, the content block, and url_for('main.index'); no handler, API, route, base-template, Python, translation, or test file was changed by task 2. The independent Flask render/status command exited 1 before request execution because flask is absent. Independent compileall exited 0 and git diff --check exited 0.",
  "residual_risk": [
    "Rendered HTML status, exact response body, and recovery link remain unverified until the exact test-client command passes in an authorized dependency-complete environment.",
    "The shared checkout forced safe serialized execution rather than the contracts' preferred isolated-worktree concurrency; task 2 accurately disclosed the pre-existing task-1 paths and did not alter them.",
    "Effective reviewer model identity and mechanical read-only enforcement were not proven by trusted host metadata."
  ],
  "started_at": "2026-08-13T04:55:00Z",
  "finished_at": "2026-08-13T05:00:04Z",
  "metadata": {
    "case_id": "V02-REAL-012",
    "case_outcome": "escalated",
    "actual_concurrency": false,
    "integration_order": 2,
    "preexisting_integrated_files": [
      "app/models.py",
      "tests.py"
    ],
    "packet_criterion_ownership": "satisfied",
    "packet_criterion_concurrency_decision": "satisfied",
    "packet_criterion_both_changes": "unverified",
    "routing_status": "Requested reviewer profile is configuration only; effective routing is unverified."
  }
}
```
