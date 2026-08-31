# Evaluation Standard

## Controlled and real evidence

Controlled repositories test exact skill invariants. Real repositories test whether those invariants survive real architecture, tooling, conventions, ambiguity, and context size.

For evaluation-driven releases, pin the Eclipse commit and target repository commits, freeze task wording, acceptance criteria, policy, and host settings, run the complete baseline, classify findings, make only evidence-backed changes, and rerun the same cases. A failed case must not be removed merely because it failed.

Every case records its identifier, type, repository and commit, host and adapter, task category and statement, expected write scope, acceptance criteria, validation, policy, and notes. Every run records available outcome, orchestration, context, review, and usage evidence. Measured and estimated usage remain distinct.

Evaluate in this order:

1. deterministic acceptance checks;
2. actual diff and write-scope checks;
3. an independent reviewer;
4. human review for genuinely ambiguous cases.

Worker self-report is never sufficient evidence. Do not fabricate external users, private-repository authorization, paid model access, package publishing authority, benchmark results, or human approval.
