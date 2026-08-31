# Evidence and escalation

A complete result must contain satisfied evidence for every acceptance criterion and passing evidence for every required validation command. “Done” and “tests pass” are claims, not evidence.

In the Result Contract, set `worker_identity.role` to `executor`. “Worker” names
the behavioral role in prose; it is not an accepted wire value.

Use `complete` only for that state. Use `blocked` when environment, context, or
authority prevents completion; `failed` when authorized bounded work exhausted
its attempts without satisfying the contract; and `escalated` when an architect
or human decision is required. Do not wrap an invalid or partial contract in
success prose.

Use these blocker classes:

- `CTX_MISSING` — request bounded context.
- `SPEC_AMBIGUOUS` — return to architect/user.
- `ENV_FAILURE` — repair environment.
- `AUTH_REQUIRED` — request human authority.
- `SCOPE_EXPANSION` — return to architect.
- `LOCAL_REASONING` — increase worker reasoning within policy.
- `ARCH_DECISION` — return to architect.
- `SECURITY_DECISION` — return to architect/human.
- `DESTRUCTIVE_ACTION` — require human approval.
- `VALIDATION_FAILURE` — retry within budget.
- `BUDGET_EXHAUSTED` — return to architect.

Do not classify context, environment, permission, or credential failures as local reasoning limitations.

Report measured usage only from host data. Mark inferred values estimated and absent values unavailable.

`files_changed` is the intended product change set, sorted before its canonical
digest is calculated. The host separately supplies the actual patch and full
status, including untracked/generated artifacts. A worker claim does not replace
that observation.
