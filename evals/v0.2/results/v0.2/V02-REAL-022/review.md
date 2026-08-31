```json
{
  "schema_version": "1.0",
  "run_id": "V02-REAL-022",
  "plan_revision": 1,
  "plan_digest": "sha256:2c0e24f23c91ce8efbb30025278e5963186361285bbeed4c9d84686c4975118f",
  "task_id": "V02-REAL-022-T01",
  "task_contract_digest": "sha256:a4e2ece72b6700b0817c74ba693485c5da18542e3a6f4023240677cf9da5f566",
  "result_digest": "sha256:d65c0d159309f4bff9c9a6772fd2d8c0c52a0de6dc7310022d84b13b6d954799",
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
      "evidence": "statusConfig is a typed pending/paid-only mapping and InvoiceStatus selects/configures one Icon without repeated status comparisons."
    },
    {
      "criterion_id": "AC-2",
      "status": "satisfied",
      "evidence": "Pending maps to the exact Pending label, gray pill classes, ClockIcon, and gray icon classes; static expected markup compares the complete output."
    },
    {
      "criterion_id": "AC-3",
      "status": "satisfied",
      "evidence": "Paid maps to the exact Paid label, green/white pill classes, CheckIcon, and white icon classes; static expected markup compares the complete output."
    },
    {
      "criterion_id": "AC-4",
      "status": "satisfied",
      "evidence": "Default export and { status: string } remain unchanged; unsupported output is explicitly covered; post-validation status lists only the authorized component and test files."
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
    "case_id": "V02-REAL-022",
    "result_artifact": "result.md",
    "actual_diff_scope": "pass",
    "contract_semantics": "pass",
    "reviewer_independence": "logical role separation; mechanical isolation unverified"
  }
}
```
