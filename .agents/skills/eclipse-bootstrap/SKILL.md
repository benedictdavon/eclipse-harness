---
name: eclipse-bootstrap
description: Install or verify Eclipse skills, select the Codex, Copilot, or manual adapter, explain capability degradation, and confirm the skills-first workflow works without the optional Python CLI. Use for setup, updates, or host selection.
---

# Eclipse Bootstrap

Prepare Eclipse as a skills-and-contract bundle, not as a runtime.

1. Identify the host and its current skill, custom-agent, model-selection, permission, and delegation capabilities.
2. Make the five Eclipse skill directories available under `.agents/skills` without overwriting user-owned files.
3. Select the Codex, Copilot, or manual adapter. Treat adapter files as host guidance, not proof of effective models or permissions.
4. Verify that `orchestrate -> execute -> review` can be followed from the skill and protocol documents alone.
5. If Python tooling is available, use `eclipse validate`, `eclipse check-concurrency`, or `eclipse doctor` as optional checks. Do not make them prerequisites.
6. Report installed files, native/emulated/manual/unsupported capabilities, requested versus effective settings, and any user action required.

The host owns model execution, agent spawning, filesystem changes, git, sandboxing, scheduling, and tools. Eclipse owns role guidance, contracts, policy, review semantics, and evaluation cases.

Read [installation.md](references/installation.md) for safe setup and [capability-modes.md](references/capability-modes.md) for fallback labels.
