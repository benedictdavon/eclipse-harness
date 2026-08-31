{
  "schema_version": "1.0",
  "run_id": "V02-REAL-022",
  "plan_revision": 1,
  "plan_digest": "sha256:67f185f55eb073743e01fee877a73529b10fabfd7df03466657b217d8b1d9c6c",
  "task_id": "V02-REAL-022-T1",
  "parent_task_id": null,
  "dependencies": [],
  "objective": "Refactor InvoiceStatus to one typed internal status-to-presentation mapping and add focused drift coverage without changing any observable behavior or exported API.",
  "rationale": "Pending and paid presentation data is duplicated across class and content conditionals; one typed mapping makes the two supported presentations coherent while focused assertions prevent label and class drift.",
  "context_manifest": {
    "schema_version": "1.0",
    "summary": "InvoiceStatus is a default-exported React component with a string status prop and duplicated pending/paid presentation conditionals. The local package has TypeScript but no configured test runner.",
    "references": [
      {
        "path": "dashboard/starter-example/app/ui/invoices/status.tsx",
        "symbol": "InvoiceStatus",
        "purpose": "Sole production implementation target and source of the behavior to preserve",
        "digest": null,
        "trust": "repository"
      },
      {
        "path": "dashboard/starter-example/package.json",
        "symbol": "scripts and dependencies",
        "purpose": "Establishes the available local toolchain and absence of a test framework",
        "digest": null,
        "trust": "project-config"
      },
      {
        "path": "dashboard/starter-example/tsconfig.json",
        "symbol": null,
        "purpose": "Type-checking configuration for the owned example",
        "digest": null,
        "trust": "project-config"
      }
    ],
    "trusted_sources": [
      "V02-REAL-022 acceptance packet",
      "Eclipse architect plan revision 1"
    ]
  },
  "decisions": {
    "fixed": [
      "Keep the default export and exact public prop type { status: string }.",
      "Use one typed internal mapping with exactly the pending and paid keys; each entry owns its label, pill classes, icon component, and icon classes.",
      "Pending remains label Pending, pill classes bg-gray-100 text-gray-500, ClockIcon, and icon classes ml-1 w-4 text-gray-500.",
      "Paid remains label Paid, pill classes bg-green-500 text-white, CheckIcon, and icon classes ml-1 w-4 text-white.",
      "Keep base classes inline-flex items-center rounded-full px-2 py-1 text-xs and preserve the empty status presentation for every other string.",
      "Use dependency-free node:test source-contract coverage; do not add or configure a test framework."
    ],
    "assumptions": [
      "The pinned checkout is clean at bb2558441a6673ab76c89914c25018bffa27a2ba.",
      "The host can provision existing locked dependencies for TypeScript validation without task-authorized network access.",
      "A node:test file containing JS-compatible syntax can execute directly despite the required .tsx filename."
    ]
  },
  "invariants": [
    "Pending and paid render the same label text, icon identity, pill classes, icon classes, order, and wrapper semantics as the base revision.",
    "Unknown status strings continue to render only the base span without status-specific content or classes.",
    "No status or public export is added and the prop is not narrowed to a union.",
    "No package, lockfile, generated output, or unrelated invoice component changes."
  ],
  "non_goals": [
    "Adding status values",
    "Changing visual design or accessibility semantics",
    "Changing callers or shared types",
    "Installing or configuring a test framework",
    "Refactoring other invoice UI"
  ],
  "scope": {
    "write_globs": [
      "dashboard/starter-example/app/ui/invoices/status.tsx",
      "dashboard/starter-example/app/ui/invoices/status.test.tsx"
    ],
    "read_globs": [
      "dashboard/starter-example/app/ui/invoices/**",
      "dashboard/starter-example/package.json",
      "dashboard/starter-example/tsconfig.json"
    ],
    "forbidden_globs": [
      ".git/**",
      ".eclipse/**",
      "**/package.json",
      "**/*lock*",
      "dashboard/final-example/**",
      "basics/**",
      "seo/**"
    ],
    "shared_interfaces": [
      "default export InvoiceStatus({ status }: { status: string }) (signature is read-only)"
    ],
    "exclusive_resources": [
      "dashboard/starter-example/app/ui/invoices/status.tsx",
      "dashboard/starter-example/.next"
    ],
    "parallel_safe": false,
    "isolation": "worktree"
  },
  "required_capabilities": [
    "repository-read",
    "scoped-write",
    "typescript-refactor",
    "node-test-execution",
    "type-checking"
  ],
  "execution_profile": {
    "role": "executor",
    "capability_tier": "bounded-routine",
    "cost_tier": "low",
    "reasoning_effort": "high",
    "preferred_model": "gpt-5.6-luna",
    "fallback_profiles": [
      "manual-bounded-worker"
    ]
  },
  "implementation_instructions": [
    "Create a private typed key/config shape and a single pending/paid mapping; do not export it or change the component signature.",
    "Select at most one mapping entry for the incoming string and render its label and icon from that entry while keeping the base span and current ordering.",
    "Avoid repeated status === 'pending' and status === 'paid' presentation branches; the mapping must be the single source for both class and content selection.",
    "Add status.test.tsx using only node:test, node:assert, and node:fs/URL primitives with JS-compatible syntax. Assert all exact pending and paid labels, pill class fragments, and icon class fragments so any drift fails the test.",
    "Do not add dependencies, change configuration, run formatters over unrelated files, or touch generated output."
  ],
  "acceptance_criteria": [
    {
      "id": "AC-022-1",
      "statement": "A typed internal mapping with exactly pending and paid replaces duplicated status-specific presentation conditionals.",
      "evidence_required": "Scoped diff showing the typed two-entry mapping and a single lookup/render path, plus passing TypeScript validation."
    },
    {
      "id": "AC-022-2",
      "statement": "Pending and paid preserve their exact labels, icon components, pill classes, icon classes, base classes, and ordering.",
      "evidence_required": "Passing focused node:test assertions covering both labels and every exact class fragment, corroborated by the scoped diff."
    },
    {
      "id": "AC-022-3",
      "statement": "The default export, { status: string } prop, supported statuses, and unknown-string behavior do not change.",
      "evidence_required": "Type-check evidence and direct diff review showing no public signature change, new status, or fallback content."
    },
    {
      "id": "AC-022-4",
      "statement": "Only the two authorized status files change and both are non-empty.",
      "evidence_required": "Changed-file list, passing packet file-presence command, and clean git diff check."
    }
  ],
  "validation": [
    {
      "command": "node --test dashboard/starter-example/app/ui/invoices/status.test.tsx",
      "purpose": "Run dependency-free focused drift coverage for labels and classes",
      "mutating": false,
      "required": true
    },
    {
      "command": "pnpm --dir dashboard/starter-example exec tsc --noEmit",
      "purpose": "Verify the typed mapping and unchanged component API compile in the owned example",
      "mutating": false,
      "required": true
    },
    {
      "command": "node -e \"const fs=require('fs'); for (const p of ['dashboard/starter-example/app/ui/invoices/status.tsx','dashboard/starter-example/app/ui/invoices/status.test.tsx']) { if (!fs.readFileSync(p,'utf8').trim()) process.exit(1) }\"",
      "purpose": "Run the acceptance packet's required non-empty-file validation",
      "mutating": false,
      "required": true
    },
    {
      "command": "git diff --check -- dashboard/starter-example/app/ui/invoices/status.tsx dashboard/starter-example/app/ui/invoices/status.test.tsx",
      "purpose": "Reject malformed whitespace in the scoped patch",
      "mutating": false,
      "required": true
    }
  ],
  "expected_evidence": [
    "Exact changed-file list",
    "Scoped diff summary identifying the typed mapping and unchanged default export signature",
    "Focused node:test command and exit code with AC-022-2 mapping",
    "TypeScript command and exit code with AC-022-1 and AC-022-3 mapping",
    "Packet validation and git diff --check exit codes",
    "Criterion-by-criterion evidence map for AC-022-1 through AC-022-4"
  ],
  "stop_conditions": [
    "Completion requires changing any file outside the two write globs.",
    "A dependency, package script, manifest, lockfile, generated file, or network access appears necessary.",
    "Preserving behavior appears to require changing the public prop type, default export, supported statuses, labels, icons, classes, or unknown-string behavior.",
    "The base revision, plan revision, or plan digest does not match this contract.",
    "Existing dependencies required for type-checking are unavailable; report the environment blocker instead of installing them.",
    "Any acceptance criterion lacks direct evidence after two bounded attempts."
  ],
  "risk": {
    "level": "low",
    "flags": [
      "behavior-preserving-refactor",
      "exact-style-contract",
      "public-api-freeze"
    ]
  },
  "complexity": "bounded",
  "budgets": {
    "max_attempts": 2,
    "max_review_rounds": 2
  },
  "authorization": {
    "network": false,
    "credentials": false,
    "external_side_effects": false,
    "destructive_actions": false,
    "targets": []
  },
  "provenance": {
    "base_revision": "bb2558441a6673ab76c89914c25018bffa27a2ba",
    "created_by": "eclipse-architect",
    "created_at": "2026-08-13T05:32:13Z",
    "source_requirement_digest": "sha256:05960458ca0ff0e45c7377e881c8a1f933fc32c4269a194f1678fcef4e2ed391"
  },
  "metadata": {
    "case_id": "V02-REAL-022",
    "policy": "sol-luna-v0.1",
    "routing_verification": "policy-only; effective model unverified",
    "supersedes": []
  }
}

