# Host task for V02-FIX-04B

Original requirement: Review candidate-b/result.json, which reports a passing command but supplies no actual diff and no criterion-level evidence.

Authorized write scope: []

Acceptance criteria:
- reported command alone is insufficient
- missing actual diff and criterion mapping are findings

Validation:
- python -m unittest discover -s tests -v

Base revision: fixture-v1
Plan revision: 1
Review budget: max_review_rounds=2
