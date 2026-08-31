# Result Contract

## Identity and status

- Run ID: `V02-REAL-002`
- Task ID: `V02-REAL-002-implement-bytes-limit`
- Plan revision: `1`
- Plan digest: `416ccdc548cb3890f126d66b6b814a52ee2c95e40a5d1353dc14f066038bca90`
- Base revision: `672971d66a2ef9f85151e53283113f33d642dabd`
- Overall status: `blocked`
- Blocker class: `ENV_FAILURE`
- Implementation status: complete within authorized scope
- Validation status: required focused pytest command failed because `pytest` is unavailable in the pinned environment
- Implementation attempts used: 1 of 2; no implementation retry was needed
- Effective model identity, permissions attestation, and measured resource usage: unavailable from trusted host metadata

## Outcome

Added an explicit length guard to `bytes_to_int`, a focused nine-byte regression test with the exact exception message assertion, and the frozen one-sentence documentation statement. Direct Python validation confirms the new error contract and the existing representative empty, one-byte, and eight-byte round trips. The packet-required pytest suite could not run because the environment does not contain `pytest`; no dependency was installed because network and dependency installation are unauthorized.

## Changed files

1. `src/itsdangerous/encoding.py`
   - Added `len(bytestr) > 8` precondition.
   - Raises `ValueError("bytestr must contain at most 8 bytes")` before the existing padding and unpack path.
2. `tests/test_itsdangerous/test_encoding.py`
   - Added `test_bytes_to_int_too_long` using a nine-byte value.
   - Asserts `ValueError` and compares the captured exception string to the exact required message.
   - Existing `test_int_bytes` cases were left intact.
3. `docs/encoding.rst`
   - Added exactly: ``bytes_to_int`` accepts byte strings containing at most eight bytes.

No other tracked or untracked repository files were changed. The final status inspection showed only the three authorized modified files and no test-generated cache files.

## Decisions and invariants

- Preserved `bytes_to_int(bytestr: bytes) -> int` and its public name.
- Left the zero-through-eight-byte padding and unsigned big-endian unpack expression unchanged.
- Did not alter `int_to_bytes`, base64 helpers, dependencies, configuration, generated output, or any path outside the three authorized write globs.
- Did not use the network, credentials, destructive actions, external effects, formatters, or package installation.

## Command evidence

### Base and state check

Command group:

```text
pwd -P
git rev-parse HEAD
git status --short --untracked-files=all
```

Exit code: `0`

Output:

```text
/workspace/scratch/473866e9940e/eval_workspace/runs/baseline/V02-REAL-002
672971d66a2ef9f85151e53283113f33d642dabd
```

The empty status output established a clean starting tree.

### Required validation 1: focused pytest

Command:

```text
PYTHONPATH=src python -m pytest tests/test_itsdangerous/test_encoding.py -q
```

Exit code: `1` (`failed`)

Output:

```text
/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python: No module named pytest
```

### Required validation 2: documentation assertion

Command:

```text
python -c "from pathlib import Path; text = Path('docs/encoding.rst').read_text(); assert 'bytes_to_int' in text and 'at most eight bytes' in text"
```

Exit code: `0` (`passed`)

Output: none.

### Required validation 3: whitespace check

Command:

```text
git diff --check -- src/itsdangerous/encoding.py tests/test_itsdangerous/test_encoding.py docs/encoding.rst
```

Exit code: `0` (`passed`)

Output: none.

### Required validation 4: scope check

Command:

```text
git diff --name-only
```

Exit code: `0` (`passed`)

Output:

```text
docs/encoding.rst
src/itsdangerous/encoding.py
tests/test_itsdangerous/test_encoding.py
```

### Additional bounded direct runtime validation

The corrected command was:

```text
PYTHONPATH=src python - <<'PY'
from itsdangerous.encoding import bytes_to_int, int_to_bytes

for value in (0, 192, 2**64 - 1):
    assert bytes_to_int(int_to_bytes(value)) == value

assert bytes_to_int(b"") == 0
assert bytes_to_int(b"\xff" * 8) == 2**64 - 1

try:
    bytes_to_int(b"\x00" * 9)
except ValueError as error:
    assert str(error) == "bytestr must contain at most 8 bytes"
else:
    raise AssertionError("ValueError not raised")
PY
```

Exit code: `0` (`passed`)

Output: none. This validates representative zero-, one-, and eight-byte round trips and the exact nine-byte exception contract without requiring pytest.

An earlier optional direct-check command encoded literal `\n` sequences in a `python -c` string and exited `1` with `SyntaxError: unexpected character after line continuation character`. It did not modify any file. The corrected here-document command above was the sole bounded retry and passed.

## Final diff evidence

```diff
diff --git a/docs/encoding.rst b/docs/encoding.rst
@@
 .. autofunction:: base64_decode
+
+``bytes_to_int`` accepts byte strings containing at most eight bytes.
diff --git a/src/itsdangerous/encoding.py b/src/itsdangerous/encoding.py
@@
 def bytes_to_int(bytestr: bytes) -> int:
+    if len(bytestr) > 8:
+        raise ValueError("bytestr must contain at most 8 bytes")
+
     return _bytes_to_int(bytestr.rjust(8, b"\x00"))[0]
diff --git a/tests/test_itsdangerous/test_encoding.py b/tests/test_itsdangerous/test_encoding.py
@@
 def test_int_bytes(value, expect):
     enc = int_to_bytes(value)
     assert enc == expect
     dec = bytes_to_int(enc)
     assert dec == value
+
+
+def test_bytes_to_int_too_long():
+    with pytest.raises(ValueError) as exc_info:
+        bytes_to_int(b"\x00" * 9)
+
+    assert str(exc_info.value) == "bytestr must contain at most 8 bytes"
```

## Acceptance-criterion evidence

| Criterion | Status | Evidence |
|---|---|---|
| `AC-NINE-BYTE-ERROR` | partial | Implementation explicitly raises the exact `ValueError`; the added focused test supplies the required nine-byte input and exact string comparison; corrected direct runtime validation exited 0. The focused pytest test itself could not execute because pytest is absent. |
| `AC-VALID-PRESERVED` | partial | The existing valid path is textually unchanged after the preceding guard. Corrected direct validation exited 0 for existing values `0`, `192`, and `2**64 - 1`, covering empty, one-byte, and eight-byte encodings. The existing parametrized pytest cases could not execute because pytest is absent. |
| `AC-DOC-LIMIT` | satisfied | Documentation diff contains the exact frozen sentence and no other documentation change; the required documentation assertion exited 0. |
| `AC-FOCUSED-PASS` | unsatisfied | The exact required command exited 1 with `No module named pytest`; no passing focused pytest evidence is available. |
| `AC-SCOPE` | satisfied | `git diff --name-only` exited 0 and listed only the three authorized files; `git diff --check` exited 0; final status showed no untracked files. |

## Blockers, deviations, risks, and escalation

- Blocker: `ENV_FAILURE` — the pinned Python environment lacks the `pytest` module.
- Deviation: the required focused pytest validation did not pass. No implementation or scope deviation occurred.
- Additional-validation deviation: the first optional direct Python command had a quoting-induced syntax error; it made no changes and the corrected bounded command passed.
- Residual risk: direct assertions exercise the specified behavior, but the complete focused encoding test module remains unexecuted, so its passing state cannot be claimed.
- Escalation: repair or provide the pinned environment with its expected test dependency available, without changing the repository patch, then rerun exactly `PYTHONPATH=src python -m pytest tests/test_itsdangerous/test_encoding.py -q`. No architectural, public-interface, authorization, or scope expansion is requested.
