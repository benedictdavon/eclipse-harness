# Review Contract

A Review Contract records independent verification of one exact Task and Result Contract. `schemas/review-contract.schema.json` is the wire format.

The host supplies the reviewer with the original requirement, current plan, task, result, actual diff, relevant callers/interfaces, and host-observed validation. The review binds to the task and result digests.

The reviewer records desired/effective permission status, criterion verdicts, validation analysis, structured findings, outcome, and residual risk. Configuration or self-report cannot prove effective read-only enforcement.

An `accepted` outcome requires:

- no material findings;
- a satisfied verdict for every criterion;
- scope-compliant changed files;
- adequate direct validation evidence;
- preserved decisions and invariants.

Finding dispositions are `worker`, `architect`, or `human`. Bounded corrections return to a worker. Architecture, interface, or scope conflicts return to the architect. Credentials, destructive actions, and new external authority return to a human.
