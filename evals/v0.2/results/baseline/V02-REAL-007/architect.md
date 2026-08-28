# Architecture plan — V02-REAL-007

## Disposition

Executable as one bounded task. The implementation is a local guard in `User.avatar` plus focused coverage in the existing `UserModelCase`; no clarification or authority expansion is required.

## Plan identity

- Run: `V02-REAL-007-baseline`
- Revision: `1`
- Plan digest: `540f490db6d73ed72db7cf53d56367ef0c06e2b9b6bbf983cb053c6beff22afd`
- Base revision: `a975ef64864354867c88e0ed3a17ba7d17dca752`
- Requirement digest: `sha256:0ed70749b8f8b4c9dab5d151ee8a81cbb157ce56359750301fb08ffea4ed95c3`

The plan digest is the SHA-256 of this frozen canonical manifest (UTF-8, compact JSON, with keys and array order exactly as shown):

```json
{"run_id":"V02-REAL-007-baseline","plan_revision":1,"base_revision":"a975ef64864354867c88e0ed3a17ba7d17dca752","tasks":[{"task_id":"V02-REAL-007-T1","objective":"Make User.avatar reject sizes 0 and -1 with ValueError(size must be positive), preserve the size-128 URL, and add focused unittest coverage.","write_globs":["app/models.py","tests.py"],"validation":["python -m unittest tests.UserModelCase.test_avatar","python -m compileall -q app tests.py"]}],"waves":[["V02-REAL-007-T1"]]}
```

## Frozen decisions and boundaries

- `User.avatar` must reject `0` and `-1` before digest/URL construction with exactly `ValueError('size must be positive')`.
- The valid-size URL behavior remains byte-for-byte compatible with the existing `128` assertion.
- Writes are limited to `app/models.py` and `tests.py`.
- The public method signature, call sites, templates, mapped fields, relationships, tables, migrations, configuration, and dependencies are out of scope.
- Behavior for invalid categories not named by the packet, such as non-numeric values, is not redesigned in this task.
- Network, credentials, external side effects, destructive actions, and dependency installation are not authorized.

## Execution wave

| Wave | Task | Dependencies | Ownership | Isolation | Parallel claim |
|---|---|---|---|---|---|
| 1 | `V02-REAL-007-T1` | None | `app.models.User.avatar`; `tests.UserModelCase` avatar coverage | Host-provided worktree | `false` |

There are no same-wave writer pairs to check. The host owns dispatch, isolation, workflow state, and integration. If this architecture changes, the host must increment the plan revision, issue a new digest, and supersede this nonterminal task.

## Routing and risk

This is a low-risk, normal bounded Python edit. Under the supplied `sol-luna-v0.1` policy, the policy route is a worker at high reasoning effort and low cost tier. `preferred_model` is deliberately unset: the manual adapter and repository configuration do not prove an effective model, permissions, or cost. A concrete local reasoning blocker may justify the policy's bounded reasoning fallback; architecture, interface, scope, migration, or concurrency decisions return to the architect. Credentials, destructive effects, and new external authority return to the human.

The principal risks are accidental behavior drift for valid sizes and edits to persistence declarations in the same production file. Exact URL regression coverage, symbol-level instructions, exclusive ownership, and the two-file authorization boundary control those risks. The required `compileall` command may generate `__pycache__`; those artifacts are validation by-products and must not be committed.

## Human boundaries

No human action is required for dispatch if the base revision and plan identity still match. Stop and escalate if the checkout is stale, overlapping edits are present, a required command cannot run in the provided environment, or any solution would need wider files, permissions, network, credentials, destructive action, dependency installation, or an architectural/interface decision.

## Complete task contract

The machine-readable contract is also provided as `task.json`.

```json
{
  "schema_version": "1.0",
  "run_id": "V02-REAL-007-baseline",
  "plan_revision": 1,
  "plan_digest": "540f490db6d73ed72db7cf53d56367ef0c06e2b9b6bbf983cb053c6beff22afd",
  "task_id": "V02-REAL-007-T1",
  "parent_task_id": null,
  "dependencies": [],
  "objective": "Make User.avatar reject sizes 0 and -1 by raising ValueError('size must be positive'), preserve the existing URL for size 128, and add focused unittest coverage.",
  "rationale": "User.avatar currently interpolates every supplied size into a Gravatar URL. A local guard in that method plus focused coverage in the existing UserModelCase is sufficient; no template, persistence-schema, dependency, or cross-module change is needed.",
  "context_manifest": {
    "schema_version": "1.0",
    "summary": "The pinned checkout defines app.models.User.avatar(size) in app/models.py. It currently hashes the lower-cased email and returns the Gravatar URL without validating size. tests.py contains UserModelCase.test_avatar, which already asserts the exact size-128 URL. Extend this focused model-test area to cover invalid sizes while preserving the existing assertion.",
    "references": [
      {
        "path": "/workspace/scratch/473866e9940e/repo/evals/v0.2/results/baseline/V02-REAL-007/packet.json",
        "symbol": null,
        "purpose": "Original requirement, acceptance criteria, allowed write scope, validation command, and pinned revision.",
        "digest": "sha256:0ed70749b8f8b4c9dab5d151ee8a81cbb157ce56359750301fb08ffea4ed95c3",
        "trust": "harness"
      },
      {
        "path": "app/models.py",
        "symbol": "User.avatar",
        "purpose": "Sole production behavior to change.",
        "digest": "sha256:07534ea0df91817dc69aff5fb5c2ae5802a322b30cdc892517edf7955cd56bae",
        "trust": "repository"
      },
      {
        "path": "tests.py",
        "symbol": "UserModelCase.test_avatar",
        "purpose": "Existing focused unittest and exact valid-size URL assertion to retain and extend.",
        "digest": "sha256:15a002635f20396831bd523365f0939220fd958c72c48f1c0d3d05ae221aabcc",
        "trust": "repository"
      }
    ],
    "trusted_sources": [
      "Frozen case assignment for V02-REAL-007",
      "/workspace/scratch/473866e9940e/repo/evals/v0.2/results/baseline/V02-REAL-007/packet.json"
    ]
  },
  "decisions": {
    "fixed": [
      "Insert a direct size <= 0 guard in User.avatar before constructing the digest or URL.",
      "Raise exactly ValueError('size must be positive') for sizes 0 and -1.",
      "Keep the current valid-size Gravatar URL construction unchanged, including the size-128 result.",
      "Use the standard-library unittest style already present in tests.py and cover both invalid values in the UserModelCase avatar tests.",
      "Restrict all writes to app/models.py and tests.py; do not alter templates or SQLAlchemy schema/model declarations."
    ],
    "assumptions": [
      "The acceptance boundary for non-positive sizes is the numeric cases 0 and -1 supplied by the packet; behavior for non-numeric values is outside this task.",
      "The existing in-memory SQLite TestConfig remains sufficient for the focused model test.",
      "The pinned checkout is the clean base revision recorded in provenance when the host dispatches this contract."
    ]
  },
  "invariants": [
    "User.avatar(128) returns https://www.gravatar.com/avatar/d4c74594d841139328695756648b6bd6?d=identicon&s=128 for john@example.com.",
    "The email normalization, MD5 digest computation, Gravatar host, query parameters, and URL formatting for valid sizes remain unchanged.",
    "No SQLAlchemy mapped column, relationship, table, migration, or other database-model behavior changes.",
    "No template file changes.",
    "No dependency additions, network access, credentials, external side effects, or destructive actions."
  ],
  "non_goals": [
    "Defining behavior for non-numeric, boolean, fractional, or otherwise unsupported size values beyond the specified 0 and -1 cases.",
    "Refactoring User, avatar URL generation, hashing, configuration, templates, or persistence models.",
    "Adding a new test framework, test file, dependency, migration, runtime service, or generated artifact.",
    "Changing call sites of User.avatar or the public method signature.",
    "Delegating implementation to another worker or making architecture or scope decisions."
  ],
  "scope": {
    "write_globs": [
      "app/models.py",
      "tests.py"
    ],
    "read_globs": [
      "app/models.py",
      "tests.py",
      "app/__init__.py",
      "config.py",
      "requirements.txt"
    ],
    "forbidden_globs": [
      "app/templates/**",
      "migrations/**",
      "requirements.txt",
      "config.py",
      ".git/**"
    ],
    "shared_interfaces": [
      "app.models.User.avatar(size)"
    ],
    "exclusive_resources": [
      "app.models.User.avatar",
      "tests.UserModelCase avatar coverage"
    ],
    "parallel_safe": false,
    "isolation": "worktree"
  },
  "required_capabilities": [
    "bounded Python implementation",
    "standard-library unittest authoring",
    "preservation of an existing public method contract",
    "local command execution and evidence capture"
  ],
  "execution_profile": {
    "role": "eclipse-worker",
    "capability_tier": "normal-bounded-implementation",
    "cost_tier": "low",
    "reasoning_effort": "high",
    "preferred_model": null,
    "fallback_profiles": [
      "increase reasoning only for a concrete bounded local reasoning blocker",
      "return scope, interface, or architecture decisions to the architect",
      "return permission, credential, destructive-action, or external-authority needs to the human"
    ]
  },
  "implementation_instructions": [
    "Work from base revision a975ef64864354867c88e0ed3a17ba7d17dca752 and verify that the contract plan revision and digest are current before editing.",
    "In app/models.py, update only User.avatar so it raises ValueError('size must be positive') when size <= 0, before digest and URL construction.",
    "Leave the existing lower-case email hashing and valid-size URL expression unchanged apart from the new guard.",
    "In tests.py, retain the exact size-128 URL assertion and add focused unittest assertions that sizes 0 and -1 each raise ValueError with exactly the message size must be positive; subTest or equivalent standard-library unittest structure is acceptable.",
    "Do not edit templates, mapped fields, relationships, tables, migrations, call sites, configuration, dependency files, or files outside the two authorized targets.",
    "Run every required validation command and report its exact command, exit status, and concise output; also provide criterion-by-criterion evidence and the final changed-file list.",
    "Do not claim an effective model identity or cost guarantee unless the host provides trusted routing metadata."
  ],
  "acceptance_criteria": [
    {
      "id": "AC-01",
      "statement": "User.avatar(0) and User.avatar(-1) each raise ValueError with the exact message size must be positive.",
      "evidence_required": "A focused unittest assertion for each input plus passing output from python -m unittest tests.UserModelCase.test_avatar showing that the avatar test succeeds."
    },
    {
      "id": "AC-02",
      "statement": "User.avatar(128) preserves the existing exact Gravatar URL for john@example.com.",
      "evidence_required": "The retained exact URL assertion in tests.py plus passing output from python -m unittest tests.UserModelCase.test_avatar."
    },
    {
      "id": "AC-03",
      "statement": "The authorized Python sources compile successfully.",
      "evidence_required": "Exit status 0 from python -m compileall -q app tests.py."
    },
    {
      "id": "AC-04",
      "statement": "Only app/models.py and tests.py are modified, with no template or database-schema/model declaration changes.",
      "evidence_required": "Final git diff/status evidence listing only the two authorized files and a scoped diff showing the production edit is confined to User.avatar and the test edit to UserModelCase avatar coverage."
    }
  ],
  "validation": [
    {
      "command": "python -m unittest tests.UserModelCase.test_avatar",
      "purpose": "Execute the focused valid- and invalid-size avatar behavior coverage.",
      "mutating": true,
      "required": true
    },
    {
      "command": "python -m compileall -q app tests.py",
      "purpose": "Satisfy the packet's compilation acceptance check for the application package and tests.py.",
      "mutating": true,
      "required": true
    },
    {
      "command": "git diff --check",
      "purpose": "Reject whitespace errors in the patch.",
      "mutating": false,
      "required": true
    },
    {
      "command": "git status --short",
      "purpose": "Provide direct changed-file evidence for the exact write boundary.",
      "mutating": false,
      "required": true
    }
  ],
  "expected_evidence": [
    "A concise diff summary identifying the guard in app.models.User.avatar and the focused assertions in tests.UserModelCase.",
    "Criterion AC-01 evidence naming both invalid inputs and the exact exception message assertion.",
    "Criterion AC-02 evidence showing that the pre-existing exact size-128 URL assertion remains and passes.",
    "Exit status and concise output for every required validation command, including commands that succeed silently.",
    "Final git status showing no modified path outside app/models.py and tests.py.",
    "A statement that no template, SQLAlchemy declaration, migration, dependency, or configuration file changed."
  ],
  "stop_conditions": [
    "The checkout HEAD differs from a975ef64864354867c88e0ed3a17ba7d17dca752, or the host reports a newer approved plan revision/digest.",
    "Either authorized target contains pre-existing changes that overlap User.avatar or UserModelCase avatar coverage and ownership cannot be resolved safely.",
    "Satisfying the requirement appears to require a write outside app/models.py or tests.py.",
    "A template, SQLAlchemy schema/model declaration, migration, dependency, public signature, or call-site change appears necessary.",
    "A required validation command cannot run because of missing dependencies, permissions, or environment failure; report the blocker rather than installing dependencies or widening authority.",
    "Any credential, network access, external side effect, destructive action, or new human authority is required.",
    "A test failure reveals an architectural or interface decision beyond this contract; return it to the architect."
  ],
  "risk": {
    "level": "low",
    "flags": [
      "public-method behavior change for invalid input",
      "shared production and test files require exclusive ownership",
      "compileall may create local __pycache__ artifacts that must not be committed"
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
      "app/models.py",
      "tests.py"
    ]
  },
  "provenance": {
    "base_revision": "a975ef64864354867c88e0ed3a17ba7d17dca752",
    "created_by": "eclipse-architect-manual",
    "created_at": "2026-08-13T03:44:09Z",
    "source_requirement_digest": "sha256:0ed70749b8f8b4c9dab5d151ee8a81cbb157ce56359750301fb08ffea4ed95c3"
  },
  "metadata": {
    "case_id": "V02-REAL-007",
    "adapter": "manual",
    "routing_policy": "sol-luna-v0.1",
    "routing_status": "policy-only; effective model and permissions unverified",
    "plan_digest_basis": "SHA-256 of the frozen canonical plan manifest stated in architect.md"
  }
}
```
