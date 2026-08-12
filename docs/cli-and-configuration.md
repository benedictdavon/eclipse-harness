# Optional CLI, policies, and adapters

The CLI supports the skills; it is not an orchestrator.

| Command | Purpose |
|---|---|
| `eclipse init` | Copy packaged skills without overwriting existing directories. |
| `eclipse validate` | Validate context/task/result/review contracts and optional cross-contract semantics. |
| `eclipse inspect` | Report contract kind, version, and digest. |
| `eclipse check-concurrency` | Validate a dependency DAG and produce ownership-safe execution waves. |
| `eclipse doctor` | Report host-specific profiles, permissions, routes, and degradation. |
| `eclipse adapters generate` | Generate idempotent Codex/Copilot wrappers; supports dry-run. |
| `eclipse eval run` | Aggregate deterministic recorded evaluation outcomes. |

Stable exit codes are `0` for success, `2` for invalid input/operation, and `3` when doctor finds an error-level diagnostic. The global `--json` flag precedes the subcommand.

## Deliberately absent commands

v0.1 has no commands for plan persistence, task dispatch, result/review ingestion, status, render/handoff state, recovery, worktrees, or legacy workflow migration. Those responsibilities belong to the host or user.

## Configuration surface

There is no versioned `.eclipse/config.json` in v0.1. The previous broad configuration implied runtime behavior that Eclipse did not own.

The retained inputs each have a direct consumer:

- `policies/sol-luna.json` is consumed by routing and adapter generation;
- `--max-concurrency` controls the generated Codex concurrency request and is rejected for a Copilot-only invocation;
- `--max-writers` controls only deterministic execution-wave calculation;
- `--host`, `--output`, and `--dry-run` control adapter generation;
- trusted doctor observations control only route attestation.

Attempt/review budgets and authorization belong to each task contract. The host applies them while executing the workflow.

## Safe adapter generation

Generation refuses to overwrite a file that lacks the Eclipse generated marker. Identical files are unchanged; generated files can be updated idempotently. Use `--output` and `--dry-run` before writing into an existing project.
