{
  "schema_version": "1.0",
  "run_id": "V02-REAL-022",
  "plan_revision": 1,
  "plan_digest": "sha256:2c0e24f23c91ce8efbb30025278e5963186361285bbeed4c9d84686c4975118f",
  "task_id": "V02-REAL-022-T01",
  "task_contract_digest": "sha256:a4e2ece72b6700b0817c74ba693485c5da18542e3a6f4023240677cf9da5f566",
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
    "dashboard/starter-example/app/ui/invoices/status.test.tsx",
    "dashboard/starter-example/app/ui/invoices/status.tsx"
  ],
  "implementation_summary": "Replaced duplicated status comparisons with a compile-time checked two-entry local configuration and one mapping-driven render path; added exact static-markup regression tests for pending, paid, and unsupported strings.",
  "decisions": [
    "Used satisfies Record<'pending' | 'paid', ...> to make the local mapping explicit and exhaustive without narrowing the public string prop.",
    "Indexed the mapping defensively so unsupported strings still render the empty base pill."
  ],
  "commands": [
    {
      "command": "node -e \"const fs=require('fs'); for (const p of ['dashboard/starter-example/app/ui/invoices/status.tsx','dashboard/starter-example/app/ui/invoices/status.test.tsx']) { if (!fs.readFileSync(p,'utf8').trim()) process.exit(1) }\"",
      "purpose": "Frozen packet acceptance validation.",
      "exit_code": 0,
      "outcome": "passed",
      "summary": "No output; production and focused test files were present and non-empty."
    }
  ],
  "criteria_evidence": [
    {
      "criterion_id": "AC-1",
      "status": "satisfied",
      "evidence": "statusConfig is a typed pending/paid-only mapping and InvoiceStatus selects/configures one Icon without repeated status comparisons."
    },
    {
      "criterion_id": "AC-2",
      "status": "satisfied",
      "evidence": "Pending maps to the exact Pending label, gray pill classes, ClockIcon, and gray icon classes; static expected markup compares the complete output."
    },
    {
      "criterion_id": "AC-3",
      "status": "satisfied",
      "evidence": "Paid maps to the exact Paid label, green/white pill classes, CheckIcon, and white icon classes; static expected markup compares the complete output."
    },
    {
      "criterion_id": "AC-4",
      "status": "satisfied",
      "evidence": "Default export and { status: string } remain unchanged; unsupported output is explicitly covered; post-validation status lists only the authorized component and test files."
    }
  ],
  "unresolved_issues": [],
  "blockers": [],
  "deviations": [],
  "observed_risks": [
    "The exact rendering tests were authored but the frozen contract only requires a non-empty-file check."
  ],
  "requested_escalation": null,
  "git": {
    "base_revision": "bb2558441a6673ab76c89914c25018bffa27a2ba",
    "changed_files_digest": "sha256:3c3789f439f3dcec6bf24aff4af11692a70d31121a1e8503951d413c573571a1"
  },
  "usage": {
    "quality": "unavailable",
    "input_tokens": null,
    "output_tokens": null,
    "cost": null,
    "currency": null,
    "source": "Trusted host metadata reports usage unavailable."
  },
  "started_at": "2026-08-13T08:49:45Z",
  "finished_at": "2026-08-13T08:51:04Z",
  "metadata": {
    "case_id": "V02-REAL-022",
    "task_bundle_digest": "sha256:78fcc944bd3dd8bf3e9336994235701a358c75e0b53d0bf7b7693784b3698492",
    "pre_validation_status_artifact": "worker-pre-validation-status.txt",
    "post_validation_status_artifact": "worker-post-validation-status.txt"
  }
}
