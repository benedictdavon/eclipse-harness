# GitHub Copilot adapter

Eclipse uses the shared `.agents/skills` source plus repository custom agents in `.github/agents/*.agent.md`.

Generated profiles use current portable tool aliases:

- architect: `read`, `search`;
- worker: `read`, `search`, `edit`, `execute`;
- reviewer: `read`, `search`.

They set `disable-model-invocation: true` so the user/host selects them deliberately and omit `model`. Available model strings, selection, reasoning support, and account access vary across Copilot CLI, cloud agent, app, and IDE surfaces. Omitting the model is an honest host-default fallback rather than a false Sol/Luna claim.

The tool list expresses desired capability. Unrecognized tools may be ignored, and exact enforcement varies by surface. Copilot supports native/custom agent invocation and may delegate, but Eclipse does not assume deterministic automatic topology, per-role reasoning parity, or worktree isolation.

Use:

```bash
eclipse adapters generate --host copilot --dry-run
eclipse adapters generate --host copilot
```

The portable contract/manual workflow remains fully usable if native orchestration is unavailable: give a task JSON to a selected worker, validate its result, then give the task/result/diff packet to the reviewer.
