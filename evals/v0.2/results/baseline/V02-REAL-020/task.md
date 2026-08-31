{
  "schema_version": "1.0",
  "run_id": "V02-REAL-020-baseline",
  "plan_revision": 1,
  "plan_digest": "639465417a0ed083d38958de9abd31eccbfeee1901eb56a10a8a6a1d7a33d855",
  "task_id": "V02-REAL-020-add-overdue-invoice-status",
  "parent_task_id": null,
  "dependencies": [],
  "objective": "Add a typed overdue invoice fixture and a distinct accessible amber overdue pill with an exclamation icon in the dashboard starter, with a focused deterministic rendering check and no change to pending or paid output.",
  "rationale": "The pinned starter stores invoice status literals in three invoice-facing type definitions, seeds statuses from placeholder data, and renders them in one isolated status component. One task owning those three production files and the authorized new test can add the state end to end without changing database schema, forms, queries, dependencies, or unrelated UI.",
  "context_manifest": {
    "schema_version": "1.0",
    "summary": "One bounded cross-layer status addition in the clean pinned Next.js examples checkout. The starter has no configured unit-test runner, so the new focused check must use Node's built-in test API and existing declared TypeScript/React dependencies without changing manifests or lockfiles.",
    "references": [
      {
        "path": "repo/evals/v0.2/results/baseline/V02-REAL-020/packet.json",
        "symbol": null,
        "purpose": "Original requirement, acceptance criteria, pinned revision, exact write scope, and required validation.",
        "digest": "543931e531c375377498a47b49e4965d5198427d606bf5cb104fe18435b0c2a6",
        "trust": "harness"
      },
      {
        "path": "dashboard/starter-example/app/lib/definitions.ts",
        "symbol": "Invoice, InvoicesTable, InvoiceForm",
        "purpose": "Invoice-facing status unions that must represent the new literal consistently.",
        "digest": "d5941685b24ee5e562d5922defb068094096eb4f717c95ee695f8a9415d3ca4e",
        "trust": "repository"
      },
      {
        "path": "dashboard/starter-example/app/lib/placeholder-data.ts",
        "symbol": "invoices",
        "purpose": "Seed fixture array that must include an overdue invoice while retaining pending and paid fixtures.",
        "digest": "24a3f69adce9cbdef636278d85161623dcad04db008372f21f2f6bc9af89e670",
        "trust": "repository"
      },
      {
        "path": "dashboard/starter-example/app/ui/invoices/status.tsx",
        "symbol": "InvoiceStatus",
        "purpose": "Existing pending and paid pill markup and the sole authorized rendering target.",
        "digest": "b1913d318c07bead3925a0a220cc5a1c10f6da3edd8a8a7b3b869a44d06a7cd9",
        "trust": "repository"
      },
      {
        "path": "dashboard/starter-example/package.json",
        "symbol": null,
        "purpose": "Read-only evidence of existing TypeScript, React, React DOM, clsx, and Heroicons dependencies and the absence of a unit-test script.",
        "digest": "e5cdd822022c1340da463cb8d78842814de80d6b4482b803a318c4fd7dc4ac4e",
        "trust": "project-config"
      },
      {
        "path": "dashboard/starter-example/tsconfig.json",
        "symbol": null,
        "purpose": "Read-only strict TypeScript configuration for all authorized TypeScript and TSX files.",
        "digest": "4e6268d243a233e8ce945a54703bbe002dd71ebf183ff285a8b3b1a551c9ce0c",
        "trust": "project-config"
      }
    ],
    "trusted_sources": [
      "Frozen architect prompt",
      "eclipse-orchestrate skill and task-contract schema",
      "V02-REAL-020 acceptance packet"
    ]
  },
  "decisions": {
    "fixed": [
      "The new stored and rendered status literal is exactly 'overdue', and its visible accessible label is exactly 'Overdue'.",
      "Add 'overdue' to the status unions of Invoice, InvoicesTable, and InvoiceForm so all existing invoice-facing data shapes agree; do not change other fields or introduce a broader type refactor.",
      "Change exactly one existing pending fixture's status to 'overdue'. Preserve the fixture array length, every other fixture field, and at least one pending and one paid fixture.",
      "Render overdue with a distinct amber pill using bg-amber-100 and text-amber-800, plus ExclamationCircleIcon from the already-declared Heroicons package.",
      "The word Overdue supplies the accessible name. Mark the exclamation SVG decorative with aria-hidden so it does not duplicate or replace the visible status text.",
      "Preserve the default InvoiceStatus export, its current status prop API, and the existing pending and paid labels, conditions, icons, and class tokens.",
      "Create the authorized status.test.tsx as a deterministic server-rendering check using Node's built-in test/assert APIs, the declared TypeScript compiler, and react-dom/server; do not add a test framework or duplicate a second component implementation."
    ],
    "assumptions": [
      "The packet's 'amber pill' permits the standard Tailwind amber-100 background with amber-800 text and icon treatment.",
      "An overdue fixture is represented most minimally by changing one pending fixture status rather than adding a new invoice and changing aggregate counts.",
      "The VARCHAR invoice status column accepts 'overdue' without a schema change; seed, query, action, and form files remain outside scope.",
      "Configured routing is policy-only; effective model identity, permissions, and cost are unverified by trusted host metadata."
    ]
  },
  "invariants": [
    "Pending renders the visible label Pending, ClockIcon, bg-gray-100, text-gray-500, and its existing shared pill classes.",
    "Paid renders the visible label Paid, CheckIcon, bg-green-500, text-white, and its existing shared pill classes.",
    "Unknown status values retain the component's current empty-pill behavior; no fallback semantics are introduced.",
    "The invoices fixture count, ordering, customer IDs, amounts, and dates remain unchanged.",
    "No database, query, aggregate, action, create/edit form, page, or final-example behavior changes.",
    "The pinned base revision remains bb2558441a6673ab76c89914c25018bffa27a2ba."
  ],
  "non_goals": [
    "Deriving overdue status from invoice dates or current time.",
    "Adding overdue as a create/edit form choice or changing validation and update actions.",
    "Changing pending/paid totals or defining whether overdue contributes to pending aggregates.",
    "Changing InvoiceStatus to a mapping-based refactor, altering its public prop type, or adding a fallback state.",
    "Adding dependencies, package scripts, test-runner configuration, snapshots, or lockfile changes.",
    "Updating the final example, documentation, screenshots, generated output, or unrelated UI."
  ],
  "scope": {
    "write_globs": [
      "dashboard/starter-example/app/lib/definitions.ts",
      "dashboard/starter-example/app/lib/placeholder-data.ts",
      "dashboard/starter-example/app/ui/invoices/status.tsx",
      "dashboard/starter-example/app/ui/invoices/status.test.tsx"
    ],
    "read_globs": [
      "dashboard/starter-example/app/lib/definitions.ts",
      "dashboard/starter-example/app/lib/placeholder-data.ts",
      "dashboard/starter-example/app/lib/data.ts",
      "dashboard/starter-example/app/seed/route.ts",
      "dashboard/starter-example/app/ui/invoices/status.tsx",
      "dashboard/starter-example/app/ui/invoices/table.tsx",
      "dashboard/starter-example/app/ui/invoices/create-form.tsx",
      "dashboard/starter-example/app/ui/invoices/edit-form.tsx",
      "dashboard/starter-example/package.json",
      "dashboard/starter-example/pnpm-lock.yaml",
      "dashboard/starter-example/tsconfig.json"
    ],
    "forbidden_globs": [
      ".git/**",
      ".github/**",
      "dashboard/starter-example/package.json",
      "dashboard/starter-example/pnpm-lock.yaml",
      "dashboard/starter-example/pnpm-workspace.yaml",
      "dashboard/starter-example/tsconfig.json",
      "dashboard/starter-example/app/lib/data.ts",
      "dashboard/starter-example/app/seed/**",
      "dashboard/starter-example/app/ui/invoices/table.tsx",
      "dashboard/starter-example/app/ui/invoices/create-form.tsx",
      "dashboard/starter-example/app/ui/invoices/edit-form.tsx",
      "dashboard/final-example/**",
      "basics/**",
      "seo/**",
      "**/.env*"
    ],
    "shared_interfaces": [
      "Invoice, InvoicesTable, and InvoiceForm status unions",
      "InvoiceStatus default export and rendered state markup",
      "invoices placeholder fixture statuses"
    ],
    "exclusive_resources": [
      "dashboard/starter-example/app/lib/definitions.ts",
      "dashboard/starter-example/app/lib/placeholder-data.ts",
      "dashboard/starter-example/app/ui/invoices/status.tsx",
      "dashboard/starter-example/app/ui/invoices/status.test.tsx"
    ],
    "parallel_safe": false,
    "isolation": "branch"
  },
  "required_capabilities": [
    "TypeScript union maintenance",
    "React server-rendered component testing",
    "accessible status semantics",
    "Tailwind utility preservation",
    "strict scoped-write discipline",
    "criterion evidence reporting"
  ],
  "execution_profile": {
    "role": "worker",
    "capability_tier": "normal-bounded-implementation",
    "cost_tier": "standard",
    "reasoning_effort": "high",
    "preferred_model": "luna",
    "fallback_profiles": [
      "luna-max-for-concrete-local-reasoning-blocker",
      "architect-escalation-for-interface-scope-or-accessibility-change"
    ]
  },
  "implementation_instructions": [
    "Extend only the three existing invoice-facing status unions in definitions.ts with the 'overdue' literal; update the nearby two-value explanatory comment accordingly and avoid unrelated type cleanup.",
    "Change exactly one currently pending invoice fixture to overdue without modifying the fixture's other fields or any other fixture entry.",
    "Import ExclamationCircleIcon alongside the existing icons. Add one overdue class condition and one overdue content branch to InvoiceStatus, keeping the existing shared, pending, and paid markup intact.",
    "Use bg-amber-100 and text-amber-800 on the overdue pill. Render the visible text Overdue and an ExclamationCircleIcon with the existing ml-1 w-4 sizing convention, amber text color, and explicit aria-hidden=true.",
    "Do not replace the conditions with a mapping, change the component signature, add date logic, or touch seed/query/form consumers.",
    "Create status.test.tsx as a Node built-in test entrypoint written so Node can execute it without a new loader. It may transpile the sibling status.tsx in memory with the project's declared TypeScript dependency, evaluate that module, and render it with react-dom/server; it must exercise the real exported component rather than a copied implementation.",
    "In the rendering check, assert overdue has visible Overdue text, amber background/text tokens, one exclamation SVG, and a decorative icon; assert pending and paid retain their exact visible labels, class tokens, and respective clock/check SVG paths or component identities.",
    "Run every required validation, report exit status and concise output, and map direct evidence to AC-01 through AC-05."
  ],
  "acceptance_criteria": [
    {
      "id": "AC-01",
      "statement": "Invoice, InvoicesTable, and InvoiceForm each admit the exact 'overdue' status literal while retaining 'pending' and 'paid'.",
      "evidence_required": "Relevant definitions.ts diff hunks plus a passing strict TypeScript check covering all authorized TS/TSX files."
    },
    {
      "id": "AC-02",
      "statement": "The placeholder invoices contain at least one overdue, pending, and paid entry, with no change to fixture count or non-status fixture values.",
      "evidence_required": "A focused placeholder-data diff showing exactly one pending-to-overdue status change and no other fixture hunk."
    },
    {
      "id": "AC-03",
      "statement": "InvoiceStatus renders overdue as a distinct bg-amber-100/text-amber-800 pill with visible text Overdue and an ExclamationCircleIcon hidden from assistive technology.",
      "evidence_required": "Component diff and passing deterministic server-render assertions for the label, amber tokens, exclamation SVG, and aria-hidden semantics."
    },
    {
      "id": "AC-04",
      "statement": "Pending and paid retain their existing labels, conditional behavior, icon identities, shared pill classes, and state-specific class tokens.",
      "evidence_required": "A minimal component diff that leaves existing pending/paid branches unchanged plus passing server-render assertions for both existing states."
    },
    {
      "id": "AC-05",
      "statement": "The change is confined to the four packet-authorized files and introduces no package, lockfile, configuration, schema, form, query, or unrelated UI change.",
      "evidence_required": "git diff --name-only lists only the four write paths and git diff --check passes."
    }
  ],
  "validation": [
    {
      "command": "node -e \"const fs=require('fs'); for (const p of ['dashboard/starter-example/app/lib/definitions.ts','dashboard/starter-example/app/ui/invoices/status.tsx']) { if (!fs.readFileSync(p,'utf8').trim()) process.exit(1) }\"",
      "purpose": "Run the packet-mandated non-empty production-file validation exactly.",
      "mutating": false,
      "required": true
    },
    {
      "command": "pnpm --dir dashboard/starter-example exec node --test app/ui/invoices/status.test.tsx",
      "purpose": "Run the focused deterministic rendering check for overdue, pending, and paid states without adding a test runner.",
      "mutating": false,
      "required": true
    },
    {
      "command": "pnpm --dir dashboard/starter-example exec tsc --noEmit --incremental false --project tsconfig.json",
      "purpose": "Type-check the status unions, component, fixture, and new test without generating incremental output.",
      "mutating": false,
      "required": true
    },
    {
      "command": "git diff --check -- dashboard/starter-example/app/lib/definitions.ts dashboard/starter-example/app/lib/placeholder-data.ts dashboard/starter-example/app/ui/invoices/status.tsx dashboard/starter-example/app/ui/invoices/status.test.tsx",
      "purpose": "Reject whitespace errors in the exact authorized patch.",
      "mutating": false,
      "required": true
    },
    {
      "command": "git diff --name-only",
      "purpose": "Prove the changed-file set is confined to the four authorized paths.",
      "mutating": false,
      "required": true
    }
  ],
  "expected_evidence": [
    "Base revision and pre-work git status.",
    "Exact changed-file list and concise diff summary.",
    "Relevant diff hunks for all three status unions, the single fixture change, the overdue rendering branch, and the focused rendering check.",
    "Command, exit status, and concise output for every required validation.",
    "A criterion-by-criterion mapping for AC-01 through AC-05.",
    "Any unavailable local dependency or unverified routing/permission assumption explicitly labeled."
  ],
  "stop_conditions": [
    "HEAD is not bb2558441a6673ab76c89914c25018bffa27a2ba or an authorized path has overlapping pre-existing changes.",
    "Implementing or validating the feature appears to require a write outside the four exact write globs.",
    "A database schema, seed route, query, aggregate, action, create/edit form, component API, package manifest, lockfile, or TypeScript configuration change appears necessary.",
    "The rendering check cannot exercise the real component with already-declared local dependencies; do not install a package or enable network access.",
    "Preserving pending and paid output conflicts with the proposed implementation, or accessibility requires a semantic choice beyond the fixed visible-label/decorative-icon design.",
    "Required tools or dependencies are unavailable, an unrelated baseline failure cannot be separated, or any criterion lacks direct evidence after the attempt budget.",
    "Credentials, external effects, destructive actions, generated-file changes, or outbound network access become necessary."
  ],
  "risk": {
    "level": "medium",
    "flags": [
      "cross-layer-status-addition",
      "invoice-type-interface-change",
      "accessibility-regression",
      "existing-state-markup-must-remain-stable",
      "no-configured-test-runner"
    ]
  },
  "complexity": "bounded",
  "budgets": {
    "max_attempts": 2,
    "max_review_rounds": 1
  },
  "authorization": {
    "network": false,
    "credentials": false,
    "external_side_effects": false,
    "destructive_actions": false,
    "targets": [
      "dashboard/starter-example/app/lib/definitions.ts",
      "dashboard/starter-example/app/lib/placeholder-data.ts",
      "dashboard/starter-example/app/ui/invoices/status.tsx",
      "dashboard/starter-example/app/ui/invoices/status.test.tsx"
    ]
  },
  "provenance": {
    "base_revision": "bb2558441a6673ab76c89914c25018bffa27a2ba",
    "created_by": "baseline-eclipse-architect",
    "created_at": "2026-08-13T05:32:47Z",
    "source_requirement_digest": "543931e531c375377498a47b49e4965d5198427d606bf5cb104fe18435b0c2a6"
  },
  "metadata": {
    "case_id": "V02-REAL-020",
    "case_type": "real",
    "task_category": "multi-file-feature",
    "policy": "sol-luna-v0.1",
    "route_verification": "unverified-policy-only",
    "plan_digest_basis": "SHA-256 of canonical JSON containing base_revision, plan_revision, run_id, source_requirement_digest, and ordered task_ids",
    "integration_order": [
      "V02-REAL-020-add-overdue-invoice-status implementation and focused rendering check",
      "read-only acceptance review"
    ]
  }
}

