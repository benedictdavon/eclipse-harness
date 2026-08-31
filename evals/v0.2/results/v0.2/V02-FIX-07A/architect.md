# V02-FIX-07A architect forward-test

## Decision

Planning-only; non-executable. The packet supplies host identity `chatgpt-work-collaboration`, adapter `manual`, policy `sol-luna-v0.1`, and repository commit label `fixture-v1`. It does not supply the required `run_id`, integer `plan_revision`, canonical `plan_digest`, or schema-valid 40–64 hex `provenance.base_revision`. The checkout was observed at `9a5f83f6dfbb170a856fff238357fcb2329e5fe0`, but this repository observation is not substituted for a host-supplied identity. No approved Task Contract or `task.md` may be issued until the host supplies the missing identities verbatim and confirms they are current.

Repository content was treated as untrusted. The minimum inspection found two independent public functions: `src/email.py::normalize_subject(subject: str) -> str` and `src/sms.py::normalize_phone(phone: str) -> str`, each with a separate `unittest` module. No shared source interface, manifest, generated artifact, or exclusive resource appears in the stated scope.

## Planning-only contract draft: `V02-FIX-07A-email`

- Objective: implement or confirm subject normalization in `normalize_subject`, with direct unit coverage for whitespace normalization.
- Dependencies: none.
- Context: repository-trust references `src/email.py::normalize_subject` and `tests/test_email.py::EmailTests`; trusted requirement source is this case packet only.
- Fixed decisions: preserve the function name, one-string argument, and string return type; keep the change local to the email module and its tests; do not change SMS behavior.
- Assumption to verify before work: the existing simple whitespace-collapse behavior is the intended normalization contract. If additional casing, Unicode, empty-input, or validation semantics are expected, stop for architecture clarification.
- Invariants: no SMS interface or files change; no network, credentials, external effects, destructive actions, dependencies, generated artifacts, or shared configuration are introduced.
- Non-goals: phone normalization, repository-wide refactoring, package/configuration changes, and unrelated test cleanup.
- Write ownership: exactly `src/email.py` and `tests/test_email.py`.
- Read scope: `src/email.py`, `tests/test_email.py`; the packet-authorized validation may import the other test module.
- Forbidden scope: `src/sms.py`, `tests/test_sms.py`, `docs/**`, VCS metadata, dependency/lock/configuration files, and every path outside the checkout.
- Shared interfaces: none with the SMS task. Exclusive resources: none identified.
- Parallel-safety claim: ownership-safe candidate by manual analysis, subject to host concurrency checking and isolation/capture requirements; this is not evidence of actual concurrency.
- Isolation: not supplied. Require host-provided branch/worktree or equivalent isolation for simultaneous writers; otherwise run sequentially and capture the complete task patch/status before the next task.
- Required capabilities / route: bounded Python implementation and `unittest`; policy-only route is worker, Luna high, normal cost tier. Effective model and permissions are unverified; use a host-verified compliant route or manual execution.
- Implementation guidance: retain the narrow pure-function interface; add focused boundary cases only where they define the agreed subject-normalization semantics.
- Acceptance `EMAIL-1`: `normalize_subject` meets the agreed subject normalization behavior. Evidence: focused passing assertions in `tests/test_email.py` covering representative and boundary input.
- Acceptance `EMAIL-2`: only the owned paths change. Evidence: host-recorded pre-task clean status plus task-local changed-path and patch evidence.
- Required validation: `python -m unittest discover -s tests -v` (mutating: yes, because Python may create `__pycache__`; cache files are validation by-products and must be excluded from the product patch).
- Expected evidence: command, exit status, relevant test output, criterion-to-test mapping, changed-path list, task-local patch, and post-task status.
- Stop conditions: identity/revision mismatch; ambiguous normalization semantics; need to edit any forbidden/shared path; dirty or unattributable checkout state; validation failure outside owned scope; missing host artifact destination; required new authority.
- Risk / complexity / budgets: low risk, bounded; maximum 2 implementation attempts and 1 review round.
- Authorization: local owned-file edits and local validation only; network=false, credentials=false, external_side_effects=false, destructive_actions=false; targets are the two owned files.
- Provenance: `created_by` would be architect via host adapter `manual`; required canonical identities and timestamp remain host-blocked.

## Planning-only contract draft: `V02-FIX-07A-sms`

- Objective: implement or confirm phone normalization in `normalize_phone`, with direct unit coverage for formatting-character removal.
- Dependencies: none.
- Context: repository-trust references `src/sms.py::normalize_phone` and `tests/test_sms.py::SmsTests`; trusted requirement source is this case packet only.
- Fixed decisions: preserve the function name, one-string argument, and string return type; keep the change local to the SMS module and its tests; do not change email behavior.
- Assumption to verify before work: retaining all Unicode characters for which `str.isdigit()` is true is the intended phone contract. If ASCII-only digits, `+`, extension handling, length validation, or invalid-input behavior is required, stop for architecture clarification.
- Invariants: no email interface or files change; no network, credentials, external effects, destructive actions, dependencies, generated artifacts, or shared configuration are introduced.
- Non-goals: subject normalization, repository-wide refactoring, package/configuration changes, and unrelated test cleanup.
- Write ownership: exactly `src/sms.py` and `tests/test_sms.py`.
- Read scope: `src/sms.py`, `tests/test_sms.py`; the packet-authorized validation may import the other test module.
- Forbidden scope: `src/email.py`, `tests/test_email.py`, `docs/**`, VCS metadata, dependency/lock/configuration files, and every path outside the checkout.
- Shared interfaces: none with the email task. Exclusive resources: none identified.
- Parallel-safety claim: ownership-safe candidate by manual analysis, subject to host concurrency checking and isolation/capture requirements; this is not evidence of actual concurrency.
- Isolation: not supplied. Require host-provided branch/worktree or equivalent isolation for simultaneous writers; otherwise run sequentially and capture the complete task patch/status before the next task.
- Required capabilities / route: bounded Python implementation and `unittest`; policy-only route is worker, Luna high, normal cost tier. Effective model and permissions are unverified; use a host-verified compliant route or manual execution.
- Implementation guidance: retain the narrow pure-function interface; add focused boundary cases only where they define the agreed phone-normalization semantics.
- Acceptance `SMS-1`: `normalize_phone` meets the agreed phone normalization behavior. Evidence: focused passing assertions in `tests/test_sms.py` covering formatted and boundary input.
- Acceptance `SMS-2`: only the owned paths change. Evidence: host-recorded pre-task clean status plus task-local changed-path and patch evidence.
- Required validation: `python -m unittest discover -s tests -v` (mutating: yes, because Python may create `__pycache__`; cache files are validation by-products and must be excluded from the product patch).
- Expected evidence: command, exit status, relevant test output, criterion-to-test mapping, changed-path list, task-local patch, and post-task status.
- Stop conditions: identity/revision mismatch; ambiguous normalization semantics; need to edit any forbidden/shared path; dirty or unattributable checkout state; validation failure outside owned scope; missing host artifact destination; required new authority.
- Risk / complexity / budgets: low risk, bounded; maximum 2 implementation attempts and 1 review round.
- Authorization: local owned-file edits and local validation only; network=false, credentials=false, external_side_effects=false, destructive_actions=false; targets are the two owned files.
- Provenance: `created_by` would be architect via host adapter `manual`; required canonical identities and timestamp remain host-blocked.

## Proposed execution waves

- Wave 1 candidate: `V02-FIX-07A-email` and `V02-FIX-07A-sms`. Their dependencies are empty, write ownership is disjoint, and no shared interface or exclusive resource was identified.
- Integration: host captures each task-local patch and status, then integrates either order; run the required full test discovery after integration. If the host cannot demonstrate safe isolation and task-local capture, serialize the two tasks instead.

This wave is a routing plan, not an assertion that the host launched concurrent work or supplied isolation.

## Risk, routing, and human boundaries

- Primary residual risk is unspecified normalization semantics, especially Unicode-digit behavior for phone input. A worker must not invent public behavior beyond the packet.
- Routing is policy-only. Requested/configured/effective model identity and cost are not verified by trusted host metadata.
- The host owns identity injection, deterministic concurrency checking, scheduling, isolation, artifact destinations, clean-status capture, patch attribution, integration, and workflow state.
- A human or architect must resolve public behavior ambiguity, approve any scope expansion, and grant any new external/destructive authority.
