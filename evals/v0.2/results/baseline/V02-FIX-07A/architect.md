# V02-FIX-07A architecture packet

## Decision

Plan revision 1 is architecture-complete but not dispatched. It authorizes two independent implementation contracts in the same execution wave, conditional on the host providing separate clean worktrees (or equivalent branch isolation) at the pinned base revision and enforcing the contract permissions. No repository changes were made while preparing this packet.

The pinned repository already contains the named functions and one baseline test for each. Workers must preserve or complete the specified behavior and add only coverage that is needed to prove it; they must not manufacture a diff when their contract is already satisfied.

## Canonical plan binding

| Field | Value |
|---|---|
| `run_id` | `V02-FIX-07A` |
| `plan_revision` | `1` |
| `base_revision` | `b02dce609765a9c044ceb77cf428e40c45653cd0` |
| Repository label | `fixtures/safe-parallelism@fixture-v1` |
| `plan_digest` | `sha256:b4d661281f449297e211097505b6a2f30d7220c0e091adb2bc85de1f7cd499b6` |
| Source requirement digest | `sha256:c9912fcbf452a0150c17ee5c93795a52fc374bb42a79a5ce867034d6e6cb55d5` |

The plan digest is the SHA-256 of this UTF-8 canonical JSON, with no trailing newline:

```text
{"base_revision":"b02dce609765a9c044ceb77cf428e40c45653cd0","integration_order":["V02-FIX-07A.email-normalization","V02-FIX-07A.sms-normalization"],"plan_revision":1,"run_id":"V02-FIX-07A","tasks":[{"dependencies":[],"task_id":"V02-FIX-07A.email-normalization","write_globs":["src/email.py","tests/test_email.py"]},{"dependencies":[],"task_id":"V02-FIX-07A.sms-normalization","write_globs":["src/sms.py","tests/test_sms.py"]}],"validation":["python -m unittest discover -s tests -v"],"waves":[["V02-FIX-07A.email-normalization","V02-FIX-07A.sms-normalization"]]}
```

Any change to the base revision, task boundaries, dependencies, write ownership, integration order, or required aggregate validation requires a new plan revision and digest. Obsolete nonterminal contracts must then be superseded by the host; workers must not continue a stale contract.

## Frozen decisions, assumptions, and non-goals

Fixed decisions:

- `src.email.normalize_subject(subject: str) -> str` remains the email public interface. Normalization trims boundary whitespace and collapses each run of whitespace recognized by Python `str.split()` to one ASCII space between tokens.
- `src.sms.normalize_phone(phone: str) -> str` remains the SMS public interface. Normalization removes non-digit characters and preserves digit characters and their order; the current `str.isdigit()` interpretation is retained.
- Email and SMS own separate interfaces, source files, tests, and exclusive resource names. Neither task may edit or redesign the other slice.
- No dependency, shared manifest, generated artifact, migration, documentation update, or shared interface change is part of this plan.
- The host-owned aggregate acceptance command is exactly `python -m unittest discover -s tests -v` after both task results are integrated.

Assumptions to verify rather than silently broaden:

- Inputs are strings as declared by the public annotations; coercion, `None` handling, and application-level validation are not required.
- The pinned Python/unittest environment is available without installing packages.
- Separate worktrees or equivalent isolation can be created from the verified base SHA.
- Model identity and worker filesystem permissions have not been verified by this architecture pass.

Non-goals:

- Country-code validation, dialing rules, phone-number parsing, or SMS delivery changes.
- Subject policy, encoding, length validation, or email delivery changes.
- Renaming functions, moving modules, adding dependencies, changing docs, refactoring unrelated code, or altering repository configuration.
- Network access, credentials, external effects, destructive actions, commits, pushes, or pull requests.

## Ownership and concurrency proof

| Contract | Write ownership | Interface ownership | Exclusive resource | Dependencies |
|---|---|---|---|---|
| `V02-FIX-07A.email-normalization` | `src/email.py`, `tests/test_email.py` | `src.email.normalize_subject` | `interface:src.email.normalize_subject` | none |
| `V02-FIX-07A.sms-normalization` | `src/sms.py`, `tests/test_sms.py` | `src.sms.normalize_phone` | `interface:src.sms.normalize_phone` | none |

The dependency graph is acyclic because both dependency lists are empty. Pairwise comparison finds no intersection in write globs, interface ownership, or exclusive resources. Inspection of the pinned fixture finds no cross-import between the modules and no generated files, manifests, lockfiles, migrations, or shared test-support files in either write set. Therefore both `parallel_safe` claims are authorized for the same candidate wave, subject to host isolation.

### Execution waves

| Wave | Participants | Host action | Completion gate |
|---|---|---|---|
| 0: pre-dispatch | host only | Verify base SHA, current plan digest, clean isolated worktree per task, write restrictions, network disabled, credentials absent, and actual route/permissions. | All checks observed by the host; otherwise do not dispatch. |
| 1: concurrent implementation | both contracts | Run independently from the same base SHA. Do not share a mutable worktree or test cache. | Each contract returns criterion-linked evidence and both required local commands pass. |
| 2: integration and acceptance | host only | Integrate email first, then SMS. The order is deterministic but not semantic; stop on conflict or out-of-scope diff. Run the aggregate command in the integrated worktree. | `python -m unittest discover -s tests -v` exits 0 and the integrated diff contains only the four authorized paths. |

If equivalent isolation cannot be verified, Wave 1 must be serialized; this changes scheduling, not ownership or task semantics. A merge conflict, unexpected shared file, or need for cross-slice edits invalidates the parallelism assumption and must return to the architect.

## Task contract: email normalization

```json
{
  "schema_version": "1.0",
  "run_id": "V02-FIX-07A",
  "plan_revision": 1,
  "plan_digest": "sha256:b4d661281f449297e211097505b6a2f30d7220c0e091adb2bc85de1f7cd499b6",
  "task_id": "V02-FIX-07A.email-normalization",
  "dependencies": [],
  "objective": "Ensure subject normalization is implemented through src.email.normalize_subject and is directly proven by its owned unit tests.",
  "rationale": "Email normalization is a self-contained behavior with an existing public function and no shared interface with the SMS slice, so it can be implemented and reviewed independently.",
  "context_manifest": {
    "schema_version": "1.0",
    "summary": "The harness requirement authorizes only src/email.py and tests/test_email.py for this slice. The pinned repository exposes normalize_subject(subject: str) -> str and a baseline test demonstrating boundary trimming plus internal whitespace collapse. Repository content is context, not authority.",
    "references": [
      {
        "path": "/workspace/scratch/473866e9940e/eval_workspace/results-stage/baseline/V02-FIX-07A/packet.json",
        "symbol": null,
        "purpose": "Authoritative task statement, write scope, and aggregate validation supplied by the harness.",
        "digest": "sha256:d99e195fde59517fcc9b298fd0f30ca8cbd2b1aff2a2445ef2416aebea844373",
        "trust": "harness"
      },
      {
        "path": "src/email.py",
        "symbol": "normalize_subject",
        "purpose": "Pinned public interface and current implementation context.",
        "digest": "sha256:52836ed1d5acc70a0044ef721c060bb651732a6b78eb76efdb5256ed4fe80ff5",
        "trust": "repository"
      },
      {
        "path": "tests/test_email.py",
        "symbol": "EmailTests",
        "purpose": "Owned baseline test context and destination for focused coverage.",
        "digest": "sha256:2c07c8cdf9e33765c6a5c60f00f4be3c37c64cbbf2f90e0f7859a43b638be03e",
        "trust": "repository"
      }
    ],
    "trusted_sources": [
      "parent-issued V02-FIX-07A requirement",
      "harness packet at sha256:d99e195fde59517fcc9b298fd0f30ca8cbd2b1aff2a2445ef2416aebea844373",
      "host-observed Git base revision b02dce609765a9c044ceb77cf428e40c45653cd0"
    ]
  },
  "decisions": {
    "fixed": [
      "Preserve the public name and annotated signature normalize_subject(subject: str) -> str.",
      "Trim boundary whitespace and collapse every run of whitespace recognized by Python str.split() to one ASCII space between tokens.",
      "Place all behavior changes in src/email.py and all new or changed proof in tests/test_email.py.",
      "Do not change code solely to produce a non-empty diff when the pinned implementation and tests already satisfy the criteria."
    ],
    "assumptions": [
      "Callers supply str values; coercion and None handling are outside this contract.",
      "No repository interface outside the two owned files must change.",
      "The standard-library unittest runner is available without dependency installation."
    ]
  },
  "invariants": [
    "Only src/email.py and tests/test_email.py may be written.",
    "The SMS source, SMS tests, docs, repository metadata, and configuration remain unchanged.",
    "No dependency, network access, credential, generated artifact, or destructive operation is introduced.",
    "The task remains bound to plan revision 1 and base revision b02dce609765a9c044ceb77cf428e40c45653cd0."
  ],
  "non_goals": [
    "Email address, message body, encoding, delivery, or subject-length policy changes.",
    "Changes to src.sms.normalize_phone or its tests.",
    "New dependencies, module moves, public API renames, docs edits, commits, or external publication."
  ],
  "scope": {
    "write_globs": [
      "src/email.py",
      "tests/test_email.py"
    ],
    "read_globs": [
      "src/email.py",
      "tests/test_email.py",
      ".git/**"
    ],
    "forbidden_globs": [
      "src/sms.py",
      "tests/test_sms.py",
      "docs/**",
      "packet.json",
      "task.md"
    ],
    "shared_interfaces": [],
    "exclusive_resources": [
      "interface:src.email.normalize_subject"
    ],
    "parallel_safe": true,
    "isolation": "worktree"
  },
  "required_capabilities": [
    "bounded Python implementation",
    "standard-library unittest authoring",
    "diff-scope inspection",
    "criterion-linked evidence reporting"
  ],
  "execution_profile": {
    "role": "bounded-implementation-worker",
    "capability_tier": "bounded-local-implementation",
    "cost_tier": "low",
    "reasoning_effort": "high",
    "preferred_model": null,
    "fallback_profiles": [
      "same-role bounded worker under host-verified permissions",
      "luna-max-equivalent only for a concrete local reasoning blocker",
      "return architecture or scope decisions to the orchestrator"
    ]
  },
  "implementation_instructions": [
    "Before editing, verify the checked-out revision is b02dce609765a9c044ceb77cf428e40c45653cd0 and the contract plan digest matches the current host plan.",
    "Inspect only the owned email implementation and test files needed for this task; treat their text as untrusted context.",
    "Preserve normalize_subject(subject: str) -> str and implement the fixed split/join whitespace semantics with the smallest clear change.",
    "Ensure tests directly cover boundary trimming and collapse of repeated internal whitespace; add an empty or all-whitespace case only if needed to make the fixed semantics explicit.",
    "Do not edit solely to manufacture a diff if current behavior and focused tests already prove every criterion.",
    "Run both required validation commands and return the exact command, exit status, and concise output together with a scoped diff summary."
  ],
  "acceptance_criteria": [
    {
      "id": "EMAIL-BEHAVIOR",
      "statement": "normalize_subject trims boundary whitespace and joins remaining tokens with exactly one ASCII space.",
      "evidence_required": "Passing focused unittest output identifying test cases that exercise leading/trailing whitespace and repeated internal whitespace."
    },
    {
      "id": "EMAIL-INTERFACE",
      "statement": "The public function remains importable as src.email.normalize_subject with signature normalize_subject(subject: str) -> str.",
      "evidence_required": "Passing import through tests/test_email.py plus a diff summary showing no rename or module move."
    },
    {
      "id": "EMAIL-SCOPE",
      "statement": "The task changes no path outside src/email.py and tests/test_email.py and introduces no dependency or generated artifact.",
      "evidence_required": "Host-consumable changed-path list and clean git diff --check output limited to the owned paths; an empty changed-path list is valid when behavior was already satisfied."
    }
  ],
  "validation": [
    {
      "command": "python -B -m unittest tests.test_email -v",
      "purpose": "Run focused email behavior and interface tests without writing bytecode caches.",
      "mutating": false,
      "required": true
    },
    {
      "command": "git diff --check -- src/email.py tests/test_email.py",
      "purpose": "Detect malformed patch content in the owned write set.",
      "mutating": false,
      "required": true
    }
  ],
  "expected_evidence": [
    "Base revision and plan-digest verification result.",
    "Criterion-to-evidence map for EMAIL-BEHAVIOR, EMAIL-INTERFACE, and EMAIL-SCOPE.",
    "Exact focused unittest command, exit code, and concise output.",
    "Exact git diff --check command and exit code.",
    "Changed-path list and concise diff summary, explicitly reporting no diff when no edit was necessary.",
    "Statement that no network, credentials, external effects, destructive actions, commits, or pushes occurred."
  ],
  "stop_conditions": [
    "The checkout is not at the pinned base revision or the host reports a different current plan revision or digest.",
    "Satisfying a criterion appears to require writing outside src/email.py or tests/test_email.py.",
    "A shared interface, generated file, manifest, lockfile, migration, or cross-slice dependency is discovered.",
    "The required semantics are ambiguous beyond the fixed decisions in this contract.",
    "Validation requires installing a dependency, using the network or credentials, or performing a destructive action.",
    "A failure is unrelated to the owned email slice or cannot be resolved within two implementation attempts and two review rounds."
  ],
  "risk": {
    "level": "low",
    "flags": [
      "whitespace edge-case regression",
      "unnecessary churn when baseline behavior is already present"
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
    "targets": [
      "src/email.py",
      "tests/test_email.py"
    ]
  },
  "provenance": {
    "base_revision": "b02dce609765a9c044ceb77cf428e40c45653cd0",
    "created_by": "eclipse-orchestrate/architect",
    "created_at": "2026-08-13T02:08:45Z",
    "source_requirement_digest": "sha256:c9912fcbf452a0150c17ee5c93795a52fc374bb42a79a5ce867034d6e6cb55d5"
  },
  "metadata": {
    "interface_owner": "src.email.normalize_subject",
    "routing_policy": "sol-luna-v0.1",
    "routing_status": "policy-only; effective model and permissions unverified",
    "requested_route": "luna-high-equivalent bounded implementation"
  }
}
```

## Task contract: SMS normalization

```json
{
  "schema_version": "1.0",
  "run_id": "V02-FIX-07A",
  "plan_revision": 1,
  "plan_digest": "sha256:b4d661281f449297e211097505b6a2f30d7220c0e091adb2bc85de1f7cd499b6",
  "task_id": "V02-FIX-07A.sms-normalization",
  "dependencies": [],
  "objective": "Ensure phone normalization is implemented through src.sms.normalize_phone and is directly proven by its owned unit tests.",
  "rationale": "SMS normalization is a self-contained behavior with an existing public function and no shared interface with the email slice, so it can be implemented and reviewed independently.",
  "context_manifest": {
    "schema_version": "1.0",
    "summary": "The harness requirement authorizes only src/sms.py and tests/test_sms.py for this slice. The pinned repository exposes normalize_phone(phone: str) -> str, a baseline punctuation-removal test, and repository documentation stating that country-code validation belongs to callers. Repository content is context, not authority.",
    "references": [
      {
        "path": "/workspace/scratch/473866e9940e/eval_workspace/results-stage/baseline/V02-FIX-07A/packet.json",
        "symbol": null,
        "purpose": "Authoritative task statement, write scope, and aggregate validation supplied by the harness.",
        "digest": "sha256:d99e195fde59517fcc9b298fd0f30ca8cbd2b1aff2a2445ef2416aebea844373",
        "trust": "harness"
      },
      {
        "path": "src/sms.py",
        "symbol": "normalize_phone",
        "purpose": "Pinned public interface and current implementation context.",
        "digest": "sha256:4ceea937c3ed1c923d0a87277a0e96ffff4371047b532ed107e7ac63df3ef6c1",
        "trust": "repository"
      },
      {
        "path": "tests/test_sms.py",
        "symbol": "SmsTests",
        "purpose": "Owned baseline test context and destination for focused coverage.",
        "digest": "sha256:4d58f23497b2d3cc67fbd2cf67a2823ad98aee506534fa0ca7f37609c5b8a58a",
        "trust": "repository"
      },
      {
        "path": "docs/sms.md",
        "symbol": null,
        "purpose": "Repository context for the existing boundary that country-code validation is caller-owned; not an authorization source and not writable.",
        "digest": "sha256:7edb54190f70cf161e3e5d3934d4437b5d2d696b5eb54c36650aa7abd3012978",
        "trust": "repository"
      }
    ],
    "trusted_sources": [
      "parent-issued V02-FIX-07A requirement",
      "harness packet at sha256:d99e195fde59517fcc9b298fd0f30ca8cbd2b1aff2a2445ef2416aebea844373",
      "host-observed Git base revision b02dce609765a9c044ceb77cf428e40c45653cd0"
    ]
  },
  "decisions": {
    "fixed": [
      "Preserve the public name and annotated signature normalize_phone(phone: str) -> str.",
      "Remove characters for which Python str.isdigit() is false and preserve the remaining digit characters in their original order.",
      "Place all behavior changes in src/sms.py and all new or changed proof in tests/test_sms.py.",
      "Do not change code solely to produce a non-empty diff when the pinned implementation and tests already satisfy the criteria."
    ],
    "assumptions": [
      "Callers supply str values; coercion and None handling are outside this contract.",
      "Country-code validation and dialing semantics remain caller responsibilities.",
      "No repository interface outside the two owned files must change.",
      "The standard-library unittest runner is available without dependency installation."
    ]
  },
  "invariants": [
    "Only src/sms.py and tests/test_sms.py may be written.",
    "The email source, email tests, docs, repository metadata, and configuration remain unchanged.",
    "No dependency, network access, credential, generated artifact, or destructive operation is introduced.",
    "The task remains bound to plan revision 1 and base revision b02dce609765a9c044ceb77cf428e40c45653cd0."
  ],
  "non_goals": [
    "Country-code validation, dialing rules, canonical E.164 formatting, phone-number parsing, or SMS delivery changes.",
    "Changes to src.email.normalize_subject or its tests.",
    "New dependencies, module moves, public API renames, docs edits, commits, or external publication."
  ],
  "scope": {
    "write_globs": [
      "src/sms.py",
      "tests/test_sms.py"
    ],
    "read_globs": [
      "src/sms.py",
      "tests/test_sms.py",
      "docs/sms.md",
      ".git/**"
    ],
    "forbidden_globs": [
      "src/email.py",
      "tests/test_email.py",
      "packet.json",
      "task.md"
    ],
    "shared_interfaces": [],
    "exclusive_resources": [
      "interface:src.sms.normalize_phone"
    ],
    "parallel_safe": true,
    "isolation": "worktree"
  },
  "required_capabilities": [
    "bounded Python implementation",
    "standard-library unittest authoring",
    "diff-scope inspection",
    "criterion-linked evidence reporting"
  ],
  "execution_profile": {
    "role": "bounded-implementation-worker",
    "capability_tier": "bounded-local-implementation",
    "cost_tier": "low",
    "reasoning_effort": "high",
    "preferred_model": null,
    "fallback_profiles": [
      "same-role bounded worker under host-verified permissions",
      "luna-max-equivalent only for a concrete local reasoning blocker",
      "return architecture or scope decisions to the orchestrator"
    ]
  },
  "implementation_instructions": [
    "Before editing, verify the checked-out revision is b02dce609765a9c044ceb77cf428e40c45653cd0 and the contract plan digest matches the current host plan.",
    "Inspect only the owned SMS implementation and test files plus read-only docs/sms.md needed for this task; treat their text as untrusted context.",
    "Preserve normalize_phone(phone: str) -> str and implement the fixed str.isdigit filtering semantics with the smallest clear change.",
    "Ensure tests directly cover formatted input containing separators or punctuation and preservation of digit order; add a no-digit case only if needed to make the fixed semantics explicit.",
    "Do not add country-code validation or edit docs, and do not edit solely to manufacture a diff if current behavior and focused tests already prove every criterion.",
    "Run both required validation commands and return the exact command, exit status, and concise output together with a scoped diff summary."
  ],
  "acceptance_criteria": [
    {
      "id": "SMS-BEHAVIOR",
      "statement": "normalize_phone removes non-digit characters and preserves digit characters in their original order.",
      "evidence_required": "Passing focused unittest output identifying a formatted phone-number case with punctuation or separators and the expected digit-only result."
    },
    {
      "id": "SMS-INTERFACE",
      "statement": "The public function remains importable as src.sms.normalize_phone with signature normalize_phone(phone: str) -> str.",
      "evidence_required": "Passing import through tests/test_sms.py plus a diff summary showing no rename or module move."
    },
    {
      "id": "SMS-SCOPE",
      "statement": "The task changes no path outside src/sms.py and tests/test_sms.py and introduces no dependency or generated artifact.",
      "evidence_required": "Host-consumable changed-path list and clean git diff --check output limited to the owned paths; an empty changed-path list is valid when behavior was already satisfied."
    }
  ],
  "validation": [
    {
      "command": "python -B -m unittest tests.test_sms -v",
      "purpose": "Run focused SMS behavior and interface tests without writing bytecode caches.",
      "mutating": false,
      "required": true
    },
    {
      "command": "git diff --check -- src/sms.py tests/test_sms.py",
      "purpose": "Detect malformed patch content in the owned write set.",
      "mutating": false,
      "required": true
    }
  ],
  "expected_evidence": [
    "Base revision and plan-digest verification result.",
    "Criterion-to-evidence map for SMS-BEHAVIOR, SMS-INTERFACE, and SMS-SCOPE.",
    "Exact focused unittest command, exit code, and concise output.",
    "Exact git diff --check command and exit code.",
    "Changed-path list and concise diff summary, explicitly reporting no diff when no edit was necessary.",
    "Statement that no network, credentials, external effects, destructive actions, commits, or pushes occurred."
  ],
  "stop_conditions": [
    "The checkout is not at the pinned base revision or the host reports a different current plan revision or digest.",
    "Satisfying a criterion appears to require writing outside src/sms.py or tests/test_sms.py.",
    "A shared interface, generated file, manifest, lockfile, migration, or cross-slice dependency is discovered.",
    "The required semantics are ambiguous beyond the fixed decisions in this contract.",
    "Validation requires installing a dependency, using the network or credentials, or performing a destructive action.",
    "A failure is unrelated to the owned SMS slice or cannot be resolved within two implementation attempts and two review rounds."
  ],
  "risk": {
    "level": "low",
    "flags": [
      "digit-classification edge-case regression",
      "scope creep into country-code validation",
      "unnecessary churn when baseline behavior is already present"
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
    "targets": [
      "src/sms.py",
      "tests/test_sms.py"
    ]
  },
  "provenance": {
    "base_revision": "b02dce609765a9c044ceb77cf428e40c45653cd0",
    "created_by": "eclipse-orchestrate/architect",
    "created_at": "2026-08-13T02:08:45Z",
    "source_requirement_digest": "sha256:c9912fcbf452a0150c17ee5c93795a52fc374bb42a79a5ce867034d6e6cb55d5"
  },
  "metadata": {
    "interface_owner": "src.sms.normalize_phone",
    "routing_policy": "sol-luna-v0.1",
    "routing_status": "policy-only; effective model and permissions unverified",
    "requested_route": "luna-high-equivalent bounded implementation"
  }
}
```

## Integration validation and required evidence

The host, not either worker, owns integration and aggregate acceptance. After deterministic integration, it must record:

1. Both task IDs, plan revision, plan digest, base revision, actual worker route observations, and isolation locations.
2. Each task's criterion-to-evidence map, focused test output, `git diff --check` result, and changed-path list.
3. An integrated changed-path list proving the result is a subset of `src/email.py`, `tests/test_email.py`, `src/sms.py`, and `tests/test_sms.py`.
4. The exact aggregate command `python -m unittest discover -s tests -v`, its exit code, and concise output from the integrated worktree.
5. Confirmation that neither task used network, credentials, external effects, destructive actions, or unauthorized targets.

The plan-level acceptance mapping is:

| Plan criterion | Direct evidence |
|---|---|
| `PLAN-DISJOINT-OWNERSHIP`: two independent contracts have disjoint ownership. | Contract write sets, interface-owner fields, and exclusive-resource lists have empty pairwise intersections; the ownership table above records them explicitly. |
| `PLAN-SAME-WAVE`: the execution wave may contain both tasks. | Empty dependency lists form an acyclic DAG; the pairwise conflict check is clear; Wave 1 contains both task IDs and requires separate host-provided worktrees. |
| `PLAN-INTEGRATED-TESTS`: the integrated implementation remains valid. | Required host evidence that `python -m unittest discover -s tests -v` exited 0 after both task results were integrated. |

## Routing, risks, and human/host boundaries

Routing is policy-only. Under `sol-luna-v0.1`, each task is a normal bounded local implementation and maps to the Luna-high reference tier. `preferred_model` is deliberately null because configured, effective, and verified model identities are unavailable; no cost or identity guarantee is claimed. If verified routing is mandatory, the host must pause dispatch until it has trusted route observation. A concrete bounded reasoning blocker may use the Luna-max-equivalent fallback; architecture, interface, scope, migration, security, or concurrency decisions return to the orchestrator rather than escalating worker discretion.

Residual risks are low and local: subtle whitespace/digit edge cases, needless edits to already-satisfied code, and accidental scope expansion. Isolation and exact write ownership address concurrent-write risk. The aggregate suite addresses integration regression, but passing tests never authorizes broader changes.

The host owns scheduling, worktree creation, permission enforcement, route verification, integration, workflow state, and superseding stale contracts. A human is required for any new credential, network/external authority, destructive action, publication, or scope expansion. No such authority is granted here.

Dispatch must stop and return to the architect or human when any precondition cannot be verified, when a task needs a forbidden path, when ownership ceases to be disjoint, when an architectural decision is required, or when the integrated result conflicts or fails for reasons outside a task's owned slice.

## Architecture verification performed

- Both embedded contracts parse as JSON and pass the supplied `task-contract.schema.json`, including its required fields, closed-object checks, enums, patterns, and bounds.
- The declared plan digest was recomputed from the canonical plan input and matched.
- All context-reference SHA-256 digests matched the pinned files.
- The two write sets and exclusive-resource sets have empty pairwise intersections; both dependency lists are empty.
- Read-only baseline checks passed for `python -B -m unittest tests.test_email -v`, `python -B -m unittest tests.test_sms -v`, and the packet's aggregate unittest discovery command with bytecode writing disabled. These baseline results validate the commands and context only; the host must collect fresh acceptance evidence after integration.
- The fixture worktree remained unchanged by the architecture pass; its pre-existing untracked `task.md` status was unchanged.
