# V02-FIX-07B architect forward-test

## Decision and identity blocker

Planning-only; non-executable. Copy supplied identities verbatim: host `chatgpt-work-collaboration`, adapter `manual`, policy `sol-luna-v0.1`, repository commit label `fixture-v1`. Required `run_id`, integer `plan_revision`, canonical `plan_digest`, and schema-valid host-supplied `provenance.base_revision` are absent. The observed checkout HEAD, `9a5f83f6dfbb170a856fff238357fcb2329e5fe0`, is repository evidence and is not substituted for a host identity. Do not create `task.md` until the host supplies current canonical identities and a destination outside the product checkout for evidence.

Minimum untrusted-repository inspection found `src/email.py::normalize_subject`, its isolated `tests/test_email.py`, and `docs/sms.md`, which states that numbers are normalized to digits and country-code validation belongs to callers. The requested source/test paths and documentation path do not share an interface or generated resource.

## Planning-only contract draft: `V02-FIX-07B-email-domain`

- Objective: add a small email-domain helper and focused unit tests without changing subject normalization.
- Dependencies: none.
- Ownership: write only `src/email.py` and `tests/test_email.py`; read those files only. Forbid `docs/**`, SMS source/tests, configuration/lock/generated/VCS paths, and all paths outside the checkout.
- Interface ownership: the new helper and its email-only tests. Shared interfaces and exclusive resources: none with the documentation task.
- Fixed decisions: keep a pure `str -> str` helper local to `src.email`; preserve `normalize_subject`; introduce no dependency or repository-wide refactor.
- Architecture clarification required before executable approval: freeze the helper name and behavior for missing/multiple `@`, case, whitespace, internationalized domains, and invalid input. A worker must not invent this public contract.
- Acceptance `EMAIL-DOMAIN-1`: the architect-approved helper behavior has direct positive and boundary tests. Evidence: focused test assertions and passing output.
- Acceptance `EMAIL-DOMAIN-2`: only owned paths change and existing subject behavior remains passing. Evidence: task-local patch/changed paths and test output.
- Required validation: `python -m unittest tests.test_email -v` (mutating: yes; it may create `__pycache__`, which must remain outside the product patch).
- Route: bounded Python worker, Luna high under `sol-luna-v0.1`, policy-only; effective model, cost, and permissions are unverified. Risk is medium until the public behavior is frozen, then low/bounded. Budget: 2 attempts, 1 review round.
- Authorization: local owned-file edits and local tests only; no network, credentials, external effects, destructive actions, or other targets.
- Stop: missing/stale identities, unresolved helper semantics, need for any forbidden/shared edit, dirty/unattributable state, missing artifact destination, or validation failure requiring scope expansion.

## Planning-only contract draft: `V02-FIX-07B-sms-doc`

- Objective: document SMS country-code behavior consistently with the current digits-only normalization and caller-owned validation boundary.
- Dependencies: none; the document describes the existing SMS contract and does not consume the new email helper.
- Ownership: write only `docs/sms.md`; read `docs/sms.md` and `src/sms.py` for behavior confirmation. Forbid all source/test edits, configuration/lock/generated/VCS paths, and paths outside the checkout.
- Interface ownership: prose describing country-code responsibility. Shared interfaces and exclusive resources: none with the email task.
- Fixed decisions: do not change runtime behavior; state that formatting is reduced to digits and validation/interpretation of country codes remains a caller responsibility; avoid guarantees not present in `normalize_phone`.
- Acceptance `SMS-DOC-1`: the document clearly identifies normalization behavior and country-code responsibility. Evidence: task-local documentation diff mapped to the current `normalize_phone` implementation.
- Acceptance `SMS-DOC-2`: only `docs/sms.md` changes. Evidence: host-recorded clean pre-status, changed-path list, patch, and post-status.
- Required integration smoke validation: `python -m unittest tests.test_email -v` (mutating: yes; cache output is excluded from the product patch). Documentation correctness additionally requires direct diff inspection because this command does not validate prose.
- Route: tiny deterministic documentation worker, Luna medium under `sol-luna-v0.1`, policy-only; effective model, cost, and permissions are unverified. Low risk/trivial. Budget: 1 attempt, 1 review round.
- Authorization: local edit to `docs/sms.md` and local validation only; no network, credentials, external effects, destructive actions, or other targets.
- Stop: identity mismatch, requested runtime/API change, need for any forbidden edit, dirty/unattributable state, missing artifact destination, or prose that cannot be supported by current source.

## Proposed waves and boundaries

- Wave 1 candidate: `V02-FIX-07B-email-domain` and `V02-FIX-07B-sms-doc`, with no dependency edge. Ownership is disjoint and neither task consumes the other's output. This is manual planning analysis, not proof of actual concurrency.
- Host integration: capture each task-local patch/status, integrate in either order, then run the required email test command. Concurrent launch requires host-provided branch/worktree or equivalent isolation and a concurrency check; otherwise serialize while preserving task-local evidence.
- The host owns identities, scheduling, isolation, clean-state capture, evidence storage, patch attribution, integration, and workflow state. An architect/human must resolve the email helper's public semantics and approve any scope or authority expansion.
