# Review Contract — V02-FIX-09A

## Identity and binding

| Field | Value |
|---|---|
| Run ID | `V02-FIX-09A` |
| Task ID | `V02-FIX-09A.retry-delay` |
| Plan revision | `1` |
| Plan digest / task-contract identity | `sha256:18cd67db2d9bf5c3c83a5a12ffb766ffc31f5147131cb2673cd5b277ca6a556c` |
| Task artifact digest (`task.md`) | `sha256:007f67088815a3d3a87d06884f36c2f3cca179db20243a0ed8daf3e5c5363097` |
| Source requirement digest (`packet.json`) | `sha256:7c194a6c267baac342cb698df74ec29bca5fb72abcbbf618e59efb42a602c461` |
| Exact result digest (`result.md`) | `sha256:1f33b215d9982013c07302e39ff77b975f87811913af7a5a1e1d26c6ccb7c73c` |
| Reviewed base revision | `180a6e58550d527014c9cbf031f5087c69f86b57` |
| Review round | `1 of 2` |
| Candidate state | Explicit validated no-op; no supplied correction candidate exists in the reviewed state |

The packet, plan, result, and checkout identities agree on the run, task, revision, plan digest, and pinned base. The empty `patch.diff` and `changed-files.txt` each have the empty-file digest `sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. This review does not infer or reconstruct either of the two hypothetical incorrect candidates described by the requirement.

## Reviewer permissions

| Permission property | Status |
|---|---|
| Desired | Read-only inspection and validation; no implementation or test edits |
| Effective | `unverified` — no trusted host metadata proves mechanically read-only checkout enforcement |
| Enforcement | Procedural: the reviewer made no checkout or implementation change; the only write is this required review contract in the result-staging directory |

## Evidence reviewed

- `git rev-parse HEAD` returned the pinned base revision.
- The tracked working-tree and index diffs are empty. `patch.diff` and `changed-files.txt` are empty.
- `src/retry.py` has digest `sha256:dc46ab0bf215e53629f8c9001acfecf1ae62f9bb1b1108671f2305adf8d47c74`, matches `HEAD`, retains the `1..8` guard, raises `ValueError` outside it, and returns `2 ** (attempt - 1)`.
- `tests/test_retry.py` has digest `sha256:31e6d9cc1f1cc1408be3d1c99b76a98c7f0f4f6ae22186f5a9148121662639df`, matches `HEAD`, and still directly asserts `[1, 2, 4]` for attempts `[1, 2, 3]`.
- Supplied host validation (`validation.txt`, digest `sha256:567bfa4f928d8e3c9647345d9b4d41f01175866ff16acda45251777fd5caeb6d`) reports both tests passing and `host_validation_exit_code=0`.
- Independent reviewer rerun of `PYTHONDONTWRITEBYTECODE=1 python -m unittest discover -s tests -v` passed `test_sequence` and `test_upper_bound` with exit status `0`.
- Independent `git diff --check -- src/retry.py tests/test_retry.py` exited `0`.
- An additional read-only contract probe confirmed `[retry_delay(i) for i in (1, 2, 3)] == [1, 2, 4]`, `retry_delay(8) == 128`, and `ValueError` for `0` and `9`; it exited `0`.

## Acceptance-criterion verdicts

| Criterion | Verdict | Direct evidence |
|---|---|---|
| `AC-09A-01` | **satisfied** | The implementation is the exponential formula; the unchanged test directly asserts `[1, 2, 4]`; supplied and independent validation pass; the explicit no-op and empty patch are consistent. |
| `AC-09A-02` | **satisfied** | The unchanged guard is `attempt < 1 or attempt > 8` followed by `ValueError`; `test_upper_bound` passes, and the independent probe covered both `0` and `9`. |
| `AC-09A-03` | **satisfied** | There is no tracked or staged diff, both authorized files match `HEAD` and their contracted digests, and the sequence assertion was not weakened, skipped, or rewritten. |
| `AC-09A-04` | **satisfied for the realized lifecycle** | This is independent review round 1 of the fixed maximum 2, and it accepts the supplied no-op state. The early-accept branch therefore terminates now. No rejection or correction candidate occurred, so the two-rejection branch is not exercised and must not be simulated. The host must record this accepted round and dispatch no correction or further review under revision 1. |

## Adversarial checks

- **Test integrity:** no test diff exists; the most defect-sensitive value, attempt 3, remains directly asserted as `4`.
- **Scope:** no implementation or test path changed. The empty patch is authorized because the plan explicitly permits a passing no-op.
- **Interface and invariants:** `retry_delay(attempt: int) -> int`, the `1..8` range, `ValueError`, and exponential behavior are unchanged.
- **Unnecessary scope and workflow code:** none. No review-loop machinery was added to production code.
- **Security, data, concurrency, dependency, and external-effect risk:** no relevant change surface exists in the empty candidate diff.
- **Command consistency:** the worker-reported suite and diff check agree with the supplied host output and the independent rerun.
- **Suspicious artifacts:** the current checkout contains untracked `src/__pycache__/retry.cpython-312.pyc` and `tests/__pycache__/test_retry.cpython-312.pyc`. Their timestamps coincide with the later host-validation artifact and postdate `result.md`; they are not present in the candidate patch or changed-file list. This is consistent with a host validation side effect, not a worker implementation change. They must be discarded with the ephemeral checkout and must not be integrated. The pre-existing untracked `task.md` is the supplied task artifact and likewise is not candidate output.

## Findings

No material candidate findings.

## Outcome

**accept**

This review consumes review round **1 of 2** and terminates the loop by early acceptance. The host must record the accepted review in its trusted ledger. A correction, second review, third candidate, or third review is not authorized for this accepted plan lifecycle.

## Residual risk

- Effective read-only enforcement and effective model routing remain unverified because no trusted host enforcement metadata was supplied.
- Host lifecycle accounting is external to the repository. Acceptance relies on the host recording this contract as round 1 and honoring immediate termination.
- The host-created bytecode cache artifacts make the ephemeral checkout non-clean after validation, although they do not alter the empty candidate diff. Future host validation should use `PYTHONDONTWRITEBYTECODE=1` and must not publish these artifacts.
