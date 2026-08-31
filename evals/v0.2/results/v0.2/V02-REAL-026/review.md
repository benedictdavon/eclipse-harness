```json
{
  "schema_version": "1.0",
  "run_id": "V02-REAL-026",
  "plan_revision": 1,
  "plan_digest": "sha256:1dadccd25d3fcda7a98caec29824dc37236313d191e028eca94e943d1d621e63",
  "task_id": "V02-REAL-026-T01",
  "task_contract_digest": "sha256:539aa6bd8d523d109d2e7748e54226c0083ce8760df5ef4c1a171153c2c98d4e",
  "result_digest": "sha256:2a6b5c8122b82e0652653ebba8c0084b740f39a1ebe0622e63d81ec10123cb69",
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
      "evidence": "The source expression requires length > 0 and an empty classifier result; the helper table expects true for 1.0.0."
    },
    {
      "criterion_id": "AC-2",
      "status": "satisfied",
      "evidence": "The helper table expects false for empty input and ^, ~, >=, <=, and > inputs."
    },
    {
      "criterion_id": "AC-3",
      "status": "satisfied",
      "evidence": "The original classifier implementation/table and deprecated default alias lines remain unchanged."
    },
    {
      "criterion_id": "AC-4",
      "status": "satisfied",
      "evidence": "Post-validation status lists exactly the authorized module and test."
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
    "case_id": "V02-REAL-026",
    "result_artifact": "result.md",
    "actual_diff_scope": "pass",
    "contract_semantics": "pass",
    "reviewer_independence": "logical role separation; mechanical isolation unverified"
  }
}
```
