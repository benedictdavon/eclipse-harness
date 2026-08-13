# Result Contract

A Result Contract is a worker's structured claim and evidence for one exact Task Contract. `schemas/result-contract.schema.json` is the wire format.

It binds to the task and plan digests and records status, worker route claims, changed files, implementation summary, local decisions, command evidence, criterion evidence, blockers, deviations, risks, escalation, git base/diff identity, usage quality, and timestamps.

## Command records

Record every acceptance-validation command and any command relevant to mutations, dependencies, network, credentials, destructive actions, or external effects. Ordinary bounded read-only exploration may be summarized; safe undeclared commands may also be recorded.

Outcome and exit code must agree:

- `passed` -> `exit_code` is `0`;
- `failed` -> `exit_code` is a non-zero integer;
- `not-run` -> `exit_code` is `null`.

Every task validation marked `required` must appear and pass for a `complete` result. Recorded commands remain subject to the Task Contract's authorization even when they were not predeclared.

## Completion

A `complete` result needs satisfied evidence for every acceptance criterion and no blockers. The host or reviewer must compare `files_changed` with the actual diff; worker self-report is not sufficient.

Requested and configured model identity are claims. Effective identity remains null unless a separate trusted host observation proves it.
