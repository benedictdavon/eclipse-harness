# Host task for V02-FIX-07B

Original requirement: Add an email-domain helper and separately document SMS country-code behavior. Keep the source and documentation work in independent contracts.

Authorized write scope: ["src/email.py", "tests/test_email.py", "docs/sms.md"]

Acceptance criteria:
- ownership is disjoint
- no false dependency is introduced

Validation:
- python -m unittest tests.test_email -v

Base revision: fixture-v1
Plan revision: 1
Review budget: max_review_rounds=2
