```json
{
  "schema_version": "1.0",
  "run_id": "V02-REAL-009",
  "plan_revision": 1,
  "plan_digest": "sha256:5da16237c46b7b633dd9c9de34a5cff7eb5be28f65a0300054e559bb3d96e957",
  "task_id": "V02-REAL-009-T1",
  "task_contract_digest": "sha256:6c35ff7c469a1f718bebd01958375e15ab31101b60ef394ab542d1d17805e778",
  "result_digest": "sha256:a2085fdabc9a93eb260d977532e35f81e4c18ca3cd5a27fe70e979e6aca77d0a",
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
      "evidence": "Serializer contains explicit None branch and focused persisted-user test asserts the serialized value is None."
    },
    {
      "criterion_id": "AC2",
      "status": "satisfied",
      "evidence": "Original replace(tzinfo=timezone.utc).isoformat() expression is retained and exact test expects 2024-01-02T03:04:05+00:00."
    },
    {
      "criterion_id": "AC3",
      "status": "satisfied",
      "evidence": "Exact compileall command exited 0; pre/post status lists only app/models.py and tests.py."
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
    "case_id": "V02-REAL-009",
    "result_artifact": "result-final.md",
    "actual_diff_scope": "pass",
    "contract_semantics": "pass",
    "reviewer_independence": "logical role separation; mechanical isolation unverified"
  }
}
```
