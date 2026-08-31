```json
{
  "schema_version": "1.0",
  "run_id": "V02-REAL-029",
  "plan_revision": 1,
  "plan_digest": "sha256:1cec5736d271506311fcfd0134266b47d01d36ecf7730d8706efb90f46d2c534",
  "task_id": "V02-REAL-029-T01",
  "task_contract_digest": "sha256:68671dc7de164eb70c9f061e53b56b8eaed46469c5cacd047bbde8bae8b897f9",
  "result_digest": "sha256:4dd2c56529e08763b522c9f1f03d6b18e9391a3adbe35979d705bfa4744da559",
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
      "evidence": "Production calls changesets.sort() after sinceRef and ignored-file filtering; the test mocks reverse/unsorted root and pre readdir results and expects alpha, pre/bravo, pre/charlie, zulu."
    },
    {
      "criterion_id": "AC-2",
      "status": "satisfied",
      "evidence": "Without the new sort, Promise.all would preserve the mocked inherited order zulu, alpha, pre/charlie, pre/bravo, contradicting the exact expected IDs."
    },
    {
      "criterion_id": "AC-3",
      "status": "satisfied",
      "evidence": "Eligibility, sinceRef, parsing/error paths, and default alias are untouched; existing ignored and sinceRef tests remain, and the new test includes ignored README plus pre changesets."
    },
    {
      "criterion_id": "AC-4",
      "status": "satisfied",
      "evidence": "Post-validation status lists exactly packages/read/src/index.ts and index.test.ts."
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
    "case_id": "V02-REAL-029",
    "result_artifact": "result.md",
    "actual_diff_scope": "pass",
    "contract_semantics": "pass",
    "reviewer_independence": "logical role separation; mechanical isolation unverified"
  }
}
```
