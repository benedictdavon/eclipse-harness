# Bounded execution

Start only when the host or user presents the task as ready or ready for correction. Confirm that the host-provided working tree is based on `provenance.base_revision`.

Also confirm a clean pre-task status and a host-owned output path outside the
product checkout. Do not write the Result Contract, logs, or reviewer material
into the repository unless the task explicitly authorizes that exact path.

Stay inside the packet. Narrow exploration is permitted only to follow direct dependencies required for the objective. Stop when completion needs material scope expansion or a new decision.

For a correction, address only the structured review findings while preserving the original contract and plan revision. Do not use a review finding as permission for adjacent refactoring.

Task `validation` entries are the commands that support acceptance. Record each required command exactly. Additional bounded exploration/debugging commands may be recorded even when they were not predeclared; they remain subject to task authorization. Always disclose mutating formatters, network/package operations, credentials, destructive actions, and external effects. Do not conceal them inside another command. Summarize long output without changing the exit status or outcome.

Capture both the patch and full status after implementation and after validation.
Ordinary `git diff` omits untracked files; list them and include their content in
the host handoff when they are part of the intended patch. If validation creates
caches, bytecode, coverage output, snapshots, or build files, report them and
their provenance. Do not delete or reset them unless destructive action and the
exact target are authorized. The host owns cleanup and integration.

Required commands gate a `complete` result. Optional probes may find real defects,
but an unavailable optional tool does not change a passing required command into
a failure. If new validation is materially necessary to prove a criterion or
invariant, return a contract/evidence blocker rather than silently expanding the
task.

Use consistent command evidence: `passed` means exit code `0`, `failed` means a non-zero exit code, and `not-run` means a null exit code.

The worker may repair routine implementation and test failures within `max_attempts`. The host or user tracks that budget; Eclipse does not schedule attempts.

For corrections, use the same canonical Task Contract identity and increment the
host-provided attempt. Never digest a Markdown envelope. When the optional CLI is
available, validate the structured Result Contract against the Task Contract
before handoff; the skills remain usable when it is absent.
