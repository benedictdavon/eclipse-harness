{
  "schema_version": "1.0",
  "run_id": "V02-REAL-020",
  "plan_revision": 1,
  "plan_digest": "sha256:303d0093692f499f544426f3c053f6045adb24272c49b2d18d89d7acedee4066",
  "task_id": "V02-REAL-020-T01",
  "task_contract_digest": "sha256:1187369093b97133de07b1b26776712f84b22cd53748fb18bf2ab961bc35e155",
  "attempt": 1,
  "status": "complete",
  "worker_identity": {
    "role": "executor",
    "requested_model": "gpt-5.6-luna",
    "configured_model": null,
    "effective_model": null,
    "verification": "unverified"
  },
  "files_changed": [
    "dashboard/starter-example/app/lib/definitions.ts",
    "dashboard/starter-example/app/lib/placeholder-data.ts",
    "dashboard/starter-example/app/ui/invoices/status.test.tsx",
    "dashboard/starter-example/app/ui/invoices/status.tsx"
  ],
  "implementation_summary": "Extended all three starter invoice status unions, changed one fixture to overdue, added an amber Overdue pill with a decorative outline exclamation icon, and added deterministic server-rendering regression tests for overdue/pending/paid.",
  "decisions": [
    "Used ExclamationCircleIcon from the already-declared Heroicons outline entrypoint.",
    "Marked the overdue icon aria-hidden so the visible Overdue label is the sole accessible text."
  ],
  "commands": [
    {
      "command": "node -e \"const fs=require('fs'); for (const p of ['dashboard/starter-example/app/lib/definitions.ts','dashboard/starter-example/app/ui/invoices/status.tsx']) { if (!fs.readFileSync(p,'utf8').trim()) process.exit(1) }\"",
      "purpose": "Frozen packet acceptance validation.",
      "exit_code": 0,
      "outcome": "passed",
      "summary": "No output; both frozen-validation targets were present and non-empty."
    }
  ],
  "criteria_evidence": [
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
  "unresolved_issues": [],
  "blockers": [],
  "deviations": [],
  "observed_risks": [
    "The declared acceptance command checks file presence only; deterministic rendering tests were authored but not executed by the frozen contract."
  ],
  "requested_escalation": null,
  "git": {
    "base_revision": "bb2558441a6673ab76c89914c25018bffa27a2ba",
    "changed_files_digest": "sha256:b2cd899d14fa704fbe41d46971ccd287b6655b7bdc97c0fdaa64cc008eafa112"
  },
  "usage": {
    "quality": "unavailable",
    "input_tokens": null,
    "output_tokens": null,
    "cost": null,
    "currency": null,
    "source": "Trusted host metadata reports usage unavailable."
  },
  "started_at": "2026-08-13T08:47:00Z",
  "finished_at": "2026-08-13T08:48:16Z",
  "metadata": {
    "case_id": "V02-REAL-020",
    "task_bundle_digest": "sha256:0a33a6191f3e25eb86f9bcad648866856521a12c4d5c28983f7da570dd34b68d",
    "pre_validation_status_artifact": "worker-pre-validation-status.txt",
    "post_validation_status_artifact": "worker-post-validation-status.txt"
  }
}
