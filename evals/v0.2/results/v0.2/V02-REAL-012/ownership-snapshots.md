# Ownership snapshots

## V02-REAL-012-T1

- Task-local files: `app/models.py`, `tests.py`
- Scope: avatar guard and exact tests only
- Validation: `python -m compileall -q app tests.py`, exit 0

## V02-REAL-012-T2

- Task-local file: `app/templates/errors/404.html`
- Scope: three translatable strings only
- Validation: `python -m compileall -q app tests.py`, exit 0
- Host serialization retained T1 files in the integrated status; they are not attributed to T2.
