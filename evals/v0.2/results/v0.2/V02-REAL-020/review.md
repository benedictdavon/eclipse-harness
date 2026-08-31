```json
{
  "schema_version": "1.0",
  "run_id": "V02-REAL-020",
  "plan_revision": 1,
  "plan_digest": "sha256:303d0093692f499f544426f3c053f6045adb24272c49b2d18d89d7acedee4066",
  "task_id": "V02-REAL-020-T01",
  "task_contract_digest": "sha256:1187369093b97133de07b1b26776712f84b22cd53748fb18bf2ab961bc35e155",
  "result_digest": "sha256:bd47b127910b81e7da497844a2ebfb7bbd470044f3f3de49eac4e79cc27702ea",
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
      "evidence": "Invoice, InvoicesTable, and InvoiceForm now include overdue; exactly one existing invoice fixture changed from pending to overdue."
    },
    {
      "criterion_id": "AC-2",
      "status": "satisfied",
      "evidence": "InvoiceStatus has a dedicated bg-amber-100/text-amber-700 branch and visible Overdue text plus aria-hidden ExclamationCircleIcon; deterministic render assertions cover all properties."
    },
    {
      "criterion_id": "AC-3",
      "status": "satisfied",
      "evidence": "Existing pending/paid conditional markup, labels, icons, and classes are unchanged, and the focused test source asserts their rendered output."
    },
    {
      "criterion_id": "AC-4",
      "status": "satisfied",
      "evidence": "Post-validation status contains only the four authorized files; no package, lockfile, final-example, or unrelated UI changes exist."
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
    "case_id": "V02-REAL-020",
    "result_artifact": "result.md",
    "actual_diff_scope": "pass",
    "contract_semantics": "pass",
    "reviewer_independence": "logical role separation; mechanical isolation unverified"
  }
}
```
