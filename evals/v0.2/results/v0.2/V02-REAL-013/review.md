```json
{
  "schema_version": "1.0",
  "run_id": "V02-REAL-013",
  "plan_revision": 1,
  "plan_digest": "sha256:f36e58ca0602c3202f5503489aa20ae64b023aa585d5ba864f7a0783d2ee8d10",
  "task_id": "V02-REAL-013-T1",
  "task_contract_digest": "sha256:4949776225cdb5d7876b6690e12084de30d33a9d38b795c342ef13f16efb7bc9",
  "result_digest": "sha256:0772b76985bb27810f27e3efe719f593996cd4ea3abf0e8c4e620804fb4e67f6",
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
      "evidence": "The exact Error is thrown for -1 and directly asserted."
    },
    {
      "criterion_id": "AC2",
      "status": "satisfied",
      "evidence": "Direct assertions preserve numeric 0 and 4."
    },
    {
      "criterion_id": "AC3",
      "status": "satisfied",
      "evidence": "A representative object preserves limit and method lowercasing; no type file changes."
    },
    {
      "criterion_id": "AC4",
      "status": "satisfied",
      "evidence": "The exact frozen Node command exited 0 and only the two authorized files changed."
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
    "case_id": "V02-REAL-013",
    "result_artifact": "result.md",
    "actual_diff_scope": "pass",
    "contract_semantics": "pass",
    "reviewer_independence": "logical role separation; mechanical isolation unverified"
  }
}
```
