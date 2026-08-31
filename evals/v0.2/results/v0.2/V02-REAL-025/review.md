```json
{
  "schema_version": "1.0",
  "run_id": "V02-REAL-025",
  "plan_revision": 1,
  "plan_digest": "sha256:056d1d8937a5848e5887fe01dd208cd201c2235fec58e1474d77afd0d5738b04",
  "task_id": "V02-REAL-025-T01",
  "task_contract_digest": "sha256:76c270a51abd61acfab325391a1da866e436197c7057aaa12b35a39f5c9092b6",
  "result_digest": "sha256:c1a442d9a5a56abc0f8356b85d5dc91f5f61ef6eedc4f731b9189bafa080d4d1",
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
      "evidence": "The declared union includes '<', the branch returns '<' for a leading single <, and the table includes ['<1.0.0','<']."
    },
    {
      "criterion_id": "AC-2",
      "status": "satisfied",
      "evidence": "All six pre-existing table rows remain unchanged and ordered; only the new row was appended."
    },
    {
      "criterion_id": "AC-3",
      "status": "satisfied",
      "evidence": "The deprecated default assignment/export is untouched and the test asserts reference identity with the named function."
    },
    {
      "criterion_id": "AC-4",
      "status": "satisfied",
      "evidence": "Post-validation status lists exactly the two authorized source/test files."
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
    "case_id": "V02-REAL-025",
    "result_artifact": "result.md",
    "actual_diff_scope": "pass",
    "contract_semantics": "pass",
    "reviewer_independence": "logical role separation; mechanical isolation unverified"
  }
}
```
