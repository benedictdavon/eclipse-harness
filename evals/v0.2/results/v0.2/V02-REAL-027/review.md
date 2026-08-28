```json
{
  "schema_version": "1.0",
  "run_id": "V02-REAL-027",
  "plan_revision": 1,
  "plan_digest": "sha256:0ff0525cb46efd7c338398cb0b1eb7cb8f7fcc8e5cb527c522f042be841f2f8a",
  "task_id": "V02-REAL-027-T01",
  "task_contract_digest": "sha256:5eea65d784c3bfa454f59489165ec6c8a95da4adfef7fa5646ec3a05c54367c0",
  "result_digest": "sha256:83643004e6cc9e6e34c29c9d2f5769871fb7a595bcd16c8683f760fe9601eca8",
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
      "evidence": "Source returns the three literals/null in fixed order; tests cover both overlap precedence cases, allowed-private missing version, and eligible null."
    },
    {
      "criterion_id": "AC-2",
      "status": "satisfied",
      "evidence": "Every test case compares shouldSkipPackage to reason !== null, and the production wrapper uses exactly that expression."
    },
    {
      "criterion_id": "AC-3",
      "status": "satisfied",
      "evidence": "README documents signature usage, each return meaning, options, precedence, allowed-private nuance, and boolean compatibility."
    },
    {
      "criterion_id": "AC-4",
      "status": "satisfied",
      "evidence": "Post-validation status lists only the authorized source, test, and README; no consumer/dependency files changed."
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
    "case_id": "V02-REAL-027",
    "result_artifact": "result.md",
    "actual_diff_scope": "pass",
    "contract_semantics": "pass",
    "reviewer_independence": "logical role separation; mechanical isolation unverified"
  }
}
```
