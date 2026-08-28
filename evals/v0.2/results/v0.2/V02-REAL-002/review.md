```json
{
  "schema_version": "1.0",
  "run_id": "V02-REAL-002",
  "plan_revision": 1,
  "plan_digest": "sha256:69e90b0639959b8be3bf2b74d33222cd7e7b3cc96f9062eea90dbea05a0e7dbd",
  "task_id": "V02-REAL-002-T1",
  "task_contract_digest": "sha256:a798c1ae213ad1860575f7b980205fe2267aa4e1fb4ba7262e95c961af50163d",
  "result_digest": "sha256:3e6fff806ffab56bde359f45d17c788fea9d05858a4e843fa7041fff49f75b56",
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
      "id": "V02-REAL-002-T1-ENV",
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
      "evidence": "Source and test diffs implement the exact nine-byte error, but pytest could not start."
    },
    {
      "criterion_id": "AC2",
      "status": "unverified",
      "evidence": "The existing valid round-trip cases and valid-input expression remain unchanged, but pytest could not start."
    },
    {
      "criterion_id": "AC3",
      "status": "satisfied",
      "evidence": "docs/encoding.rst adds exactly one sentence: bytes_to_int accepts at most eight bytes."
    },
    {
      "criterion_id": "AC4",
      "status": "unsatisfied",
      "evidence": "Required validation exited 1 because pytest is absent; pre/post status lists only the three authorized files."
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
    "case_id": "V02-REAL-002",
    "result_artifact": "result-final.md",
    "actual_diff_scope": "pass",
    "contract_semantics": "pass",
    "reviewer_independence": "logical role separation; mechanical isolation unverified"
  }
}
```
