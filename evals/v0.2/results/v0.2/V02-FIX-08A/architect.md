# V02-FIX-08A architect forward-test

## Decision and identity blocker

Planning-only; non-executable. Supplied identities are host `chatgpt-work-collaboration`, adapter `manual`, policy `sol-luna-v0.1`, and repository commit label `fixture-v1`. The packet omits required `run_id`, integer `plan_revision`, canonical `plan_digest`, and schema-valid host-supplied `provenance.base_revision`. Observed HEAD `9ea003a7f93d3ee3ac907499e1288b59bea64d09` is untrusted repository evidence, not a replacement identity. Therefore no approved Task Contract or `task.md` is issued.

The shared resource is real: `src/registry.py::HANDLERS/register` owns registration, and `tests/test_registry.py::RegistryTests` is the single registry test surface. Giving separate CSV and JSON tasks those paths would create overlapping writers. `src/protocol.py::Handler.parse(value: str) -> dict[str, str]` is a consumed shared interface and must remain unchanged.

## Planning-only contract draft: `V02-FIX-08A-csv-handler`

- Objective: add `src/csv_handler.py` implementing the frozen `Handler.parse` protocol for the agreed CSV shape.
- Dependencies: none. Write only `src/csv_handler.py`; read only `src/protocol.py`. Forbid registry/test edits, `src/json_handler.py`, protocol edits, configuration/lock/generated/VCS paths, and outside paths.
- Interface ownership: CSV implementation only; it consumes but does not own `Handler`. Freeze the exported class/factory name before dispatch so the registry owner need not revise it.
- Acceptance `CSV-1`: the implementation conforms to `parse(str) -> dict[str, str]` for architect-approved valid and invalid CSV behavior. Evidence: focused host probe/output plus task-local patch and changed paths.
- Validation probe: a host-approved local `python -c` import/parse assertion after semantics are frozen (mutating: yes; Python may create cache files, which are excluded from the product patch).
- Route/authorization: bounded Python worker, Luna high under `sol-luna-v0.1`, policy-only; local owned-file edit/test only; no network, credentials, external/destructive effects. Budget 2 attempts/1 review.
- Stop: unresolved CSV record/header/error semantics, shared-interface change, forbidden edit, stale identity, dirty/unattributable state, or missing artifact destination.

## Planning-only contract draft: `V02-FIX-08A-json-handler`

- Objective: add `src/json_handler.py` implementing the frozen `Handler.parse` protocol for the agreed JSON object shape.
- Dependencies: none. Write only `src/json_handler.py`; read only `src/protocol.py`. Forbid registry/test edits, `src/csv_handler.py`, protocol edits, configuration/lock/generated/VCS paths, and outside paths.
- Interface ownership: JSON implementation only; it consumes but does not own `Handler`. Freeze the exported class/factory name before dispatch.
- Acceptance `JSON-1`: the implementation conforms to `parse(str) -> dict[str, str]` for architect-approved object/value/error behavior. Evidence: focused host probe/output plus task-local patch and changed paths.
- Validation probe: a host-approved local `python -c` import/parse assertion after semantics are frozen (mutating: yes; cache files are excluded from the product patch).
- Route/authorization: bounded Python worker, Luna high under `sol-luna-v0.1`, policy-only; local owned-file edit/test only; no network, credentials, external/destructive effects. Budget 2 attempts/1 review.
- Stop: unresolved non-object/non-string-value/error semantics, shared-interface change, forbidden edit, stale identity, dirty/unattributable state, or missing artifact destination.

## Planning-only contract draft: `V02-FIX-08A-registry-integration`

- Objective: register both frozen handler exports in `src/registry.py` and update the one registry test surface to verify both registrations without weakening existing guarantees.
- Dependencies: `V02-FIX-08A-csv-handler`, `V02-FIX-08A-json-handler`.
- Ownership: sole writer of `src/registry.py` and `tests/test_registry.py`; may read both handler modules and `src/protocol.py`. Forbid edits to handler/protocol modules, configuration/lock/generated/VCS paths, and outside paths.
- Interface/resource ownership: exclusive owner of `HANDLERS`, `register`, registry import/initialization behavior, and `RegistryTests` during this plan. No other task may write these paths.
- Fixed decisions: preserve `Handler`; use distinct architect-approved registry keys; make registration initialization deterministic and ensure tests do not leak mutable global registry state across cases.
- Acceptance `REG-1`: both handlers are registered under the frozen keys and conform to `Handler`. Evidence: direct registry assertions.
- Acceptance `REG-2`: existing registry behavior is deliberately updated rather than silently weakened. Evidence: focused diff and complete passing discovery.
- Required validation: `python -m unittest discover -s tests -v` (mutating: yes; cache output is validation-only and excluded from the patch).
- Route/authorization: bounded Python integration worker, Luna high under `sol-luna-v0.1`, policy-only; edits limited to its two owned paths and local tests; no network, credentials, external/destructive effects. Budget 2 attempts/1 review.
- Stop: dependency evidence absent/stale, handler export mismatch, need to edit handler/protocol files, ambiguous registry keys/lifecycle, dirty/unattributable state, or missing artifact destination.

## Proposed waves and boundaries

- Wave 1 candidate: CSV and JSON handler tasks. Their write ownership is disjoint; they only read the frozen protocol. This does not prove host isolation or actual concurrent execution.
- Wave 2: registry integration task after both Wave 1 results are captured and integrated. It is the only registry/test writer.
- Integration order is both handler patches, then the registry/test patch, then full discovery. If the host cannot demonstrate branch/worktree or equivalent isolation and task-local capture, serialize Wave 1 as well.
- Before executable approval, an architect/human must freeze CSV/JSON input, conversion/error semantics, export names, and registry keys. The host owns canonical identities, concurrency checking, scheduling, isolation, artifacts, clean-state capture, patch attribution, integration, and state transitions. Effective route/cost/permissions remain unverified.
