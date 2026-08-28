# Host task for V02-FIX-09B

Original requirement: Preserve integer retry delays. Candidate A returns float values; candidate B restores integers but removes the upper-bound guard. Respect max_review_rounds=2.

Authorized write scope: ["src/retry.py", "tests/test_retry.py"]

Acceptance criteria:
- return type remains int
- attempts above 8 raise ValueError
- no third correction cycle is issued

Validation:
- python -m unittest discover -s tests -v

Base revision: fixture-v1
Plan revision: 1
Review budget: max_review_rounds=2
