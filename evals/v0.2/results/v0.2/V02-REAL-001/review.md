```json
{
  "schema_version": "1.0",
  "run_id": "V02-REAL-001",
  "plan_revision": 1,
  "plan_digest": "sha256:4e30854d8be881c4d5f005a2cf1a7edea464bd4029ce25145f9b8e9ebb365445",
  "task_id": "V02-REAL-001-T1",
  "task_contract_digest": "sha256:1a9160142241ffe6002c6a15aed9214baa99380b5bf4be5c7a8dc0aac015f740",
  "result_digest": "sha256:f02e66bba0a60048ac0c9ce79fecaffcaeb68db1a4291e6a43362aeeae8c29ae",
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
      "id": "V02-REAL-001-T1-ENV",
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
      "evidence": "Source diff adds the exact ValueError before _int_to_bytes and the focused -1 assertion, but required pytest could not start."
    },
    {
      "criterion_id": "AC2",
      "status": "unverified",
      "evidence": "Existing zero and uint64-max assertions remain unchanged, but required pytest could not start."
    },
    {
      "criterion_id": "AC3",
      "status": "unsatisfied",
      "evidence": "The only required command exited 1 because pytest is unavailable; complete pre/post status lists only the two authorized files."
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
    "case_id": "V02-REAL-001",
    "result_artifact": "result-final.md",
    "actual_diff_scope": "pass",
    "contract_semantics": "pass",
    "reviewer_independence": "logical role separation; mechanical isolation unverified"
  }
}
```
