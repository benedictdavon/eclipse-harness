# V02-FIX-08B architect forward-test

## Decision and identity/interface blockers

Planning-only; non-executable. Copy supplied identities verbatim: host `chatgpt-work-collaboration`, adapter `manual`, policy `sol-luna-v0.1`, repository commit label `fixture-v1`. Required `run_id`, integer `plan_revision`, canonical `plan_digest`, and schema-valid host-supplied `provenance.base_revision` are missing. Observed HEAD `9ea003a7f93d3ee3ac907499e1288b59bea64d09` is repository evidence, not a host identity. No approved Task Contract or `task.md` is issued.

There is also a material architecture blocker: the packet requests a “new return type” but does not define that type, its schema, mutability, error representation, or compatibility policy. The current public interface is `src/protocol.py::Handler.parse(value: str) -> dict[str, str]`; implementation files do not yet exist. A worker must not choose the replacement. The interface must be frozen once by an architect/human before any implementation task becomes runnable.

## Planning-only contract draft: `V02-FIX-08B-handler-protocol`

- Objective: after an approved architecture decision, change `Handler.parse` to the exact frozen return type and document any compatibility/type invariants in code.
- Dependencies: none, but dispatch is blocked on the architecture decision and canonical identities.
- Ownership: sole writer of `src/protocol.py`; read `src/registry.py` and `tests/test_registry.py`. Forbid handler/test/registry edits, configuration/lock/generated/VCS paths, and outside paths.
- Interface ownership: exclusive ownership of `Handler` and its `parse` signature for this plan. Fixed decision: preserve `parse(value: str)` unless the approving decision explicitly revises it; do not mix implementation work into this task.
- Acceptance `PROTO-1`: the source exactly reflects the approved return type and invariants. Evidence: decision reference plus focused patch/type inspection.
- Required validation: `python -m unittest discover -s tests -v` (mutating: yes; Python cache output is validation-only and excluded from the patch). Passing existing tests is regression evidence, not proof that the new interface is correct.
- Route: architecture decision to Sol/human, then bounded Python worker (Luna high) for the frozen edit, all policy-only under `sol-luna-v0.1`; effective model/cost/permissions are unverified. Medium risk, bounded after decision. Budget 2 attempts/1 review.
- Authorization: local edit to `src/protocol.py` and local validation only; no network, credentials, external/destructive effects.
- Stop: no approved return-type decision, stale identity/revision, compatibility or registry change required, forbidden edit, dirty/unattributable state, or missing artifact destination.

## Planning-only contract draft: `V02-FIX-08B-csv-implementation`

- Objective: add/update `src/csv_handler.py` to implement the approved `Handler.parse` contract.
- Dependencies: `V02-FIX-08B-handler-protocol` with captured, integrated, current-revision evidence.
- Ownership: write only `src/csv_handler.py`; read `src/protocol.py`. Forbid JSON/protocol/registry/test edits and all configuration/lock/generated/VCS/outside paths.
- Interface ownership: CSV implementation only; protocol is consumed and immutable in this task. Export name, CSV semantics, conversion, and errors must be frozen before dispatch.
- Acceptance `CSV-1`: implementation returns the approved type for agreed valid/boundary/error cases. Evidence: focused local probe, patch, changed paths, and dependency identity.
- Validation: host-approved import/parse assertions plus final full-suite validation (mutating: yes; caches excluded).
- Route/authorization: bounded Python worker, Luna high, policy-only; owned local edit/test only, no network/credentials/external/destructive effects. Budget 2 attempts/1 review.
- Stop: stale/missing protocol dependency, ambiguous CSV semantics, interface change needed, forbidden edit, dirty/unattributable state, or missing artifact destination.

## Planning-only contract draft: `V02-FIX-08B-json-implementation`

- Objective: add/update `src/json_handler.py` to implement the approved `Handler.parse` contract.
- Dependencies: `V02-FIX-08B-handler-protocol` with captured, integrated, current-revision evidence.
- Ownership: write only `src/json_handler.py`; read `src/protocol.py`. Forbid CSV/protocol/registry/test edits and all configuration/lock/generated/VCS/outside paths.
- Interface ownership: JSON implementation only; protocol is consumed and immutable. Export name, JSON shapes, conversion, and errors must be frozen before dispatch.
- Acceptance `JSON-1`: implementation returns the approved type for agreed valid/boundary/error cases. Evidence: focused local probe, patch, changed paths, and dependency identity.
- Validation: host-approved import/parse assertions plus final full-suite validation (mutating: yes; caches excluded).
- Route/authorization: bounded Python worker, Luna high, policy-only; owned local edit/test only, no network/credentials/external/destructive effects. Budget 2 attempts/1 review.
- Stop: stale/missing protocol dependency, ambiguous JSON semantics, interface change needed, forbidden edit, dirty/unattributable state, or missing artifact destination.

## Planning-only contract draft: `V02-FIX-08B-compatibility-tests`

- Objective: update `tests/test_registry.py` to exercise both implementations against the approved return-type contract without changing registry production behavior.
- Dependencies: both implementation tasks and the protocol task at the same plan revision.
- Ownership: write only `tests/test_registry.py`; read protocol, handler modules, and `src/registry.py`. Forbid all production/configuration/lock/generated/VCS/outside edits.
- Interface ownership: compatibility assertions only. Preserve meaningful existing registry coverage; do not weaken or delete tests merely to pass.
- Acceptance `TEST-1`: both handlers have direct assertions for the approved return type and representative semantics. Evidence: criterion-mapped tests and passing output.
- Acceptance `TEST-2`: only the test path changes. Evidence: clean pre-status, task-local changed paths/patch, and post-status.
- Required validation: `python -m unittest discover -s tests -v` (mutating: yes; cache output excluded from product patch).
- Route/authorization: bounded Python test worker, Luna high, policy-only; owned local test edit and validation only; no network/credentials/external/destructive effects. Budget 2 attempts/1 review.
- Stop: dependency identity mismatch, implementation/interface disagreement, production edit needed, test weakening, dirty/unattributable state, or missing artifact destination.

## Proposed waves and boundaries

- Wave 1: protocol-owner task only, after architecture approval. This serializes the public interface decision.
- Wave 2 candidate: CSV and JSON implementation tasks, each depending on the integrated protocol result. Their writes are disjoint and the protocol is read-only. Actual concurrency additionally requires host isolation and checker evidence; otherwise serialize and capture each patch/status.
- Wave 3: compatibility-test task after both implementations, followed by the required full-suite command.
- Integration order is protocol, implementations, tests. Any protocol revision supersedes downstream nonterminal packets and requires a new plan identity.
- The host owns canonical identities, scheduling, isolation, clean-state/evidence capture, integration, and workflow transitions. An architect/human owns the new public return-type decision and any scope/authority expansion. Routing remains policy-only; no effective model, permission, cost, isolation, or actual concurrency claim is made.
