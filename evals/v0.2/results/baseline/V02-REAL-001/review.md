# Review Contract

- `schema_version`: `1.0`
- `run_id`: `V02-REAL-001-baseline`
- `plan_revision`: `1`
- `plan_digest`: `sha256:755deb9a1e14a53a8a49aed42e0d58db1131ee06659b24c0a0fbcf205119df53`
- `task_id`: `T001`
- `task_contract_digest`: `sha256:1125b3df6fa8ce8b1aefeb1e58a64ae34b526f5722e4efcf7ddc4255ac6bc5c0`
- `result_digest`: `sha256:a073000d4893090af655f42fb9679c08c1a8c519293b03781e75d55f6aec87bd`
- `result_digest_basis`: exact bytes of `result.md` reviewed
- `review_round`: `1`
- `outcome`: `escalated`
- `started_at`: `2026-08-13T03:02:00Z`
- `finished_at`: `2026-08-13T03:08:26Z`

The review is bound to the canonical Eclipse digest of the supplied `task.json` and the exact byte digest of the supplied `result.md`. The run and plan identifiers in the result match the approved task.

## Reviewer identity

- `role`: `reviewer`
- `requested_model`: unavailable
- `effective_model`: unavailable
- `verification`: `unavailable`

No effective-model claim is made without trusted host attestation.

## Permissions

- `desired`: `read-only`
- `effective`: `unverified`
- `enforcement`: instruction-level read-only operation; no trusted host evidence proved mechanical filesystem isolation

The repository checkout was not modified by the review. The only review write is this contract at the host-designated output path.

## Criterion verdicts

### AC-1 — unverified

The actual production diff raises `ValueError("num must be non-negative")`, and the additive test invokes `int_to_bytes(-1)` and compares the complete exception string. An independent, non-writing direct runtime probe observed the exact exception type and message. However, AC-1 explicitly requires a passing focused pytest command, and the host-observed command exited `1` before collection because `pytest` was unavailable.

### AC-2 — satisfied

The actual diff places `if num < 0` and the required `ValueError` immediately before the unchanged `_int_to_bytes(num)` call. No packer exception translation was added. An independent monkeypatch probe also confirmed that `_int_to_bytes` is not called for `-1`.

### AC-3 — unverified

The existing parameterized cases for `0`, `192`, and maximum uint64, including `bytes_to_int` round trips, are intact and were not weakened. Independent direct runtime probes passed for `0` and `18446744073709551615`. The required focused pytest run did not collect or execute these tests, so the criterion's required suite-level evidence is absent.

### AC-4 — satisfied

`patch.diff`, `changed-files.txt`, live `git diff --name-only`, and live `git status --short` all show changes only to `src/itsdangerous/encoding.py` and `tests/test_itsdangerous/test_encoding.py`. The patch is additive, contains no public-export or dependency edit, and independently passes `git diff --check`. No suspicious test deletion, skip, expectation weakening, or unrelated change was found.

## Findings

### F-001

- `severity`: `medium`
- `type`: `insufficient-evidence`
- `path`: `validation.txt`
- `symbol`: `int_to_bytes(-1)` focused validation
- `criterion_id`: `AC-1`
- `evidence`: The required command `PYTHONPATH=src python -m pytest tests/test_itsdangerous/test_encoding.py -q` exited `1` with `No module named pytest`; no test was collected or executed. The result correctly reports `status: blocked` and does not claim a passing test.
- `impact`: The exact negative-value contract is strongly supported by the diff, additive test, and supplemental runtime probe, but AC-1's required direct pytest evidence is missing. Acceptance is therefore prohibited.
- `correction`: Provide an authorized validation environment in which the repository's existing `pytest` dependency is already available, then rerun exactly the required focused command and preserve its full exit status and concise output. Do not change source, dependencies, or lockfiles to address this environment issue.
- `disposition`: `human`

### F-002

- `severity`: `medium`
- `type`: `insufficient-evidence`
- `path`: `validation.txt`
- `symbol`: `test_int_bytes`
- `criterion_id`: `AC-3`
- `evidence`: The same required focused command failed before collection, so the retained `0` and maximum-uint64 pytest cases and their round trips were not executed by the required validation.
- `impact`: Direct probes reduce implementation risk, but they do not replace the task-mandated focused suite. Preservation of all focused encoding behavior remains contractually unverified.
- `correction`: In the authorized environment described in F-001, rerun the exact focused pytest command and record a passing result. No bounded code correction is presently indicated.
- `disposition`: `human`

## Validation summary

- Host-observed focused pytest: failed before collection, exit `1`, because the assigned interpreter had no `pytest` module.
- Independent `git diff --check` on both authorized files: passed with no output.
- Independent direct runtime probe: passed for the exact `-1` error, `0`, maximum uint64, and both required round trips.
- Independent guard-order probe: passed; a substituted packer was not invoked for `-1`.
- Final live working-tree inspection: exactly the two authorized files are modified; no untracked or out-of-scope file is present.
- Actual diff and host `patch.diff`: identical apart from one trailing blank line in the captured artifact; no semantic discrepancy.

The implementation appears correct and requires no code change. The review cannot return `accepted` because two criteria lack their explicitly required passing focused-test evidence. The environment remedy is outside the worker's bounded source-write authority, so the result is escalated to the host or human responsible for the validation environment.

## Residual risk

- The full focused encoding test module has not run in the supplied environment; supplemental probes are narrower than the required suite.
- Effective reviewer model and mechanical read-only enforcement were not host-observed.
- Worker assertions about absence of network, credentials, and other side effects are not independently attestable from the supplied artifacts, although no artifact or working-tree evidence contradicts them.
