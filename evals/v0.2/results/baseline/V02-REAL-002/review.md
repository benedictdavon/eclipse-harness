# Review Contract

```json
{
  "schema_version": "1.0",
  "run_id": "V02-REAL-002",
  "plan_revision": 1,
  "plan_digest": "416ccdc548cb3890f126d66b6b814a52ee2c95e40a5d1353dc14f066038bca90",
  "task_id": "V02-REAL-002-implement-bytes-limit",
  "task_contract_digest": "sha256:ee564c0b247670f73df541287a568cdf9c9d78bb09bf741f39a0cce7983ae2a9",
  "result_digest": "sha256:869201ee1d3e3169385e3570ab98e80fcc2df622444e7c444bf7188aab0077b0",
  "review_round": 1,
  "outcome": "escalated",
  "reviewer_identity": {
    "role": "reviewer",
    "requested_model": null,
    "effective_model": null,
    "verification": "unverified"
  },
  "permissions": {
    "desired": "read-only",
    "effective": "unverified",
    "enforcement": "host-conditional"
  },
  "findings": [
    {
      "id": "RV-001",
      "severity": "medium",
      "type": "acceptance-failure",
      "path": "validation.txt",
      "symbol": null,
      "criterion_id": "AC-FOCUSED-PASS",
      "evidence": "The host-observed packet-required command `PYTHONPATH=src python -m pytest tests/test_itsdangerous/test_encoding.py -q` exited 1 with `/opt/codex/runtimes/codex-primary-runtime/dependencies/python/bin/python: No module named pytest`. Independent non-mutating discovery also found no importable pytest module in that Python environment. The worker correctly reported this failure rather than claiming a pass.",
      "impact": "The required focused encoding test module was not collected or executed, so AC-FOCUSED-PASS and the required-validation invariant are unsatisfied. The otherwise correct patch cannot be accepted without direct passing evidence, and collection or interaction failures in the focused module remain possible.",
      "correction": "The human or host must provide the pinned run with an authorized test-capable environment containing pytest, without changing the repository patch or expanding its write scope. A bounded worker must then rerun exactly `PYTHONPATH=src python -m pytest tests/test_itsdangerous/test_encoding.py -q` and return host-observed exit-zero output for review. No source, test, or documentation correction is currently indicated.",
      "disposition": "human"
    }
  ],
  "criteria_verdicts": [
    {
      "criterion_id": "AC-NINE-BYTE-ERROR",
      "status": "satisfied",
      "evidence": "The actual patch adds a pre-padding `len(bytestr) > 8` guard that explicitly raises `ValueError(\"bytestr must contain at most 8 bytes\")`. The focused test uses exactly nine bytes and compares the captured exception string exactly. An independent read-only runtime check of that input exited 0."
    },
    {
      "criterion_id": "AC-VALID-PRESERVED",
      "status": "satisfied",
      "evidence": "The actual diff leaves the original rjust-and-unpack expression byte-for-byte unchanged and only precedes it with a branch that is false for lengths 0 through 8. The existing parametrized round-trip cases remain intact, and independent read-only checks reproduced the empty-, one-, and eight-byte expected results with exit 0."
    },
    {
      "criterion_id": "AC-DOC-LIMIT",
      "status": "satisfied",
      "evidence": "The documentation diff adds exactly one occurrence of the frozen sentence: ``bytes_to_int`` accepts byte strings containing at most eight bytes. No other documentation content changed."
    },
    {
      "criterion_id": "AC-FOCUSED-PASS",
      "status": "unsatisfied",
      "evidence": "The host-observed required pytest command exited 1 before collection because pytest is unavailable; there is no exit-zero focused-suite record."
    },
    {
      "criterion_id": "AC-SCOPE",
      "status": "satisfied",
      "evidence": "Host-observed patch and changed-file evidence, reconciled with the live worktree, show only docs/encoding.rst, src/itsdangerous/encoding.py, and tests/test_itsdangerous/test_encoding.py modified; there are no staged or untracked changes. Independent `git diff --check` exited 0. The test addition is focused and does not weaken, delete, skip, or rewrite existing coverage."
    }
  ],
  "validation_summary": "The host-observed packet-required pytest command failed with exit 1 because pytest is absent, so acceptance is prohibited. Independent read-only review confirmed the exact nine-byte ValueError behavior, representative preserved valid-input round trips, exactly one required documentation sentence, the three-file scope, no staged or untracked files, and a clean `git diff --check`. The actual patch matches the live worktree content; the host patch artifact differs from default `git diff` only by one terminal blank line. No suspicious test weakening, unrelated change, unauthorized change, interface change, security concern, or unsupported completion claim was found.",
  "residual_risk": [
    "The complete focused encoding test module remains unexecuted, so pytest collection and interaction behavior are not directly verified.",
    "Effective reviewer model identity and mechanical read-only enforcement were not established by trusted host metadata."
  ],
  "started_at": "2026-08-13T03:02:00Z",
  "finished_at": "2026-08-13T03:06:18Z",
  "metadata": {
    "case_id": "V02-REAL-002",
    "base_revision": "672971d66a2ef9f85151e53283113f33d642dabd",
    "packet_digest": "sha256:d45c0331a7ba09c24a4423fd0cac14051c859db8e82a7c9b7ff553d47fde416c",
    "patch_digest": "sha256:f7b7a2f6ae3f1ac573048a9c12d0ddbcfa942a0914508d294a7ca5b02b2dbcf2",
    "changed_files_digest": "sha256:0bbf9ded7c5fad671dde4a49467cca8c9115da802e66e26b2d52e8b9879a0496",
    "host_validation_digest": "sha256:21eded5fb791b8c347428c3a8d57aef6c331b325052992a11023a98b8f2ce010",
    "review_budget": "round 1 of 1",
    "routing_reason": "Resolving the sole failure requires environment or dependency authority that the task explicitly withholds from the worker."
  }
}
```
