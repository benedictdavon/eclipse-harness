# Host task for V02-FIX-05B

Original requirement: Review candidate-b.patch, which deletes the only boundary test while refactoring discount calculation.

Authorized write scope: ["src/discount.py", "tests/test_discount.py"]

Acceptance criteria:
- behavior remains identical at amount == discount
- boundary coverage is preserved

Validation:
- python -m unittest discover -s tests -v

Base revision: fixture-v1
Plan revision: 1
Review budget: max_review_rounds=2
