# v0.2 Implementation Specification

## Baseline and boundary

- Baseline tag: `v0.1.0-alpha.1`
- Baseline commit: `8a674fafe1f1d03c34e27c7a875752a0138f5e2b`
- Baseline tree: `68c8e4ac54d35576bfdcaf18e9dcba10afbb8908`
- Product boundary: skills, contracts, policy, adapters, evals, and optional deterministic validation only.

The host owns model execution, delegation, filesystem mutation, git, sandboxing, scheduling, retries, workflow state, and integration. No v0.2 work package may introduce a runtime, scheduler, process manager, worktree manager, persistence layer, recovery journal, migration runtime, or plugin framework.

## Current repository inventory

- Skills: `.agents/skills/eclipse-{orchestrate,execute,review,bootstrap,doctor}`
- Protocol: `protocol/{context-manifest,task-contract,result-contract,review-contract,routing-policy}.md`
- Policy: `policies/sol-luna.json`
- Host adapters: `.codex/`, `.github/agents/`, `docs/adapters/`, and `src/eclipse_harness/adapters/`
- Contracts: `schemas/`, `examples/contracts/`, and `src/eclipse_harness/contracts.py`
- Evaluation: `examples/evaluation/` and `src/eclipse_harness/evaluation.py`
- Optional tooling: `src/eclipse_harness/cli.py`, deterministic validators, adapter rendering, doctor diagnostics, and recorded-eval aggregation
- Validation: `tests/`, `tools/self_check.py`, and `.github/workflows/ci.yml`

## Verified host facts

| Host | Capability | Verified behavior | Official source | Date |
|---|---|---|---|---|
| ChatGPT/Codex | Agent Skills | Repository skills are discovered under `.agents/skills`; skills use progressive disclosure and may include references/scripts. | https://developers.openai.com/codex/build-skills | 2026-08-13 |
| ChatGPT/Codex | Subagents | Current Codex surfaces support explicit subagent workflows; parallel writes require care and the host owns execution. | https://developers.openai.com/codex/agent-configuration/subagents | 2026-08-13 |
| Codex | Project instructions | `AGENTS.md` is layered from repository root toward the working directory. | https://developers.openai.com/codex/agent-configuration/agents-md | 2026-08-13 |
| GitHub Copilot | Skills and agents | Copilot cloud/IDE surfaces expose skills and custom agents, but availability and delegation semantics vary by surface and policy. | https://docs.github.com/copilot/concepts/agents/cloud-agent/about-cloud-agent | 2026-08-13 |
| GitHub Copilot | Reviewer behavior | Copilot review can use head-branch skills, is not guaranteed to find every issue, and requires validation/human review. | https://docs.github.com/copilot/concepts/agents/code-review | 2026-08-13 |

No current documentation proves the effective model or permission state of these evaluation runs. Requested/configured/effective values remain distinct and effective identity is recorded as unverified unless trusted host metadata exists.

## Work packages

| Requirement | Exact files | Change | Evidence |
|---|---|---|---|
| Freeze evaluation | `evals/v0.2/**`, `docs/roadmap/v0.2/evaluation.md` | Add controlled fixtures, 20 cases, 5 pinned repos, 30 real tasks, prompts, scorers, and hashes. | Freeze commit and manifest validation |
| Baseline | `evals/v0.2/results/baseline/**` | Run the complete campaign against the unmodified v0.1 skills. | Raw run artifacts and aggregate report |
| Findings | `docs/roadmap/v0.2/findings.md` | Classify every baseline defect and map it to invariant, root cause, fix, and regression. | Finding-to-case links |
| Skill hardening | `.agents/skills/**`, relevant `protocol/**` | Make only changes supported by baseline evidence. | Focused regressions and post-fix campaign |
| Rerun | `evals/v0.2/results/v0.2/**`, `before-after.md`, `release-evidence.md` | Rerun the frozen campaign and classify improved/unchanged/regressed/incomparable. | Same case IDs and frozen task hashes |
| Validation | `tests/**`, CI | Preserve skills-first boundary and validate schemas, skills, security, adapters, packaging, and supported platforms. | Local and GitHub Actions results |

## Skill and protocol change rule

No production skill, protocol, contract, adapter, policy, or optional-tool behavior changes before the v0.1 baseline is complete. Every later change must cite a recorded finding and at least one frozen regression case. `SKILL.md` remains concise; supporting detail goes in one-level references.

## Human gates

No paid-host token or cost telemetry is available from the current host. Token/cost fields will be marked unavailable, not estimated. Ambiguous evaluator judgments are retained and labeled for human review rather than silently counted as success.

## Freeze checklist

- [x] no runtime or scheduler scope added
- [x] all mandatory requirements mapped
- [x] current Codex and Copilot facts checked against official sources
- [x] controlled and real case files hashed
- [x] evaluation freeze commit created: `0ed50a49b506789e684baaa1dbe055f3c4f64e5f`
