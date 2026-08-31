```json
{
  "schema_version": "1.0",
  "run_id": "V02-REAL-008",
  "plan_revision": 1,
  "plan_digest": "sha256:cea7f3f67a16142c8779081ae9ceb75c8551ade22b1d168961e5d482ae98b52a",
  "task_id": "V02-REAL-008-T1",
  "task_contract_digest": "sha256:cffe4276c851de1a08282703c35d3405c9918ba6e581bece16ba937fc63ec96d",
  "result_digest": "sha256:4cad6d79b2d7554db48c04108779666caa778414e85d5981a737bcac54a913da",
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
      "evidence": "Focused persisted-user test asserts true and false states; authenticated direct, update, and collection routes inject token_auth.current_user()."
    },
    {
      "criterion_id": "AC2",
      "status": "satisfied",
      "evidence": "to_dict defaults viewer to None, guards the field, and test asserts omission without viewer; create_user remains viewer-free."
    },
    {
      "criterion_id": "AC3",
      "status": "satisfied",
      "evidence": "Diff/status is limited to the three authorized Python files and adds response-only logic, no mappings or migrations."
    },
    {
      "criterion_id": "AC4",
      "status": "satisfied",
      "evidence": "Exact compileall command exited 0."
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
    "case_id": "V02-REAL-008",
    "result_artifact": "result-final.md",
    "actual_diff_scope": "pass",
    "contract_semantics": "pass",
    "reviewer_independence": "logical role separation; mechanical isolation unverified"
  }
}
```
