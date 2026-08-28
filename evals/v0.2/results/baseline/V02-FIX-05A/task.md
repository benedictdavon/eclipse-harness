# Host task for V02-FIX-05A

Original requirement: Review candidate-a.patch for the requirement that discounts never make a total negative.

Authorized write scope: ["src/discount.py", "tests/test_discount.py"]

Acceptance criteria:
- implementation clamps at zero
- the original negative-total regression test remains meaningful

Validation:
- python -m unittest discover -s tests -v

Base revision: fixture-v1
Plan revision: 1
Review budget: max_review_rounds=2
