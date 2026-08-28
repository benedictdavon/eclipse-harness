```json
{
  "schema_version": "1.0",
  "run_id": "V02-REAL-028",
  "plan_revision": 1,
  "plan_digest": "sha256:fbed2226b8402b3f34b0fe26ddd0b12879f59d35582420d562f4dac3fadbdc26",
  "task_id": "V02-REAL-028-T01",
  "task_contract_digest": "sha256:7941287cfca1882983e959575f651112c6bae593894c5815efff0ebaf71c37a0",
  "result_digest": "sha256:cbdd1b3fd527246cead6dc34a153bb6bfb6b1089f196a587af46ad13905bbc77",
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
      "evidence": "The return union contains '='; inputs beginning '=' return '='; the table includes =1.0.0 \u2192 =."
    },
    {
      "criterion_id": "AC-2",
      "status": "satisfied",
      "evidence": "Every prior operator/fallback row and production branch remains unchanged."
    },
    {
      "criterion_id": "AC-3",
      "status": "satisfied",
      "evidence": "README lists ^, ~, >=, <=, >, = and states that plain 1.0.0 returns the empty string, matching code/tests."
    },
    {
      "criterion_id": "AC-4",
      "status": "satisfied",
      "evidence": "Deprecated default alias lines remain unchanged; post-validation status lists only the three authorized files."
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
    "case_id": "V02-REAL-028",
    "result_artifact": "result.md",
    "actual_diff_scope": "pass",
    "contract_semantics": "pass",
    "reviewer_independence": "logical role separation; mechanical isolation unverified"
  }
}
```
