```json
{
  "schema_version": "1.0",
  "run_id": "V02-REAL-004",
  "plan_revision": 1,
  "plan_digest": "sha256:7510b56e4cabf0a91b31715ba7f9530b2b0462068c533cf6afdc01a1133d94d5",
  "task_id": "V02-REAL-004-T1",
  "task_contract_digest": "sha256:b6a20f35a41075dcba354e75f74ff796342ec21f5b7aa0e30e6f11da5e2bc5b6",
  "result_digest": "sha256:353371d9f4c682ca05de4b87e2ac5f75c44f4d4ea32421c9de26ba544553cf1a",
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
      "id": "V02-REAL-004-T1-ENV",
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
      "status": "satisfied",
      "evidence": "Source diff shows _base64_pad(bytes)->bytes containing exactly string + b'=' * (-len(string) % 4), called once by base64_decode."
    },
    {
      "criterion_id": "AC2",
      "status": "unverified",
      "evidence": "Diff changes only mechanical padding delegation; required tests could not start."
    },
    {
      "criterion_id": "AC3",
      "status": "unsatisfied",
      "evidence": "Required command exited 1 because pytest is absent; pre/post status lists only encoding.py."
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
    "case_id": "V02-REAL-004",
    "result_artifact": "result-final.md",
    "actual_diff_scope": "pass",
    "contract_semantics": "pass",
    "reviewer_independence": "logical role separation; mechanical isolation unverified"
  }
}
```
