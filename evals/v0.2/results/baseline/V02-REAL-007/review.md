# Review Contract — V02-REAL-007

## Contract identity

- `schema_version`: `1.0`
- `run_id`: `V02-REAL-007-baseline`
- `plan_revision`: `1`
- `plan_digest`: `540f490db6d73ed72db7cf53d56367ef0c06e2b9b6bbf983cb053c6beff22afd`
- `task_id`: `V02-REAL-007-T1`
- `task_contract_digest`: `sha256:01e403eb8a70a01217e7944e018fe46163caf149f48f2531ec6489a48a535ce2`
- `result_digest`: `sha256:50fbd4559456e986288d5ae175dbe5f9295c2c2efe9869c2d5886e14ebd0052e`
- `review_round`: `1`
- `outcome`: `escalated`
- `started_at`: `2026-08-13T04:01:10Z`
- `finished_at`: `2026-08-13T04:02:19Z`

The packet digest is `sha256:0ed70749b8f8b4c9dab5d151ee8a81cbb157ce56359750301fb08ffea4ed95c3`, matching the task provenance. Recomputing the frozen canonical plan manifest produced the declared plan digest. The checkout remains at the pinned commit `a975ef64864354867c88e0ed3a17ba7d17dca752` and base tree `2c6e850f2babd3e23d75154a6b0c64cd5d19aa20`. The reviewed patch artifact and actual working-tree diff contain the same hunks; the artifact has only one additional trailing blank line.

## Reviewer identity and permissions

- `role`: `eclipse-reviewer`
- `requested_model`: `null`
- `effective_model`: `null`
- `verification`: `unverified`
- `permissions.desired`: `read-only`
- `permissions.effective`: `unverified`
- `permissions.enforcement`: The host did not provide mechanical read-only attestation. The review was conducted without source edits; only this required review artifact was written outside the reviewed checkout.

## Decision

The patch is narrowly scoped and its source logic is consistent with the requirement, but it cannot be accepted under the approved task contract. AC-01 and AC-02 expressly require a passing focused unittest. That command never imports the test module in the provided environment because Flask is absent, so neither the new rejection behavior nor the preserved valid-size behavior has direct runtime evidence. Installing dependencies is outside the worker's authorization. The result is therefore escalated to the human/host to provide an appropriately provisioned validation environment; no source correction is requested from the worker on the present evidence.

## Criterion verdicts

| Criterion | Status | Evidence |
|---|---|---|
| `AC-01` | `unverified` | `User.avatar` contains a direct `size <= 0` guard raising exactly `ValueError('size must be positive')`. `tests.py` adds anchored exact-message coverage for both `0` and `-1` using subtests. However, the required `python -m unittest tests.UserModelCase.test_avatar` exits 1 during module import with `ModuleNotFoundError: No module named 'flask'`; no assertion executes. The contract's required passing runtime evidence is absent. |
| `AC-02` | `unverified` | The production digest/URL lines and the pre-existing exact size-128 URL assertion are byte-for-byte unchanged from the base revision. All repository call sites pass positive sizes. Nevertheless, the same required focused unittest does not execute, so the contract's required passing runtime evidence is absent. |
| `AC-03` | `satisfied` | Host validation records `python -m compileall -q app tests.py` with exit status 0 and no output. Independent read-only in-memory compilation of `app/models.py` and `tests.py` also succeeded. |
| `AC-04` | `satisfied` | Actual `git status --porcelain=v1 --untracked-files=all` lists only `app/models.py` and `tests.py`. The actual diff is 7 insertions: two lines inside `User.avatar` and five lines inside `UserModelCase.test_avatar`. No template, mapped column, relationship, table, migration, dependency, configuration, call-site, or public-signature change exists. |

## Findings

### REV-001 — Required behavioral validation cannot execute

- `severity`: `medium`
- `type`: `insufficient-evidence`
- `path`: `tests.py`
- `symbol`: `tests.UserModelCase.test_avatar`
- `criteria`: `AC-01`, `AC-02`
- `evidence`: The worker reports exit status 1 for `python -m unittest tests.UserModelCase.test_avatar`, failing while importing `app/__init__.py` with `ModuleNotFoundError: No module named 'flask'`. Independent reproduction with `PYTHONDONTWRITEBYTECODE=1` produced the same exit status and traceback before any test ran. The host validation artifact records only the successful compile command.
- `impact`: The main changed behavior and valid-size regression path have not been executed. Because both criteria explicitly require a passing focused unittest, accepting would violate the task evidence requirements and Eclipse acceptance mechanics even though static inspection strongly supports the implementation.
- `correction`: The human/host must provide an isolated environment with the repository's declared dependencies already installed, or explicitly authorize dependency provisioning, then run the exact command `python -m unittest tests.UserModelCase.test_avatar`. Supply exit status 0 and concise output and re-review the unchanged task/result and patch digests. If the test then fails functionally, issue a new bounded worker correction; do not ask the current worker to install dependencies under this contract.
- `disposition`: `human`

## Validation summary

- `python -m unittest tests.UserModelCase.test_avatar`: worker-reported exit 1; reviewer independently reproduced exit 1. Import failed on missing Flask before `UserModelCase.test_avatar` executed. This required validation is blocked, not passed.
- `python -m compileall -q app tests.py`: host-recorded exit 0 with no output. This satisfies AC-03.
- `git diff --check`: independently exit 0 with no output.
- `git status --short`: independently shows only ` M app/models.py` and ` M tests.py`, matching `changed-files.txt` and the actual diff.
- Static/adversarial inspection: the guard precedes hashing and URL construction; valid-size implementation lines are unchanged; the test change is additive and does not weaken or remove the existing exact URL assertion; relevant production/template call sites use sizes 128, 256, 70, and 64.
- Worker claims are appropriately qualified: the worker explicitly reports the unittest blocker and does not claim AC-01 or AC-02 runtime success. Its compile, changed-file, no-out-of-scope-change, and blocker claims are supported by host artifacts or independent review.

## Invariants, scope, and non-goals

- Valid-size email normalization, MD5 digest construction, Gravatar host, query parameters, and URL formatting are unchanged.
- No SQLAlchemy declaration or database behavior was edited.
- No template, migration, dependency, configuration, call-site, or generated source artifact was edited.
- Behavior for unsupported non-numeric, boolean, and fractional categories was not redesigned; the task explicitly makes those categories non-goals.
- No suspicious test removal, assertion weakening, unrelated refactor, network access, credential use, external effect, or destructive action is present in the patch.

## Residual risk

- The patch appears correct by exact diff and static inspection, but confidence remains below acceptance because the application dependency graph and focused assertions have not executed.
- Validation remains dependent on host-provided project dependencies. Provisioning them is outside the current worker authorization and must not be inferred from the source-only success.
- No additional architecture, security, data-integrity, compatibility, or scope risk was identified in the reviewed change.
