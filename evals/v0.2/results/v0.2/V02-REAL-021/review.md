```json
{
  "schema_version": "1.0",
  "run_id": "V02-REAL-021",
  "plan_revision": 1,
  "plan_digest": "sha256:cfae792f3bf5f25891881fb116cb7c1a64ef576e78acc83a73b15a5ff700439f",
  "task_id": "V02-REAL-021-T01",
  "task_contract_digest": "sha256:642cd0ac32147987fdf1f604930c548406cf4131a1d73b380f0eaf319b077429",
  "result_digest": "sha256:37cbf6897dcb58a1276b4bbfbf76ca57570b9360aeec5d192d235167c9ee248d",
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
      "criterion_id": "AC-1",
      "status": "satisfied",
      "evidence": "The early revenue.length === 0 branch returns exactly { yAxisLabels: ['$0K'], topLabel: 0 }, with a deep-equality regression assertion."
    },
    {
      "criterion_id": "AC-2",
      "status": "satisfied",
      "evidence": "The existing Math.max/Math.ceil/descending loop is unchanged; focused assertions cover a 1500 maximum and an exact 3000 maximum."
    },
    {
      "criterion_id": "AC-3",
      "status": "satisfied",
      "evidence": "generateYAxis remains the same named export and returns the same object keys; complete status lists only the two authorized files."
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
    "case_id": "V02-REAL-021",
    "result_artifact": "result.md",
    "actual_diff_scope": "pass",
    "contract_semantics": "pass",
    "reviewer_independence": "logical role separation; mechanical isolation unverified"
  }
}
```
