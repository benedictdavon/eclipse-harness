# Eclipse Harness

Eclipse Harness is a skills-first toolkit for architect–worker–reviewer coding workflows. It turns decisions into bounded task contracts, requires evidence from implementation, and gives an independent reviewer a precise acceptance packet.

The name comes from the original Sol + Luna idea: spend scarce reasoning on architecture and review, then delegate bounded implementation economically. Sol/Luna is a reference policy, not a dependency of the protocol.

## Product boundary

Eclipse does not execute agents or manage workflows.

| Eclipse owns | The host owns |
|---|---|
| Role and delegation guidance | Model execution and agent spawning |
| Task, context, result, and review contracts | Filesystem mutation and tools |
| Routing and escalation policy | Git branches, worktrees, and integration |
| Dependency/write-scope guidance | Sandboxing, permissions, and scheduling |
| Review semantics and eval cases | Persistence of workflow status |

Codex, GitHub Copilot, another compatible host, or a human runs the work. Python tooling is optional.

## What v0.1 provides

- portable `eclipse-orchestrate`, `eclipse-execute`, and `eclipse-review` skills;
- setup and diagnostic skills for bootstrap and host-specific capability checks;
- versioned task, context, result, review, role-policy, capability, and evaluation schemas;
- structured stale-plan binding, criterion evidence, command evidence, findings, and escalation semantics;
- dependency-DAG validation and ownership-safe execution-wave guidance;
- a vendor-neutral routing model plus the Sol/Luna reference policy;
- Codex, Copilot, and generic/manual adapters with explicit degradation;
- optional contract, adapter, doctor, and eval utilities;
- cross-platform tests and CI for Python 3.10–3.14.

It does not include canonical run state, a scheduler, recovery journal, worktree manager, migration runtime, process manager, event store, or autonomous model calls.

## Use the skills without Python

1. Make `.agents/skills` available to the host.
2. Invoke `eclipse-orchestrate` with the requirement. It returns task contracts and execution waves.
3. Give one current task contract and its referenced context to an implementation worker following `eclipse-execute`.
4. Give the requirement, current plan, task, result, actual diff, and host-observed validation to an independent reviewer following `eclipse-review`.
5. Route bounded findings back to a worker, architectural findings to the architect, and new authority or destructive actions to a human.

The contract examples in [`examples/contracts`](examples/contracts) are usable as templates. The normative field semantics live in [`protocol`](protocol).

## Optional Python tools

Python 3.10 or later is needed only for the optional CLI:

```bash
python -m pip install eclipse-harness
```

From a checkout:

```bash
python -m pip install -e ".[dev]"
```

Useful checks:

```bash
eclipse validate examples/contracts/task.json --kind task
eclipse validate examples/contracts/result.json --kind result \
  --task examples/contracts/task.json
eclipse check-concurrency path/to/T001.json path/to/T002.json
eclipse adapters generate --host all --dry-run
eclipse --json doctor
```

`eclipse init` copies packaged skills without overwriting existing skill directories. None of these commands owns execution or workflow state.

## Portability

| Capability | Codex CLI/app | GitHub Copilot | Manual/other |
|---|---|---|---|
| Core skills | `.agents/skills` | `.agents/skills` | Copy/read directly |
| Native role wrappers | `.codex/agents/*.toml` | `.github/agents/*.agent.md` | Not required |
| Per-role model intent | Configurable | Host/account dependent | External decision |
| Effective model proof | Host-observed only | Host-observed only | Usually unavailable |
| Reviewer read-only intent | Configured; host may override | Read/search tool intent; enforcement varies | Process policy |
| Contract workflow | Full | Full | Full |

Requested or configured models, reasoning, and permissions are not described as effective unless trustworthy host metadata proves them.

See [Architecture](docs/architecture.md), [Optional CLI](docs/cli-and-configuration.md), [Security](docs/security.md), and the [adapter documentation](docs/adapters).

Version 0.1 is an alpha skills-and-protocol release. The evaluation fixtures are not benchmark conclusions or cost-saving claims. Licensed under the [MIT License](LICENSE).
