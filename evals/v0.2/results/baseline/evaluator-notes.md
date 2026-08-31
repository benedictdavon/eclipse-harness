# Controlled baseline evaluator notes

- Skill source: detached worktree at `8a674fafe1f1d03c34e27c7a875752a0138f5e2b` (`v0.1.0-alpha.1`). Every role agent was directed to that worktree, never the modified v0.2 branch.
- Host workspaces: clean fixture copies under `eval_workspace/runs/baseline/<case-id>`, each initialized at a local `fixture-v1` commit. Candidate-patch review cases retained the patch as evidence and did not repair or silently apply it to the reviewed checkout.
- Role isolation: each invoked architect, worker, and reviewer ran in a fresh subagent thread. Reviewers did not inherit architect or worker conversation state. Non-applicable roles are null in `run.json` and have zero invocations.
- Expectation isolation: role agents received sanitized `packet.json` files with `expected_behavior` and `notes` removed and were explicitly prohibited from reading evaluator expectations or other results.
- Host usage data: token, cost, and provider-effective-model measurements were unavailable; every `usage` object is empty.
- Frozen-case defects were preserved. The architecture-blocker fixtures have no `tests/` directory; candidate patch files use placeholder `@@` hunk headers and are not mechanically applicable; repeated-correction cases supply neither candidate state nor candidate diffs.
- Integrity limitation: during the initial campaign audit, the host evaluator displayed the frozen case definitions, including expected-behavior fields, before dispatch. Those fields were not passed to any role thread. Raw role outputs therefore remain independently generated, but evaluator-side scoring was not blind. This limitation is preserved rather than hidden.

The 20 records are qualifying because each reached a meaningful terminal evaluation outcome. A qualifying record is not necessarily a successful product outcome; the repeated-correction records, for example, expose an evaluation flaw rather than exercising the intended loop.

# Real-repository baseline evaluator notes

- Thirty additional qualifying runs cover all five frozen repository commits and all frozen task-category minimums. Source clones were never modified; every case used a clean explicit copy at its recorded commit.
- Architects used the detached v0.1 skill bundle read-only. Workers wrote only their explicit case workspace. Reviewers used separate role threads from workers and inspected host-captured patch, status, and validation evidence.
- Some later architect, worker, or reviewer threads processed two cases sequentially under explicit context-isolation instructions because the host had bounded agent slots. This is auditable in the raw artifacts, but per-case thread freshness is not mechanically proven.
- Host constraints prohibited dependency installation and network access. The four ItsDangerous focused pytest commands failed because pytest was absent. Python application compile commands passed, while Flask-backed runtime probes were unavailable. Frozen Node validation commands were dependency-free and passed; upstream package test/type/lint tools were unavailable without `node_modules`.
- Reviewers sometimes escalated on expanded contract validation beyond the frozen packet command. Records preserve the actual terminal review outcome and distinguish the frozen validation check from extra unavailable evidence.
- Real review-correction cases `V02-REAL-018`, `V02-REAL-024`, and `V02-REAL-030` did not include authentic candidate seed patches in their frozen setup. The first two could check corrected end behavior but not candidate-detection capability; the last safely blocked worker dispatch. All remain qualifying terminal runs and are explicitly classified as evaluation flaws, not silently dropped.
- Effective model, tokens, and cost were unavailable. Repeated discovery is null because the host did not expose reliable instrumentation. No values were estimated.

All 50 baseline records are qualifying. Qualification means a meaningful terminal evaluation outcome, not acceptance; 22 real-repository cases ended in an environment failure while preserving their actual patch and review evidence.
