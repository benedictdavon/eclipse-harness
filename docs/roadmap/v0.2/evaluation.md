# v0.2 Evaluation Plan

## Method

The campaign evaluates the unmodified v0.1 skills first and the candidate v0.2 skills second. Case wording, repository commits, acceptance criteria, policy, evaluator rules, and host configuration remain identical. Raw outputs, actual diffs, command evidence, independent review artifacts, and deterministic scorer results are retained by case ID.

Controlled cases isolate one role invariant. Real-repository cases exercise the complete architect → worker → reviewer loop unless a valid stop/escalation is itself the expected terminal behavior. A run qualifies only when it reaches acceptance, changes requested, architecture/human escalation, or a classified environment failure with enough evidence to evaluate the skill behavior.

## Frozen identity

- Eclipse baseline: `v0.1.0-alpha.1` / `8a674fafe1f1d03c34e27c7a875752a0138f5e2b`
- Policy: `policies/sol-luna.json` at the baseline commit
- Adapter: manual portable contract transfer over ChatGPT Work collaboration threads
- Effective model and reasoning: unverified
- Network: disabled for workers unless a case explicitly says otherwise
- Worker descendants: disabled
- Maximum implementation attempts: 2
- Maximum review rounds: 2
- Evaluation definition: `evals/v0.2/campaign.json` plus the referenced controlled/real case files

## Controlled campaign

Twenty frozen cases cover all ten required families, with two variants per family:

1. bounded implementation;
2. architecture blocker;
3. weak/vague requirement;
4. result without sufficient evidence;
5. test weakening;
6. unauthorized refactor;
7. safe parallelism;
8. unsafe parallelism;
9. repeated correction loop;
10. prompt injection.

Exact prompts, scopes, acceptance criteria, validation, and expected evaluator assertions are in `evals/v0.2/controlled/cases.json`. Deterministic seed repositories are under `evals/v0.2/controlled/fixtures/`.

## Pinned real repositories

| Repo ID | Repository | Commit | Archetype |
|---|---|---|---|
| `REAL-PY-LIB` | https://github.com/pallets/itsdangerous | `672971d66a2ef9f85151e53283113f33d642dabd` | small Python library / mature OSS |
| `REAL-PY-APP` | https://github.com/miguelgrinberg/microblog | `a975ef64864354867c88e0ed3a17ba7d17dca752` | medium Python web application / legacy-style single app |
| `REAL-TS-NODE` | https://github.com/sindresorhus/ky | `3419113b48e034fdcf8fa6bd3be3da7b3d0d758f` | TypeScript/Node library / mature OSS |
| `REAL-NEXT` | https://github.com/vercel/next-learn | `bb2558441a6673ab76c89914c25018bffa27a2ba` | React/Next educational frontend collection |
| `REAL-MONOREPO` | https://github.com/changesets/changesets | `b4dc91f545ff2afead214278b7b5ebc8d4e96322` | TypeScript multi-package monorepo |

Thirty exact tasks and their categories are in `evals/v0.2/real/cases.json`. The fixed category totals are 6 bounded changes, 6 multi-file changes, 5 bug fixes, 4 refactors, 3 architecture-sensitive tasks, 3 parallelization candidates, and 3 review/correction cases.

## Evidence and scoring

For each run, retain:

- architect output and task contract;
- worker output/result contract or classified escalation;
- actual patch and changed-file list;
- validation output and exit codes;
- independent review output;
- deterministic acceptance and scope checks;
- invocation/correction/escalation counts;
- context/task-contract size and referenced files;
- measured usage only if the host exposes it.

The deterministic scorer checks required artifact presence, scope, acceptance mappings, command evidence, diff integrity, role stop conditions, and expected case-specific assertions. It does not treat worker or reviewer prose as proof.

## Freeze rule

The evaluation freeze is the first commit on `agent/eclipse-harness-v0.2`. After baseline execution, the case definitions, prompt packets, expected assertions, and pinned commits are immutable. A failing case remains in all reports. Any evaluation flaw is classified explicitly and the affected before/after comparison is marked invalid or incomparable; it is not rewritten in place.
