```json
{
  "schema_version": "1.0",
  "run_id": "V02-REAL-010",
  "plan_revision": 1,
  "plan_digest": "sha256:ecbaf3b1e425f571ccb9915297582a25052724d1ad70c37a28aa21ba4c574390",
  "task_id": "V02-REAL-010-T1",
  "task_contract_digest": "sha256:350baf926ce0fad85ed2171d8967e003b1b71465380e3ad01e5d0ab6fb5b7f25",
  "result_digest": "sha256:caf3b6acc75bfd54afb8c8427270e8ff0763bbeea3ce758ccb402b1043b961d4",
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
      "evidence": "Model diff has one _relationship_count helper and three narrow delegates."
    },
    {
      "criterion_id": "AC2",
      "status": "satisfied",
      "evidence": "Existing follower/following assertions remain; direct u1.posts_count()==1 assertion added; each delegate retains its original .select()."
    },
    {
      "criterion_id": "AC3",
      "status": "satisfied",
      "evidence": "Only app/models.py and tests.py changed; helper counts the supplied scoped Select subquery without mapping or query broadening."
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
    "case_id": "V02-REAL-010",
    "result_artifact": "result-final.md",
    "actual_diff_scope": "pass",
    "contract_semantics": "pass",
    "reviewer_independence": "logical role separation; mechanical isolation unverified"
  }
}
```
