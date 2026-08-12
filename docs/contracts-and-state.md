# Contracts and host-owned state

The normative contract documents live under [`protocol/`](../protocol). JSON is the machine-readable interchange format; Markdown may present a human view but is not parsed as protocol state.

## Contract set

- A **Context Manifest** provides the smallest sufficient context and classifies each source's trust.
- A **Task Contract** binds one objective to a plan revision, dependencies, scope, policy intent, acceptance, validation, authorization, and stop conditions.
- A **Result Contract** reports changed files, implementation summary, acceptance evidence, validation commands, blockers, risks, and escalation.
- A **Review Contract** binds to the exact task and result digests and reports independent verdicts, findings, outcome, and residual risk.

Validate with the optional CLI when available:

```bash
eclipse validate context.json --kind context
eclipse validate task.json --kind task
eclipse validate result.json --kind result --task task.json
eclipse validate review.json --kind review --task task.json --result result.json
```

The skills remain usable when these commands are unavailable.

## Plan revisions and stale work

The host or user decides which plan revision is current. Every task, result, and review carries revision and digest bindings. When architecture changes, the architect creates a new revision and marks every obsolete nonterminal task superseded. That includes blocked, escalated, changes-requested, and ready-for-correction work.

Old results are rejected by comparing their bindings to the current task packet. Eclipse does not persist a canonical run record or recover host workflow state.

## Command evidence

Task `validation` lists commands that contribute to acceptance. Result `commands` must include every required validation and may also disclose bounded exploratory/debugging commands. Undeclared commands are not automatically invalid, but all recorded commands remain subject to task authorization.

Cross-field semantics are strict:

- `passed` requires `exit_code: 0`;
- `failed` requires a non-zero integer exit code;
- `not-run` requires `exit_code: null`.

Sensitive or effectful commands—network, dependency installation, credentials, destructive actions, mutations, or external effects—must be authorized and disclosed. Ordinary read-only exploration may be summarized rather than logged command by command.

## Compatibility

Contract, capability, policy, and evaluation versions are explicit. Breaking field semantics require a schema version change and a documented old-to-new mapping. Eclipse does not ship a general migration engine.
