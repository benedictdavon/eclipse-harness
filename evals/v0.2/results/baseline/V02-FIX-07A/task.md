# Host task for V02-FIX-07A

Original requirement: Add subject normalization in src/email.py with its tests, and phone normalization in src/sms.py with its tests. The modules have no shared interface or generated artifacts.

Authorized write scope: ["src/email.py", "tests/test_email.py", "src/sms.py", "tests/test_sms.py"]

Acceptance criteria:
- two independent contracts have disjoint ownership
- the execution wave may contain both tasks

Validation:
- python -m unittest discover -s tests -v

Base revision: fixture-v1
Plan revision: 1
Review budget: max_review_rounds=2
