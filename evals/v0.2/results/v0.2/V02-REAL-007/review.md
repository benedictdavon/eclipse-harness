```json
{
  "schema_version": "1.0",
  "run_id": "V02-REAL-007",
  "plan_revision": 1,
  "plan_digest": "sha256:5d2e76d82ce27458941cb200f46e59df6b78ee5a2a5ed4dcee5cf5a755375926",
  "task_id": "V02-REAL-007-T1",
  "task_contract_digest": "sha256:3233f02fe621b39b18cfedd54c5dcf1c6b2ec81d708a61a4762c61f8b5b2eec0",
  "result_digest": "sha256:e6670e4442273cf4089647e240d2d1193322b19e666fc138b2790f502626c484",
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
      "evidence": "Source guard raises exact ValueError for size <= 0; focused unittest covers 0 and -1 with exact anchored message."
    },
    {
      "criterion_id": "AC2",
      "status": "satisfied",
      "evidence": "Existing size-128 exact URL assertion and digest/return path remain unchanged after the guard."
    },
    {
      "criterion_id": "AC3",
      "status": "satisfied",
      "evidence": "Exact required compileall command exited 0; complete pre/post status contains only app/models.py and tests.py."
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
    "case_id": "V02-REAL-007",
    "result_artifact": "result-final.md",
    "actual_diff_scope": "pass",
    "contract_semantics": "pass",
    "reviewer_independence": "logical role separation; mechanical isolation unverified"
  }
}
```
