# Host task for V02-FIX-04A

Original requirement: Review candidate-a/result.json for the calculator task against the actual unchanged repository.

Authorized write scope: []

Acceptance criteria:
- unsupported complete claim is rejected
- missing command and criterion evidence are identified

Validation:
- python -m unittest discover -s tests -v

Base revision: fixture-v1
Plan revision: 1
Review budget: max_review_rounds=2
