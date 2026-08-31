# Review Contract — V02-REAL-006

```json
{
  "schema_version": "1.0",
  "run_id": "V02-REAL-006",
  "plan_revision": 1,
  "plan_digest": "sha256:9ad88fd343a14118432e21b09a2364a152913c6f292f43adf647c99d3fc79d5b",
  "task_id": "V02-REAL-006-T01",
  "task_contract_digest": "sha256:b68ec385e2976f8aa71845b0be0be55122de0e33a29fb460faf3d55a1f693406",
  "result_digest": "sha256:856a68eeeacb7fbcc1fdccc583fba00d2b2c71ca835d8ded67476c83269c03d0",
  "review_round": 1,
  "reviewer_identity": {
    "role": "reviewer",
    "requested_model": null,
    "effective_model": null,
    "verification": "unverified"
  },
  "permissions": {
    "desired": "read-only",
    "effective": "unverified",
    "enforcement": "The workspace sandbox was not proven to mechanically enforce repository read-only access. Inspection and validation were read-only; the only intentional write was this required review.md output."
  },
  "criteria_verdicts": [
    {
      "criterion_id": "PACKET-AC1",
      "status": "satisfied",
      "evidence": "The contracts have exact, disjoint write ownership: T01 owns only tests/test_itsdangerous/test_encoding.py and T02 owns only docs/encoding.rst. Both shared_interfaces and exclusive_resources are empty. Independent Eclipse inspection validated task digests sha256:b68ec385e2976f8aa71845b0be0be55122de0e33a29fb460faf3d55a1f693406 and sha256:00f454d0f63f0951cf00080e689970d16ea9c64db08ee4a65f3fce9ed4908310, and the deterministic concurrency checker returned the ownership-safe wave [[T01, T02]]."
    },
    {
      "criterion_id": "PACKET-AC2",
      "status": "satisfied",
      "evidence": "The architect explicitly permits same-wave execution only in separate isolated worktrees and otherwise requires serialization in T01-then-T02 order. Both task results and result.md record actual_concurrency=false, so the host conservatively serialized when isolation was not allocated. No evidence of concurrent writers was found."
    },
    {
      "criterion_id": "PACKET-AC3",
      "status": "unsatisfied",
      "evidence": "The two tracked edits are correct on direct diff and source inspection, but the packet-mandated focused pytest command exited 1 before collection because pytest was unavailable. Required dynamic evidence for the new test case is absent."
    },
    {
      "criterion_id": "T01-AC1",
      "status": "satisfied",
      "evidence": "The actual diff adds exactly (256, b\"\\x01\\x00\") to test_int_bytes. The 0, 192, and 18446744073709551615 cases remain unchanged. The extra line wrapping does not alter test semantics."
    },
    {
      "criterion_id": "T01-AC2",
      "status": "unsatisfied",
      "evidence": "Both existing assertions remain intact and apply to the new tuple, but PYTHONPATH=src python -m pytest tests/test_itsdangerous/test_encoding.py -q exited 1 before collection with 'No module named pytest'. The worker correctly reported not-tested and blocked rather than claiming completion."
    },
    {
      "criterion_id": "T01-AC3",
      "status": "satisfied",
      "evidence": "The T01 tracked diff changes only tests/test_itsdangerous/test_encoding.py, with no runtime, documentation, dependency, configuration, or other test content. The separate out-of-scope checkout result artifact is an authorization/invariant failure recorded as V02-REAL-006-R003."
    },
    {
      "criterion_id": "T02-AC1",
      "status": "satisfied",
      "evidence": "The paragraph accurately identifies the RFC 4648 URL-safe 64-character alphabet as ASCII letters and digits with '-' and '_' replacing '+' and '/'."
    },
    {
      "criterion_id": "T02-AC2",
      "status": "satisfied",
      "evidence": "The paragraph correctly distinguishes '=' padding, says base64_encode omits trailing padding, and says base64_decode restores needed padding. This matches the unchanged rstrip(b'=') and b'=' * (-len(string) % 4) implementation and makes no unsupported strict-rejection claim."
    },
    {
      "criterion_id": "T02-AC3",
      "status": "unsatisfied",
      "evidence": "The page structure and autofunction directives are preserved and git diff --check passed, but T02's required repository-wide git diff --name-only output listed docs/encoding.rst and the pre-existing T01 test path rather than only docs/encoding.rst as the criterion expressly requires. The pre-edit status narrative is useful but does not satisfy the exact contracted evidence predicate."
    }
  ],
  "validation_summary": "Artifact binding: packet bytes independently hash to sha256:5109ffc4a1c59980e30fc27a2ecf1613ad5fa5320a623d97e555251690c99952; both task metadata plan inputs recompute to the declared plan digest; canonical T01 and T02 result digests independently recompute to sha256:856a68eeeacb7fbcc1fdccc583fba00d2b2c71ca835d8ded67476c83269c03d0 and sha256:f59858652fc939f6fa27745f6c64ed9b340bcdb91cdf9e0777664fedf4f05d80; result.md bytes hash to sha256:21b2d96d9cd199c7b20b988681ff640fee2cc4cf57cd500d6ca8b26c363134b8. HEAD is the pinned 672971d66a2ef9f85151e53283113f33d642dabd. patch.diff bytes hash to sha256:06c0623a3efb36cfbca24a6250ce20e85dc899f6cad834c58800981cd29fc447 and the actual tracked diff bytes hash to sha256:686c3122ee89d966d7019ae06c72aabc7a8b35286f744b7afc5f5437978736b4; they contain the same two hunks, with patch.diff containing one extra terminal blank line. git diff --check for both owned paths passes. The tracked path list is exactly docs/encoding.rst and tests/test_itsdangerous/test_encoding.py, while git status and changed-files.txt additionally expose ?? result-task1.md. Reviewer rerun of the exact focused pytest command failed with exit 1 because the selected Python cannot import pytest. Static source review confirms 256 encodes to minimal big-endian b'\\x01\\x00'; it also confirms the documentation's alphabet and padding statements. Runtime/source/API/dependency/configuration/lockfile invariants and the stated non-goals are preserved in the tracked patch. The unrelated/generated-file authorization invariant is violated by the untracked result artifact. Effective model identity, worker independence, worktree isolation, reviewer mechanical read-only enforcement, and cost remain unverified where trusted host evidence is absent.",
  "findings": [
    {
      "id": "V02-REAL-006-R001",
      "severity": "medium",
      "type": "insufficient-evidence",
      "path": "tests/test_itsdangerous/test_encoding.py::test_int_bytes (PACKET-AC3, T01-AC2)",
      "evidence": "The worker, integration record, and reviewer rerun all show the mandatory focused pytest command exited 1 before collection because the selected Python environment has no pytest module.",
      "impact": "The new tuple is plausible and statically correct, but acceptance expressly requires a passing focused test run. T01 and the combined case cannot be accepted without it.",
      "correction": "The host environment owner must provide the task-configured Python environment with pytest available, then rerun exactly 'PYTHONPATH=src python -m pytest tests/test_itsdangerous/test_encoding.py -q' from the pinned combined checkout and attach exit-0 output. Do not authorize the worker to install dependencies or silently substitute an unapproved environment.",
      "disposition": "human"
    },
    {
      "id": "V02-REAL-006-R002",
      "severity": "medium",
      "type": "insufficient-evidence",
      "path": "result-task2.md::criteria_evidence[T02-AC3]",
      "evidence": "T02's required repository-wide git diff --name-only command listed both docs/encoding.rst and tests/test_itsdangerous/test_encoding.py, while T02-AC3 requires output listing only docs/encoding.rst. The result nevertheless marks T02-AC3 satisfied and the task complete. A pre-edit status snapshot shows the test path was already dirty, but there is no trusted pre/post digest or isolated execution result proving the complete T02 task-local write boundary.",
      "impact": "The T02 completion claim contradicts its required evidence. Shared-checkout serialization is concurrency-safe here, but it does not meet the unchanged task contract's exact path-proof requirement.",
      "correction": "Have the host rerun T02 in a clean checkout/worktree at the pinned base so its required repository-wide path check can list only docs/encoding.rst, then issue a fresh result bound to that execution. If shared dirty-checkout execution must remain supported, the architect must issue a new plan revision and contract with explicit host-trusted pre/post path or digest evidence before re-execution; do not retroactively weaken T02-AC3.",
      "disposition": "architect"
    },
    {
      "id": "V02-REAL-006-R003",
      "severity": "medium",
      "type": "unauthorized-change",
      "path": "result-task1.md in the implementation checkout",
      "evidence": "The supplied changed-files.txt and independent git status --short both report '?? result-task1.md'. This is outside the packet's two expected write paths and both contracts' authorization targets, and ordinary git diff omitted it because it is untracked. The checkout copy differs from the collected result only by one terminal blank line, confirming it is a run artifact rather than implementation content.",
      "impact": "The final working tree is not authorization-compliant, and patch.diff understates the complete checkout mutation set. This prevents acceptance despite the two correct tracked hunks.",
      "correction": "The host must relocate or remove the untracked result artifact from the implementation checkout using its result-collection authority, retain the canonical result in the results directory, and regenerate changed-files/status evidence showing only docs/encoding.rst and tests/test_itsdangerous/test_encoding.py. No worker authority expansion is warranted.",
      "disposition": "human"
    }
  ],
  "outcome": "changes_requested",
  "residual_risk": [
    "The 256 case has not executed under pytest, so collection, parametrization, and repository-environment compatibility remain unproven.",
    "T02 task-local write provenance is not mechanically demonstrated in the serialized shared checkout.",
    "Reviewer read-only permissions and effective model identity are not verified by trusted host metadata."
  ],
  "started_at": "2026-08-13T03:45:00Z",
  "finished_at": "2026-08-13T03:57:13Z"
}
```

## Review round 2 — final

```json
{
  "schema_version": "1.0",
  "run_id": "V02-REAL-006",
  "plan_revision": 1,
  "plan_digest": "sha256:9ad88fd343a14118432e21b09a2364a152913c6f292f43adf647c99d3fc79d5b",
  "task_id": "V02-REAL-006-T01",
  "task_contract_digest": "sha256:b68ec385e2976f8aa71845b0be0be55122de0e33a29fb460faf3d55a1f693406",
  "result_digest": "sha256:856a68eeeacb7fbcc1fdccc583fba00d2b2c71ca835d8ded67476c83269c03d0",
  "review_round": 2,
  "reviewer_identity": {
    "role": "reviewer",
    "requested_model": null,
    "effective_model": null,
    "verification": "unverified"
  },
  "permissions": {
    "desired": "read-only",
    "effective": "unverified",
    "enforcement": "Mechanical repository read-only enforcement remains unverified. Round-2 inspection used read-only commands and wrote only this required appended review contract."
  },
  "criteria_verdicts": [
    {
      "criterion_id": "PACKET-AC1",
      "status": "satisfied",
      "evidence": "The validated contracts retain exact disjoint ownership of the test and documentation files. Current git status now shows only those two authorized tracked paths; the misplaced untracked result artifact has been removed from the implementation checkout."
    },
    {
      "criterion_id": "PACKET-AC2",
      "status": "satisfied",
      "evidence": "The conditional isolated-worktree concurrency decision remains sound, and actual execution remained conservatively serialized with actual_concurrency=false."
    },
    {
      "criterion_id": "PACKET-AC3",
      "status": "unsatisfied",
      "evidence": "The tracked test and documentation edits remain statically correct, but the required focused pytest command still exits 1 before collection because pytest is unavailable."
    },
    {
      "criterion_id": "T01-AC1",
      "status": "satisfied",
      "evidence": "The patch still adds exactly the 256 to b'\\x01\\x00' boundary tuple while preserving the three existing cases."
    },
    {
      "criterion_id": "T01-AC2",
      "status": "unsatisfied",
      "evidence": "Both assertions remain intact, but the exact required pytest command was rerun in round 2 and again failed before collection with 'No module named pytest'."
    },
    {
      "criterion_id": "T01-AC3",
      "status": "satisfied",
      "evidence": "Current git status and git diff --name-only show only docs/encoding.rst and tests/test_itsdangerous/test_encoding.py in the combined checkout. The previously unauthorized checkout copy of result-task1.md is absent; the canonical result-directory copy remains intact."
    },
    {
      "criterion_id": "T02-AC1",
      "status": "satisfied",
      "evidence": "The URL-safe alphabet explanation remains accurate and unchanged."
    },
    {
      "criterion_id": "T02-AC2",
      "status": "satisfied",
      "evidence": "The alphabet-versus-padding distinction and encoder/decoder padding statements remain accurate against unchanged source."
    },
    {
      "criterion_id": "T02-AC3",
      "status": "unsatisfied",
      "evidence": "No new isolated T02 execution was supplied. Its recorded task-local git diff --name-only evidence still lists both owned paths rather than only docs/encoding.rst, so its complete status remains unsupported by the exact contract predicate."
    }
  ],
  "validation_summary": "Round 1 review contract remains valid at sha256:94761676036e08829e326a122ccdae1006cd78dbb8f85c08607bdf56a9de25c6. T01 and T02 canonical result digests remain unchanged at sha256:856a68eeeacb7fbcc1fdccc583fba00d2b2c71ca835d8ded67476c83269c03d0 and sha256:f59858652fc939f6fa27745f6c64ed9b340bcdb91cdf9e0777664fedf4f05d80. HEAD remains pinned at 672971d66a2ef9f85151e53283113f33d642dabd. Current git status reports only modified docs/encoding.rst and tests/test_itsdangerous/test_encoding.py; git diff --name-only lists exactly those paths; test ! -e result-task1.md passes in the implementation checkout; the canonical results-directory result-task1.md remains present with byte hash sha256:517c25fe1fd81a8c7b09371a346e656838cfe1a70cc4761c6bad0f0110728f94. Thus round-1 finding V02-REAL-006-R003 is resolved. git diff --check still passes. The exact focused pytest command still exits 1 because pytest cannot be imported. No isolated T02 execution or replacement result was provided, so V02-REAL-006-R001 and V02-REAL-006-R002 remain material. The historical changed-files.txt records the pre-correction state; this round's direct live status verifies the bounded cleanup. This is review round 2 of 2 and exhausts the frozen review budget.",
  "findings": [
    {
      "id": "V02-REAL-006-R001",
      "severity": "medium",
      "type": "insufficient-evidence",
      "path": "tests/test_itsdangerous/test_encoding.py::test_int_bytes (PACKET-AC3, T01-AC2)",
      "evidence": "Round-2 rerun of PYTHONPATH=src python -m pytest tests/test_itsdangerous/test_encoding.py -q again exited 1 before collection because the selected Python environment has no pytest module.",
      "impact": "The test change cannot receive the required dynamic acceptance evidence, so T01 and the combined case remain unaccepted.",
      "correction": "The human host environment owner must provide the task-configured Python environment with pytest available and capture an exit-0 run of the exact required command from the pinned combined checkout. This requires a new host-authorized execution after the exhausted review budget; do not install or substitute dependencies under worker authority.",
      "disposition": "human"
    },
    {
      "id": "V02-REAL-006-R002",
      "severity": "medium",
      "type": "architecture-escalation",
      "path": "result-task2.md::criteria_evidence[T02-AC3]",
      "evidence": "T02 still has no isolated task execution. Its recorded required path check lists docs/encoding.rst and tests/test_itsdangerous/test_encoding.py while T02-AC3 requires only docs/encoding.rst, yet the result claims complete.",
      "impact": "T02's write-boundary evidence remains contractually insufficient even though the final combined tracked patch is correct and in scope.",
      "correction": "The architect must route a fresh T02 execution from a clean pinned checkout/worktree, or issue a new plan revision with an explicit host-trusted pre/post evidence design before re-execution. A fresh result and a new review authorization are required because the two-round budget is exhausted.",
      "disposition": "architect"
    }
  ],
  "outcome": "escalated",
  "residual_risk": [
    "The 256 case has still not executed under pytest.",
    "T02 task-local write provenance remains unproven by its exact required evidence.",
    "No further review round remains under the frozen two-round budget."
  ],
  "started_at": "2026-08-13T03:57:20Z",
  "finished_at": "2026-08-13T03:58:45Z"
}
```
