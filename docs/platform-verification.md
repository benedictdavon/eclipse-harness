# Platform verification — 2026-08-12

The adapter implementation was checked against current official OpenAI and GitHub documentation on 2026-08-12.

## OpenAI Codex

Official documentation establishes:

- repository skills under `.agents/skills`;
- project custom agents under `.codex/agents`;
- required custom-agent fields `name`, `description`, and `developer_instructions`;
- role files may set `model`, `model_reasoning_effort`, and `sandbox_mode`;
- `agents.max_concurrent_threads_per_session` is the current concurrency field and `max_threads` is legacy;
- project `.codex/config.toml` loads only for trusted projects;
- subagents inherit parent/live permission overrides, although role-specific read-only intent can be configured.

References:

- https://developers.openai.com/codex/agent-configuration/subagents
- https://developers.openai.com/codex/config-advanced
- https://developers.openai.com/codex/config-reference
- https://developers.openai.com/codex/build-skills
- https://developers.openai.com/codex/agent-configuration/agents-md

Current documentation describes configuration intent but cannot prove the effective model/permissions of a particular run. Eclipse therefore requires trusted host-observed metadata for attestation.

## GitHub Copilot

Official documentation establishes:

- shared project skills under `.agents/skills`;
- project custom agents under `.github/agents` with `.agent.md` files;
- required `description` plus optional `name`, `tools`, `model`, `disable-model-invocation`, and `user-invocable`;
- portable tool aliases including `execute`, `read`, `edit`, `search`, and `agent`;
- Copilot CLI can select a custom agent and model programmatically;
- model availability and some custom-agent features vary by product/account; unsupported fields/tool names may be ignored.

References:

- https://docs.github.com/en/copilot/concepts/agents/about-agent-skills
- https://docs.github.com/en/copilot/reference/custom-agents-configuration
- https://docs.github.com/en/copilot/how-tos/copilot-cli/customize-copilot/create-custom-agents-for-cli
- https://docs.github.com/en/copilot/reference/copilot-cli-reference/cli-programmatic-reference

Eclipse omits fixed models from generated Copilot profiles and reports effective settings unverified unless the running host proves them.
