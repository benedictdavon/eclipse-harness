# Eclipse Harness

Eclipse Harness is a portable protocol and toolset for architect–worker–reviewer coding workflows. It turns architectural decisions into bounded task contracts, requires structured execution evidence, validates results independently, and escalates only at decision or authorization boundaries.

The name comes from the original Sol + Luna idea: use scarce reasoning for architecture and review, and economical reasoning for bounded implementation. The core does not depend on those model names. Sol/Luna ships as a reference policy built on vendor-neutral roles, capabilities, risk, cost tier, reasoning effort, permissions, and fallback behavior.

## What v0.1 provides

- versioned task, result, review, configuration, capability, run-state, policy, and evaluation schemas;
- typed Python models and semantic validators;
- explicit lifecycle transitions, plan revision binding, stale-result rejection, retry/review budgets, and recovery checks;
- dependency DAG validation, write-glob overlap detection, shared-interface/exclusive-resource guards, and execution waves;
- repository-bounded authorization, secret detection/redaction, command safety checks, and trust classes;
- canonical `.eclipse/runs/<id>/run.json` state with generated `ACTIVE_PLAN.md` and `HANDOFF.md` views;
- policy-driven routing and the Sol/Luna reference ladder;
- generated Codex and GitHub Copilot role adapters;
- meaningful host/route/permission/worktree diagnostics;
- a manual fallback workflow, legacy `soluna-workflow` migration, git worktree primitives, structured events/usage, and an evaluation harness;
- four portable Agent Skills under `.agents/skills`;
- layered tests and a Linux/macOS/Windows Python 3.10+ CI matrix.

Eclipse is a protocol-and-skill suite, not a general provider runtime. Codex, Copilot, another compatible host, or a human remains responsible for executing agents.

## Installation

Python 3.10 or later is required.

```bash
python -m pip install eclipse-harness
```

For development:

```bash
python -m pip install -e ".[dev]"
```

Until a package is published, install from a checkout or pinned Git revision. Repository-scoped skills in this project are available directly to Codex and Copilot when the checkout is opened as the project.

## Quick start

```bash
eclipse init
eclipse adapters generate --host all --dry-run
eclipse --json doctor
eclipse validate examples/contracts/task.json --kind task
```

Create canonical run state and add a contract:

```bash
eclipse plan create \
  --run-id feature-001 \
  --objective "Implement the approved feature" \
  --plan-digest sha256:approved-plan \
  --base-revision "$(git rev-parse HEAD)"

eclipse plan add-task --run-id feature-001 path/to/task.json
eclipse task start --run-id feature-001 --task-id T001
```

After the worker returns a result and the independent reviewer returns a review:

```bash
eclipse result ingest --run-id feature-001 path/to/result.json  # Git diff is observed
eclipse review ingest --run-id feature-001 --human-approval \
  --principal "$USER" path/to/review.json
eclipse render feature-001
eclipse --json status feature-001
```

The global `--json` flag precedes the subcommand: `eclipse --json <command> ...`. Outside a Git
working tree, a trusted root operator must repeat `--observed-file PATH` for every changed path.

## Workflow

1. The architect turns ambiguity into a plan revision and task contracts.
2. The harness validates scope, dependencies, routing intent, authorization, and concurrency.
3. A bounded executor implements one contract and returns structured evidence.
4. The harness rejects stale, incomplete, or unauthorized results.
5. An independent read-only reviewer checks the requirement, plan, packet, diff, evidence, and risks.
6. Bounded findings become worker correction contracts; architectural findings return to the architect; authority boundaries return to the human.

See [Architecture](docs/architecture.md), [Contracts and state](docs/contracts-and-state.md), [CLI and configuration](docs/cli-and-configuration.md), and [Security](docs/security.md).

## Portability promise

Portable semantics are controlled by Eclipse: contracts, schemas, roles, lifecycle, routing intent, evidence, validation, state, and policy.

Host behavior is adapter-specific: actual model choice, effective reasoning effort, agent spawning, context behavior, tool access, sandbox enforcement, and native concurrency. Eclipse reports capability gaps and degrades to policy-only or manual mode. It does not claim identical behavior across hosts.

| Capability | Codex CLI/app | GitHub Copilot | Manual/other |
|---|---|---|---|
| `.agents/skills` core | Supported | Supported | Copy/read contracts |
| Native profiles | `.codex/agents/*.toml` | `.github/agents/*.agent.md` | Not required |
| Per-role model intent | Configurable | Host/account dependent | External decision |
| Effective model proof | Host-observed only | Host-observed only | Unavailable |
| Read-only reviewer | Configured; runtime overrides surfaced | Read/search tool profile; enforcement varies | Process policy |
| Task/result/review protocol | Full | Full | Full |

Platform details and current official-source verification are in [Codex](docs/adapters/codex.md), [Copilot](docs/adapters/copilot.md), and [Platform verification](docs/platform-verification.md).

## Project status

Version 0.1 is an alpha protocol release. It includes no live model credentials, external-provider marketplace, autonomous provider execution, billing probe, GUI, or fabricated benchmark conclusion. See [Known limitations](docs/limitations.md) and [Evaluation methodology](docs/evaluation.md).

Licensed under the [MIT License](LICENSE).
