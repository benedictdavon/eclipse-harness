# Review Contract

A Review Contract records independent verification of one exact Task and Result Contract. `schemas/review-contract.schema.json` is the wire format.

The host supplies the reviewer with the original requirement, current plan, task, result, clean pre-task status, actual patch and full post-task status including untracked files, relevant callers/interfaces, and host-observed validation. The review binds to canonical task and result digests.

The reviewer records desired/effective permission status, criterion verdicts, validation analysis, structured findings, outcome, and residual risk. Configuration or self-report cannot prove effective read-only enforcement.

An `accepted` outcome requires:

- no material findings;
- a satisfied verdict for every criterion;
- scope-compliant changed files;
- adequate direct validation evidence;
- preserved decisions and invariants.

Required contract validation and direct criterion evidence gate acceptance.
Supplemental checks can support concrete defects; an unavailable undeclared tool
does not by itself fail the task. A missing material evidence requirement is a
contract issue for the architect.

Host-proven result/log files and validation byproducts are distinguished from
the intended product patch. Missing provenance is routed to the host, not used as
permission for destructive worker cleanup. Prompt-injection review relies on
observable diff/command/disclosure evidence and trusted host observations, not
worker claims that a capability was absent.

Finding dispositions are `worker`, `architect`, or `human`. Bounded corrections return to a worker. Architecture, interface, or scope conflicts return to the architect. Credentials, destructive actions, and new external authority return to a human.

Architecture proposals with material public API, schema, security, or invariant
effects receive read-only review before executable worker delegation. Once the
task's review-round budget is exhausted, remaining findings escalate rather than
starting another correction.
