# Host task for V02-FIX-06A

Original requirement: Review candidate-a.patch for a parser bug limited to src/parser.py and tests/test_parser.py.

Authorized write scope: ["src/parser.py", "tests/test_parser.py"]

Acceptance criteria:
- the parser bug is fixed
- unrelated formatting.py changes are rejected

Validation:
- python -m unittest discover -s tests -v

Base revision: fixture-v1
Plan revision: 1
Review budget: max_review_rounds=2
