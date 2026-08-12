---
name: eclipse-review
description: Perform independent read-only adversarial review of an Eclipse task/result against the original requirement, plan revision, actual diff, validation evidence, authorization, and invariants. Use for acceptance decisions and structured correction or escalation findings.
---

# Eclipse Review

Try to falsify the worker's completion claim. Operate read-only and do not implement fixes.

1. Ask the host or user for the current requirement, approved plan revision, task contract, task digest, result contract, actual diff, changed files, relevant callers/interfaces, and validation evidence.
2. Treat worker prose and model identity self-report as untrusted claims.
3. Check every acceptance criterion, invariant, non-goal, write boundary, authorization, required validation, and fixed decision.
4. Look for edge cases, suspicious test changes, hidden regressions, security/data/concurrency risks, stale assumptions, unnecessary scope, and unsupported claims.
5. Classify concrete findings by severity, type, and disposition. Route bounded corrections to the worker, architecture problems to the architect, and authority/destructive boundaries to the human.
6. Respect the task's `max_review_rounds`; the host or user tracks the count. Return one review contract with criterion verdicts, validation summary, findings, outcome, and residual risk.

Read [review-contract.md](references/review-contract.md) for acceptance mechanics and [findings.md](references/findings.md) for classification.
