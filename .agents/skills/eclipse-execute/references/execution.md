# Bounded execution

Start only when the host or user presents the task as ready or ready for correction. Confirm that the host-provided working tree is based on `provenance.base_revision`.

Stay inside the packet. Narrow exploration is permitted only to follow direct dependencies required for the objective. Stop when completion needs material scope expansion or a new decision.

For a correction, address only the structured review findings while preserving the original contract and plan revision. Do not use a review finding as permission for adjacent refactoring.

Task `validation` entries are the commands that support acceptance. Record each required command exactly. Additional bounded exploration/debugging commands may be recorded even when they were not predeclared; they remain subject to task authorization. Always disclose mutating formatters, network/package operations, credentials, destructive actions, and external effects. Do not conceal them inside another command. Summarize long output without changing the exit status or outcome.

Use consistent command evidence: `passed` means exit code `0`, `failed` means a non-zero exit code, and `not-run` means a null exit code.

The worker may repair routine implementation and test failures within `max_attempts`. The host or user tracks that budget; Eclipse does not schedule attempts.
