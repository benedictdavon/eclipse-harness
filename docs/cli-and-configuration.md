# CLI and configuration

## Commands

| Command | Purpose |
|---|---|
| `eclipse init` | Create strict default configuration without overwriting existing state. |
| `eclipse validate` | Validate config/task/result/review syntax and semantics. |
| `eclipse inspect` | Report contract kind, version, and canonical digest. |
| `eclipse plan create/add-task/revise` | Create and version canonical run plans. |
| `eclipse task start` | Start one ready attempt within budget. |
| `eclipse result ingest` | Verify worker evidence against an observed Git diff and persist it. |
| `eclipse review ingest` | Persist review evidence with explicit human/host approval attestation. |
| `eclipse status` | Show canonical run state. |
| `eclipse render` | Generate plan/handoff views from state. |
| `eclipse check-concurrency` | Validate DAG/ownership and calculate safe waves. |
| `eclipse doctor` | Diagnose host, routes, permissions, profiles, and git. |
| `eclipse adapters generate` | Generate idempotent host profiles; supports dry-run. |
| `eclipse migrate soluna-workflow` | Inspect and conservatively migrate recognizable legacy state. |
| `eclipse worktree prepare` | Create task branch/worktree at an explicit base commit. |
| `eclipse eval run` | Execute a recorded deterministic evaluation suite. |

Global `--json` precedes the subcommand, for example `eclipse --json doctor`. Stable exit codes are `0` for success, `2` for invalid input/operation, and `3` when doctor finds an error-level diagnostic.

## Configuration

`.eclipse/config.json` is strict and rejects unknown fields. It separates:

- policy and human-interaction profile;
- host adapter selection;
- unverified-route fallback behavior;
- writer/reader concurrency;
- attempt/review budgets;
- git isolation and clean-base rules;
- evidence/staleness validation;
- network, repository trust, secret, and run-state security defaults.

Profiles are `strict`, `standard`, and `fast`; all retain human authority for credentials, destructive actions, target changes, and external side effects. In strict routing, unverified effective models fail closed. Standard defaults to policy-only; manual produces packets without native spawning assumptions.

## Adapter installation

Generation refuses to overwrite a file that lacks the Eclipse generated marker. Existing generated content is updated idempotently; identical files are unchanged. Use `--output` for staging and `--dry-run` before installing into an existing project.
