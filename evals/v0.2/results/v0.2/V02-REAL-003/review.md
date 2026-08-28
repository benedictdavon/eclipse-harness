```json
{
  "schema_version": "1.0",
  "run_id": "V02-REAL-003",
  "plan_revision": 1,
  "plan_digest": "sha256:0d72877b8a29508b6703311d151e29be603ea9d0cfc731b71124fcfcf8f04118",
  "task_id": "V02-REAL-003-T1",
  "task_contract_digest": "sha256:5be7ea26400ff18dfb9fa8e9dabc43145dd5c4581b71c82a40c080de4904718d",
  "result_digest": "sha256:71c4267b9f1b126a083fbb8356d9be17ed17c2ca23df35f2cc7bf881361dee0f",
  "review_round": 1,
  "outcome": "escalated",
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
  "findings": [
    {
      "id": "V02-REAL-003-T1-ENV",
      "severity": "medium",
      "type": "insufficient-evidence",
      "path": "validation.txt",
      "symbol": null,
      "criterion_id": null,
      "evidence": "Required validation failed: PYTHONPATH=src python -m pytest tests/test_itsdangerous/test_encoding.py -q (exit 1).",
      "impact": "The task cannot be accepted while a required validation command or criterion remains unsatisfied.",
      "correction": "Have the host provide the already-declared repository test environment without changing the candidate patch, then rerun the exact required command. Do not authorize dependency installation through this bounded task.",
      "disposition": "human"
    }
  ],
  "criteria_verdicts": [
    {
      "criterion_id": "AC1",
      "status": "unverified",
      "evidence": "Diff shows strict conversion inside BadData translation and a non-ASCII regression, but pytest could not start."
    },
    {
      "criterion_id": "AC2",
      "status": "unverified",
      "evidence": "Focused assertions cover both valid str and bytes forms, but pytest could not start."
    },
    {
      "criterion_id": "AC3",
      "status": "unsatisfied",
      "evidence": "Required validation exited 1 because pytest is absent; pre/post status lists only authorized files."
    }
  ],
  "validation_summary": "The corrected Task/Result identity chain passes semantic validation and the actual patch is within scope. The worker correctly did not claim completion: at least one declared required command failed because the pinned repository test environment is unavailable.",
  "residual_risk": [
    "The implementation remains unaccepted until the exact required repository validation executes successfully.",
    "Effective model identity and mechanical reviewer read-only enforcement are unverified."
  ],
  "started_at": "2026-08-28T04:20:00Z",
  "finished_at": "2026-08-28T04:22:00Z",
  "metadata": {
    "case_id": "V02-REAL-003",
    "result_artifact": "result-final.md",
    "actual_diff_scope": "pass",
    "contract_semantics": "pass",
    "reviewer_independence": "logical role separation; mechanical isolation unverified"
  }
}
```
