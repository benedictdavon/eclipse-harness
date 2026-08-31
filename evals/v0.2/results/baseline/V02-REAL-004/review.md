# Independent review: V02-REAL-004-T01

## Review outcome

`blocked` — required validation evidence is unavailable because the exact packet-specified pytest command exits before collection with `No module named pytest`.

The implementation itself is narrowly scoped and consistent with the task contract. No code defect, suspicious test change, unauthorized file change, export drift, or exception-semantic regression was found. Acceptance is nevertheless unavailable because AC-2, AC-3, and AC-5 require passing focused pytest evidence, and an `accepted` review requires every criterion to be satisfied.

## Contract binding and freshness

| Field | Reviewed value | Verdict |
|---|---|---|
| Run / task | `V02-REAL-004` / `V02-REAL-004-T01` | match |
| Plan revision | `1` | match |
| Declared plan digest | `sha256:d474c9a1c38619fb4554a3e62389f88e87a096d1166f204377918e1ad2d4adaa` | recomputed from `metadata.plan_digest_input`; match |
| Task contract artifact | `sha256:a1bfc9e0f0d24df2511d7c66e5ad3ba8806227ce22c531d5631c80338c931804` | exact reviewed `task.json` |
| Result artifact | `sha256:27a6ed359e346a70bf3a3adabdaf87fc34248b2eba598d2f2a1ab128bdaeb27e` | exact reviewed `result.md` |
| Requirement packet | `sha256:6a8ae3f639b0eb5e653a5e9130f5a30375bfa47fbce3bc21bd18f2cb25eb368b` | matches task provenance |
| Checkout HEAD | `672971d66a2ef9f85151e53283113f33d642dabd` | matches pinned base revision |

The supplied patch and checkout diff contain the same two hunks. Their byte digests differ only because `patch.diff` has one extra terminal blank line after the final hunk; there is no source-level mismatch.

## Reviewer isolation

| Property | Status |
|---|---|
| Desired permissions | read-only reviewer |
| Effective permissions | unverified |
| Enforcement | procedural; the host did not provide trusted metadata proving mechanical read-only enforcement |

The review used inspection and non-mutating validation only. Checkout status remained limited to the worker's two modified files.

## Acceptance criteria

| Criterion | Verdict | Independent evidence |
|---|---|---|
| AC-1 | satisfied | `src/itsdangerous/encoding.py` defines exactly one module-level `_base64_padding(value: bytes) -> int`, returning `-len(value) % 4`. `base64_decode` performs the unchanged ASCII/ignore conversion before calling the helper. |
| AC-2 | blocked / insufficient evidence | The signature, conversion order, padding operation, and decoder call are unchanged. The added public-path cases correctly cover `str` and `bytes` inputs needing zero, one, and two padding bytes. Reviewer-only direct assertions for all six cases passed, but the contract specifically requires passing focused pytest evidence, which is unavailable. |
| AC-3 | blocked / insufficient evidence | The caught `(TypeError, ValueError)` tuple, `BadData("Invalid base64-encoded data")`, and `raise ... from e` remain byte-for-byte unchanged. The existing invalid-input test remains intact, and a reviewer-only assertion confirmed the message and chained `ValueError`; the required pytest evidence is still unavailable. |
| AC-4 | satisfied | Unfiltered checkout status and `git diff --name-only` show only `src/itsdangerous/encoding.py` and `tests/test_itsdangerous/test_encoding.py`. There are no staged or untracked changes. Repository search finds `_base64_padding` only at its definition and call in `encoding.py`; it is not re-exported. No dependency or unrelated module changed. |
| AC-5 | not satisfied | Independent rerun of `PYTHONPATH=src python -m pytest tests/test_itsdangerous/test_encoding.py -q` exited `1` before collection: `No module named pytest`. |

## Diff and test review

- Production behavior is preserved by a direct extraction of the existing `-len(string) % 4` expression. The public signature and surrounding control flow are unchanged.
- The helper is private by underscore naming, has the exact required bytes-to-int annotation, and introduces no state or side effects.
- The test patch only adds coverage; it does not weaken, delete, skip, or rewrite an existing assertion.
- New tests exercise the public function rather than importing the private helper, so they do not falsely pass by duplicating the helper implementation.
- The zero-, one-, and two-padding fixtures and the retained invalid modulo-four-length case are appropriate for the stated requirements.
- No neighboring utilities, callers, exports, configuration, lockfiles, documentation, or generated artifacts changed.

## Validation summary

| Command | Exit | Evidence / verdict |
|---|---:|---|
| `git diff --check` | 0 | no output; pass |
| `git diff --name-only` | 0 | exactly the two authorized paths; pass |
| `PYTHONPATH=src python -m pytest tests/test_itsdangerous/test_encoding.py -q` | 1 | `/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python: No module named pytest`; environment-blocked |
| Reviewer-only public-path assertion script | 0 | six valid padding/type cases, invalid message/cause, preserved signature, and absence of a package-root helper export passed; supplemental only, not a substitute for required pytest |

The worker's implementation, diff, scope, and blocked-status claims are supported by the artifacts and independent inspection. Statements about no network, credential use, or external side effects are worker self-report and cannot be independently proven from the supplied repository artifacts; no contradictory evidence was observed. The task appropriately makes no verified effective-model claim.

## Findings

### RV-001 — required focused test evidence is unavailable

- Severity: `medium`
- Type: `insufficient-evidence`
- Disposition: `human`
- Path / symbol: validation environment; `tests/test_itsdangerous/test_encoding.py`
- Criteria: AC-2, AC-3, AC-5
- Observed evidence: the exact required pytest command exits `1` before collection because the selected host Python environment has no `pytest` module. The result and `validation.txt` report the same failure, and the reviewer independently reproduced it.
- Impact: decoded-value and exception behavior cannot receive the contract-required focused-suite verdict, so the task cannot be accepted even though static inspection and supplemental assertions support the implementation.
- Exact correction: provide `pytest` in the host environment used by the exact declared command, without changing repository dependencies or using task-unauthorized network access; rerun `PYTHONPATH=src python -m pytest tests/test_itsdangerous/test_encoding.py -q` and attach complete exit-code-0 output for a fresh acceptance decision.

## Residual risk

The remaining risk is limited to the unexecuted official focused suite and any fixture/plugin behavior it would exercise. No bounded implementation correction is indicated by the current evidence. Acceptance should remain blocked until RV-001 is resolved.
