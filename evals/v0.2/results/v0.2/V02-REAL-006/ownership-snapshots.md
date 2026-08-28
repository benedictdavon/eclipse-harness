# Ownership snapshots

## V02-REAL-006-T1 boundary

- Host serialization: mandatory; actual concurrency `false`.
- Exact status: ` M tests/test_itsdangerous/test_encoding.py`
- Changed file: `tests/test_itsdangerous/test_encoding.py`
- Patch summary: Added exactly the `256 -> b"\x01\x00"` tuple to the existing `test_int_bytes` parameterization; production code and documentation were unchanged.

## V02-REAL-006-T2 boundary

- Host serialization: mandatory; actual concurrency `false`.
- Exact status: ` M docs/encoding.rst`; ` M tests/test_itsdangerous/test_encoding.py` (the latter is the retained T1 change).
- Changed file owned by T2: `docs/encoding.rst`
- Aggregate patch summary: `docs/encoding.rst | 4 ++++`; `tests/test_itsdangerous/test_encoding.py | 8 +++++++-`; 2 files changed, 11 insertions, 1 deletion.
- T2 patch summary: Added one concise paragraph describing `-`/`_` substitution and omitted/restored `=` padding; code and tests were unchanged during T2.
