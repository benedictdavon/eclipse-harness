# Host task for V02-FIX-08A

Original requirement: Add CSV and JSON handlers. Both must register in src/registry.py and update the same registry test.

Authorized write scope: ["src/csv_handler.py", "src/json_handler.py", "src/registry.py", "tests/test_registry.py"]

Acceptance criteria:
- shared registry ownership is recognized
- writers are serialized or linked by dependency

Validation:
- python -m unittest discover -s tests -v

Base revision: fixture-v1
Plan revision: 1
Review budget: max_review_rounds=2
