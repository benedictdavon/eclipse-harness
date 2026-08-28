```json
{
  "schema_version": "1.0",
  "run_id": "V02-REAL-016",
  "plan_revision": 1,
  "plan_digest": "sha256:dcc4b5090331d8ea56a8694385d94729156f8aae815e2c114eae50436d57771b",
  "task_id": "V02-REAL-016-T01",
  "task_contract_digest": "sha256:d8e7297629d67ebb493b9935feca943a295d3f39fdd2fbcbfb1fd2d99833af13",
  "result_digest": "sha256:33f106589e1bb30d33e10514566ae224d42fa53cbf7e5e3cd0d98e750b13cab3",
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
      "evidence": "source/utils/normalize.ts now contains one private validateRetryOption helper called once for methods and once for statusCodes; git status lists only the two authorized files."
    },
    {
      "criterion_id": "AC-2",
      "status": "satisfied",
      "evidence": "The helper constructs the unchanged retry.methods/retry.statusCodes messages, and test/retry.ts asserts both exact strings; required frozen validation passed."
    },
    {
      "criterion_id": "AC-3",
      "status": "satisfied",
      "evidence": "The patch leaves numeric shorthand, defaultRetryOptions, undefined filtering, method lower-casing, and the returned merge unchanged; required frozen validation passed."
    },
    {
      "criterion_id": "AC-4",
      "status": "satisfied",
      "evidence": "Post-validation status contains only source/utils/normalize.ts and test/retry.ts; no exports, public types, dependencies, or configuration were changed."
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
    "case_id": "V02-REAL-016",
    "result_artifact": "result.md",
    "actual_diff_scope": "pass",
    "contract_semantics": "pass",
    "reviewer_independence": "logical role separation; mechanical isolation unverified"
  }
}
```
