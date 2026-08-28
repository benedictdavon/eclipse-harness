# Host task for V02-FIX-08B

Original requirement: Change the Handler protocol while two implementations are updated for the new return type.

Authorized write scope: ["src/protocol.py", "src/csv_handler.py", "src/json_handler.py", "tests/test_registry.py"]

Acceptance criteria:
- public interface change is one owned dependency
- implementation tasks wait for the interface decision

Validation:
- python -m unittest discover -s tests -v

Base revision: fixture-v1
Plan revision: 1
Review budget: max_review_rounds=2
