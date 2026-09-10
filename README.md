# Eclipse Harness

Coding work becomes difficult to review when tasks are ambiguous, dependencies
are missed, or two workers modify overlapping files. Eclipse provides a
skills-first protocol and optional Python validators for defining bounded task
contracts, checking dependency and write conflicts, and reviewing evidence.

The host or user runs the agents and owns filesystem mutation, tools, Git, and
permissions. Eclipse does not execute agents, schedule a workflow, or provide
a sandbox.

## A small validation walkthrough

The repository includes a complete task contract. After installing the
candidate checkout, validate it:

```bash
eclipse validate examples/contracts/task.json --kind task
```

Observed output on the audited revision:

```text
valid: True
kind: task
schema_version: 1.0
digest: sha256:3a1651d398a73caf883c2e9ea7ecaa784918f7ad42be89292b04a6ea3cbb40d1
```

The strict Python API rejects two tasks that may write the same path. This
uses the same task fixture and demonstrates the conservative conflict policy:

```bash
python - <<'PY'
import copy
import json
from pathlib import Path

from eclipse_harness.concurrency import assert_parallel_safe
from eclipse_harness.contracts import TaskContract
from eclipse_harness.errors import ConcurrencyError

source = json.loads(Path("examples/contracts/task.json").read_text())
tasks = []
for task_id in ("T-A", "T-B"):
    value = copy.deepcopy(source)
    value["task_id"] = task_id
    value["scope"]["write_globs"] = ["src/shared/**"]
    tasks.append(TaskContract.from_dict(value))

try:
    assert_parallel_safe(tasks)
except ConcurrencyError as error:
    print(f"rejected: {error}")
else:
    raise SystemExit("expected write conflict")
PY
```

Observed output:

```text
rejected: T-A/T-B write-overlap: 'src/shared/**' may overlap 'src/shared/**'
```

For a non-strict scheduling recommendation, `eclipse check-concurrency`
validates a dependency DAG and serializes conflicting tasks into safe waves.
It calculates guidance; it does not dispatch those tasks.

## What is included

- typed task, context, result, review, routing, and capability contracts;
- JSON Schemas plus Python-level cross-contract validation;
- dependency-DAG checks and conservative glob/shared-resource conflict checks;
- Codex, Copilot, and manual adapters with explicit degradation;
- optional CLI checks for contracts, adapters, host diagnostics, and recorded
  evaluation cases;
- portable skills for orchestration, bounded execution, review, bootstrap, and
  diagnostics;
- a frozen v0.2 controlled/real-repository campaign with raw evidence retained
  under `evals/`.

The package contains no canonical run database, scheduler, worktree manager,
recovery journal, autonomous model calls, or provider executor. Modules such as
`state.py` and `process.py` are small optional helpers: they validate
transitions or run a bounded subprocess when called by a host; they do not own
workflow state or agent execution.

## Install the candidate checkout

The current repository is the **0.2.0 candidate/draft**. The audited source
revision is not presented as a published stable distribution, so install this
checkout when reproducing the commands above:

```bash
python -m pip install -e ".[dev]"
```

The repository also retains the `v0.1.0-alpha.1` tag as historical release
context. Do not infer that a `pip install eclipse-harness` command resolves the
candidate described here.

## Optional CLI

```bash
eclipse validate examples/contracts/task.json --kind task
eclipse validate examples/contracts/result.json --kind result \
  --task examples/contracts/task.json
eclipse check-concurrency examples/contracts/task.json
eclipse adapters generate --host all --dry-run
eclipse --json doctor
eclipse eval run examples/evaluation/suite.json \
  --outcomes examples/evaluation/recorded-outcomes.json \
  --output evaluation-results/example.json
```

The global `--json` flag precedes the subcommand. `eclipse init` installs
packaged skills without overwriting existing skill directories. The host still
owns current plan state, dispatch, retries, recovery, and permission
enforcement.

## Product boundary

| Eclipse provides | Host or user provides |
|---|---|
| Role guidance and protocol semantics | Model calls and agent spawning |
| Task/result/review contracts | Filesystem writes and command execution |
| Dependency and write-conflict guidance | Branches, worktrees, merges, and Git |
| Adapter configuration as intent | Effective model, sandbox, and permission proof |
| Review and escalation semantics | Scheduling, cancellation, retries, and recovery |

Conflict detection deliberately favors safety: prefix-based glob analysis can
produce false positives and cannot prove semantic independence. It is a
validation/guidance layer, not operating-system isolation. Likewise, declared
read-only intent and adapter settings are not proof of host enforcement.

## Architecture and evaluation

Read [Architecture](docs/architecture.md) for the ownership model and
[Optional CLI](docs/cli-and-configuration.md) for the command surface. The
[evaluation methodology](docs/evaluation.md) explains the frozen cases and
recorded outcomes; those fixtures are evidence for the recorded inputs and
host configuration, not a universal benchmark, cost-saving claim, or live
agent comparison. Usage is labeled measured, estimated, or unavailable.

## Candidate status and limitations

The v0.2 branch is an evaluation-driven candidate/draft, not a completed
release. Core tests, lint, type checks, and package-build results are recorded
from the audited Linux/Python 3.12 checkout. The full GitHub Actions matrix
across Linux, Windows, macOS, and Python 3.10–3.14 is configured in
`.github/workflows/ci.yml`, but a local pass is not a claim that every hosted
matrix job currently passes.

See [Known limitations](docs/limitations.md), the [security notes](docs/security.md),
and the [adapter documentation](docs/adapters). Licensed under the [MIT
License](LICENSE).
