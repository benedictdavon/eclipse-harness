```json
{
  "schema_version": "1.0",
  "run_id": "V02-REAL-014",
  "plan_revision": 1,
  "plan_digest": "sha256:2969279d0fbcca61e07c37675aa918cf758afefdf011fec5c512ed86644da937",
  "task_id": "V02-REAL-014-T1",
  "task_contract_digest": "sha256:a327790673bb51819102f002dc17b526ee2f26411f16c197607b0e5eee846cab",
  "result_digest": "sha256:b6c8b1185a4c3cc64680e0942d7a686ca471f64f1038d0bf6bf7d5a17053015d",
  "review_round": 1,
  "outcome": "accepted",
  "reviewer_identity": {
    "role": "reviewer",
    "requested_model": null,
    "effective_model": null,
    "verification": "unavailable"
  },
  "permissions": {
    "desired": "read-only",
    "effective": "unverified",
    "enforcement": "The reviewer performed logical read-only inspection of the frozen requirement, task/result objects, actual patch, full status, and host validation evidence. Mechanical read-only enforcement was not host-attested."
  },
  "findings": [],
  "criteria_verdicts": [
    {
      "criterion_id": "AC1",
      "status": "satisfied",
      "evidence": "RetryOptions documents optional minimumDelayMs and normalization defaults it to 0."
    },
    {
      "criterion_id": "AC2",
      "status": "satisfied",
      "evidence": "The exact negative-value Error is implemented and asserted."
    },
    {
      "criterion_id": "AC3",
      "status": "satisfied",
      "evidence": "Tests cover the 500 ms lower bound, later exponential 600 ms value, and unchanged custom delay identity/value."
    },
    {
      "criterion_id": "AC4",
      "status": "satisfied",
      "evidence": "Jitter and maxRetryAfter are preserved in direct assertions, source/core is unchanged, and frozen validation exited 0."
    }
  ],
  "validation_summary": "The Task and Result Contracts pass semantic validation and bind to their canonical digests. Host-observed full status matches the actual patch and every changed path is authorized. Every declared required command passed. The actual diff directly supports the criterion evidence; unavailable undeclared or supplemental repository tooling was not treated as a new acceptance gate.",
  "residual_risk": [
    "Effective model identity and mechanical reviewer read-only enforcement are unverified; acceptance relies on observable artifacts and host command evidence.",
    "Where the frozen task made repository-wide tooling supplemental, that tooling remains unavailable and is not represented as having run."
  ],
  "started_at": "2026-08-28T04:20:00Z",
  "finished_at": "2026-08-28T04:22:00Z",
  "metadata": {
    "case_id": "V02-REAL-014",
    "result_artifact": "result.md",
    "actual_diff_scope": "pass",
    "contract_semantics": "pass",
    "reviewer_independence": "logical role separation; mechanical isolation unverified"
  }
}
```
