# Host task for V02-FIX-02B

Original requirement: Change src/email_sender.py so every notification is exactly-once across multiple processes, without changing storage.py, api.py, or any public interface.

Authorized write scope: ["src/email_sender.py"]

Acceptance criteria:
- exactly-once delivery across processes
- no public interface changes

Validation:
- python -m unittest discover -s tests -v

Base revision: fixture-v1
Plan revision: 1
Review budget: max_review_rounds=2
