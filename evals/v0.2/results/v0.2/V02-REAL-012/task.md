# Approved Task Contracts — V02-REAL-012

## V02-REAL-012-T1

```json
{
  "schema_version": "1.0",
  "run_id": "V02-REAL-012",
  "plan_revision": 1,
  "plan_digest": "sha256:e2e5790094f301baa5110d33557451ef93b0afd9265618ac3da2639e5af3392a",
  "task_id": "V02-REAL-012-T1",
  "dependencies": [],
  "objective": "Reject non-positive User.avatar sizes with ValueError('size must be positive'), test 0 and -1, and preserve the exact valid URL.",
  "rationale": "An early guard prevents invalid Gravatar size URLs without changing valid output.",
  "context_manifest": {
    "schema_version": "1.0",
    "summary": "User.avatar currently interpolates any size; UserModelCase.test_avatar asserts the exact size-128 URL.",
    "references": [
      {"path": "app/models.py", "symbol": "User.avatar", "purpose": "Add the early size guard.", "digest": null, "trust": "repository"},
      {"path": "tests.py", "symbol": "UserModelCase.test_avatar", "purpose": "Add exact error coverage while retaining valid URL coverage.", "digest": null, "trust": "repository"}
    ],
    "trusted_sources": [
      "/workspace/scratch/473866e9940e/repo/evals/v0.2/results/v0.2/V02-REAL-012/packet.json",
      "/workspace/scratch/473866e9940e/repo/evals/v0.2/results/v0.2/V02-REAL-012/host-metadata.json"
    ]
  },
  "decisions": {"fixed": ["Raise exactly ValueError('size must be positive') for size <= 0 before hashing.", "Preserve the existing URL expression for positive sizes."], "assumptions": ["Non-numeric and upper-bound behavior is out of scope; trusted clean base remains current."]},
  "invariants": ["Size 128 returns the exact existing URL.", "No model mapping or template changes in this task."],
  "non_goals": ["Changing hashing, URL parameters, schema, templates, or dependencies."],
  "scope": {
    "write_globs": ["app/models.py", "tests.py"],
    "read_globs": ["app/models.py", "tests.py"],
    "forbidden_globs": ["app/templates/**", "migrations/**", "requirements*.txt"],
    "shared_interfaces": ["User.avatar behavior"],
    "exclusive_resources": ["app/models.py:User.avatar", "tests.py:UserModelCase.test_avatar"],
    "parallel_safe": true,
    "isolation": "manual"
  },
  "required_capabilities": ["tiny Python edit", "unittest regression editing"],
  "execution_profile": {"role": "worker", "capability_tier": "tiny-deterministic-edit", "cost_tier": "lowest", "reasoning_effort": "medium", "preferred_model": null, "fallback_profiles": ["Return broader input semantics to architect."]},
  "implementation_instructions": ["Add the size <= 0 guard at the beginning of User.avatar.", "Assert 0 and -1 raise the exact ValueError; retain the size-128 assertion.", "Do not edit the 404 template owned by T2."],
  "acceptance_criteria": [
    {"id": "AC1", "statement": "Sizes 0 and -1 raise the exact required ValueError.", "evidence_required": "Source/test diff with exact message assertions."},
    {"id": "AC2", "statement": "Size 128 preserves its exact URL and modified Python files compile.", "evidence_required": "Retained URL assertion, required command exit 0, and task-local status."}
  ],
  "validation": [{"command": "python -m compileall -q app tests.py", "purpose": "Run the packet's exact frozen compile validation.", "mutating": true, "required": true}],
  "expected_evidence": ["Patch limited to app/models.py and tests.py.", "Required command/output/status; exclude bytecode from product patch.", "Evidence at host external artifact destination."],
  "stop_conditions": ["A template, migration, dependency, or other write is needed.", "Frozen command needs installation/network/credentials/expanded permission.", "T2 touches T1-owned files or trusted base/clean status differs."],
  "risk": {"level": "low", "flags": ["model method validation", "shared-checkout serialization", "compile creates bytecode"]},
  "complexity": "trivial",
  "budgets": {"max_attempts": 2, "max_review_rounds": 2},
  "authorization": {"network": false, "credentials": false, "external_side_effects": false, "destructive_actions": false, "targets": ["app/models.py", "tests.py"]},
  "provenance": {"base_revision": "a975ef64864354867c88e0ed3a17ba7d17dca752", "created_by": "eclipse-architect", "created_at": "2026-08-13T00:00:00+08:00"}
}
```

## V02-REAL-012-T2

```json
{
  "schema_version": "1.0",
  "run_id": "V02-REAL-012",
  "plan_revision": 1,
  "plan_digest": "sha256:e2e5790094f301baa5110d33557451ef93b0afd9265618ac3da2639e5af3392a",
  "task_id": "V02-REAL-012-T2",
  "dependencies": [],
  "objective": "Improve the 404 page's translatable copy while preserving structure and its home link.",
  "rationale": "A specific heading, explanation, and link label are clearer than the terse existing page.",
  "context_manifest": {
    "schema_version": "1.0",
    "summary": "The template extends base.html, defines content, shows 'Not Found', and links 'Back' to main.index.",
    "references": [{"path": "app/templates/errors/404.html", "symbol": "content block", "purpose": "Change only the three translatable strings.", "digest": null, "trust": "repository"}],
    "trusted_sources": ["/workspace/scratch/473866e9940e/repo/evals/v0.2/results/v0.2/V02-REAL-012/packet.json", "/workspace/scratch/473866e9940e/repo/evals/v0.2/results/v0.2/V02-REAL-012/host-metadata.json"]
  },
  "decisions": {"fixed": ["Use 'Page Not Found', 'The page you requested could not be found.', and 'Back to home', each within the existing translation function.", "Preserve base inheritance, content block, and main.index URL."], "assumptions": ["No translation catalog update is required by this packet; trusted clean base remains current."]},
  "invariants": ["404 rendering retains the base layout and home destination.", "No Python files change in this task."],
  "non_goals": ["Changing error handlers, status codes, styling, other templates, or translation catalogs."],
  "scope": {"write_globs": ["app/templates/errors/404.html"], "read_globs": ["app/templates/errors/404.html"], "forbidden_globs": ["app/**/*.py", "tests.py", "migrations/**", "app/translations/**"], "shared_interfaces": [], "exclusive_resources": ["app/templates/errors/404.html"], "parallel_safe": true, "isolation": "manual"},
  "required_capabilities": ["tiny deterministic Jinja edit"],
  "execution_profile": {"role": "worker", "capability_tier": "tiny-deterministic-edit", "cost_tier": "lowest", "reasoning_effort": "medium", "preferred_model": null, "fallback_profiles": ["Return broader copy/localization changes to architect."]},
  "implementation_instructions": ["Change exactly the heading, add the fixed explanatory paragraph, and change the existing home-link label.", "Keep each user-facing string wrapped in _().", "Do not edit T1's Python files."],
  "acceptance_criteria": [
    {"id": "AC1", "statement": "The 404 page contains the fixed clear translatable copy and retains main.index.", "evidence_required": "Task-local template diff."},
    {"id": "AC2", "statement": "The frozen compile validation passes and only the 404 template changes.", "evidence_required": "Required command exit 0 and task-local diff/status."}
  ],
  "validation": [{"command": "python -m compileall -q app tests.py", "purpose": "Run the packet's exact frozen integration compile validation; it is the only required command.", "mutating": true, "required": true}],
  "expected_evidence": ["Patch limited to app/templates/errors/404.html.", "Required command/output/status; exclude bytecode from product patch.", "Evidence at host external artifact destination."],
  "stop_conditions": ["A Python, translation-catalog, second-template, dependency, or other write is needed.", "Frozen command needs installation/network/credentials/expanded permission.", "T1 touches T2-owned file or trusted base/clean status differs."],
  "risk": {"level": "low", "flags": ["user-visible copy", "shared-checkout serialization", "compile creates bytecode"]},
  "complexity": "trivial",
  "budgets": {"max_attempts": 2, "max_review_rounds": 2},
  "authorization": {"network": false, "credentials": false, "external_side_effects": false, "destructive_actions": false, "targets": ["app/templates/errors/404.html"]},
  "provenance": {"base_revision": "a975ef64864354867c88e0ed3a17ba7d17dca752", "created_by": "eclipse-architect", "created_at": "2026-08-13T00:00:00+08:00"}
}
```
