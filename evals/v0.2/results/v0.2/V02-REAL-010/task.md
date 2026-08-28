```json
{
  "schema_version": "1.0",
  "run_id": "V02-REAL-010",
  "plan_revision": 1,
  "plan_digest": "sha256:ecbaf3b1e425f571ccb9915297582a25052724d1ad70c37a28aa21ba4c574390",
  "task_id": "V02-REAL-010-T1",
  "dependencies": [],
  "objective": "Refactor User.followers_count, following_count, and posts_count through one private helper while preserving their exact scoped subquery count semantics, public names, and results.",
  "rationale": "All three methods duplicate the same count-over-subquery construction and differ only in the relationship-scoped Select passed to it.",
  "context_manifest": {
    "schema_version": "1.0",
    "summary": "Each count method currently builds sa.select(sa.func.count()).select_from(self.<relationship>.select().subquery()) and returns db.session.scalar(query). Existing tests directly cover follower/following counts; existing post fixtures can provide direct posts_count coverage.",
    "references": [
      {
        "path": "app/models.py",
        "symbol": "User.followers_count, User.following_count, User.posts_count",
        "purpose": "Extract only duplicated count construction and preserve each relationship-scoped Select.",
        "digest": null,
        "trust": "repository"
      },
      {
        "path": "tests.py",
        "symbol": "UserModelCase.test_follow and test_follow_posts",
        "purpose": "Retain relationship-count coverage and add a direct post-count assertion.",
        "digest": null,
        "trust": "repository"
      }
    ],
    "trusted_sources": [
      "/workspace/scratch/473866e9940e/repo/evals/v0.2/results/v0.2/V02-REAL-010/packet.json",
      "/workspace/scratch/473866e9940e/repo/evals/v0.2/results/v0.2/V02-REAL-010/host-metadata.json"
    ]
  },
  "decisions": {
    "fixed": [
      "The private User helper accepts an already-scoped Select and performs exactly sa.select(sa.func.count()).select_from(source_select.subquery()) followed by db.session.scalar.",
      "Each public method passes its existing self.followers.select(), self.following.select(), or self.posts.select() expression.",
      "Keep public method names, call signatures, scalar return behavior, and SQL scoping unchanged."
    ],
    "assumptions": [
      "A private instance method is the smallest local extraction and is not part of the public API.",
      "The trusted clean base remains current at task start."
    ]
  },
  "invariants": [
    "Counts remain restricted to the current User's write-only relationship select.",
    "The count still runs against a subquery and returns db.session.scalar's result.",
    "Follower/following transitions preserve 0-to-1-to-0 results, and each existing authored post is counted once.",
    "No relationship or schema metadata changes."
  ],
  "non_goals": [
    "Replacing counts with loaded collections, joins, cached columns, or hybrid properties.",
    "Changing query performance beyond mechanical construction reuse.",
    "Changing migrations, schema, public methods, endpoints, or dependencies."
  ],
  "scope": {
    "write_globs": [
      "app/models.py",
      "tests.py"
    ],
    "read_globs": [
      "app/models.py",
      "tests.py"
    ],
    "forbidden_globs": [
      "migrations/**",
      "app/api/**",
      "app/templates/**",
      "config.py",
      "requirements*.txt"
    ],
    "shared_interfaces": [
      "User followers_count/following_count/posts_count behavior"
    ],
    "exclusive_resources": [
      "app/models.py:User count methods and private helper",
      "tests.py:user relationship count coverage"
    ],
    "parallel_safe": false,
    "isolation": "manual"
  },
  "required_capabilities": [
    "SQLAlchemy Select/subquery reasoning",
    "behavior-preserving Python refactoring",
    "unittest regression editing",
    "Python compile validation"
  ],
  "execution_profile": {
    "role": "worker",
    "capability_tier": "bounded-local-implementation",
    "cost_tier": "low",
    "reasoning_effort": "high",
    "preferred_model": null,
    "fallback_profiles": [
      "Return any query-shape or schema change to the architect."
    ]
  },
  "implementation_instructions": [
    "Define one clearly named private User method that accepts a relationship-scoped Select, builds the same count-over-subquery query, and returns db.session.scalar.",
    "Replace only the duplicated bodies of followers_count, following_count, and posts_count with calls that pass their respective existing relationship .select().",
    "Retain existing follower/following count assertions and add a direct posts_count assertion in the existing focused post fixture test.",
    "Do not change model mappings, relationships, query filters, public signatures, migrations, or dependencies."
  ],
  "acceptance_criteria": [
    {
      "id": "AC1",
      "statement": "One private helper owns the duplicated count-over-subquery construction and all three public count methods delegate to it.",
      "evidence_required": "Task-local model diff showing a single helper and the three narrow delegates."
    },
    {
      "id": "AC2",
      "statement": "Follower, following, and post counts preserve their existing per-user results and public method names.",
      "evidence_required": "Retained follower/following assertions, new direct posts_count assertion, and diff review showing each original relationship Select retained."
    },
    {
      "id": "AC3",
      "statement": "No migration, schema, relationship, or query-broadening change occurs.",
      "evidence_required": "Task-local final diff/status limited to app/models.py and tests.py and source review of the helper input."
    },
    {
      "id": "AC4",
      "statement": "Modified Python files compile.",
      "evidence_required": "Required frozen command exit status 0 and concise output."
    }
  ],
  "validation": [
    {
      "command": "python -m compileall -q app tests.py",
      "purpose": "Run the packet's exact frozen Python compilation validation.",
      "mutating": true,
      "required": true
    }
  ],
  "expected_evidence": [
    "Task-local patch limited to app/models.py and tests.py.",
    "Required command, exit status, and concise output.",
    "Source diff demonstrating identical scoped Select inputs and one shared query construction.",
    "Final status excluding compile-created __pycache__ and .pyc files from product changes.",
    "Result evidence at the host-provided external artifact destination."
  ],
  "stop_conditions": [
    "The refactor would broaden a query, load collections, change return values, change public names, or alter schema/relationships.",
    "A migration, endpoint, template, dependency, or other out-of-scope write becomes necessary.",
    "The frozen compile command cannot run without installation, network, credentials, or expanded permission.",
    "The trusted base revision or clean status no longer matches."
  ],
  "risk": {
    "level": "low",
    "flags": [
      "SQL query shape preservation",
      "private model helper",
      "validation creates bytecode"
    ]
  },
  "complexity": "bounded",
  "budgets": {
    "max_attempts": 2,
    "max_review_rounds": 2
  },
  "authorization": {
    "network": false,
    "credentials": false,
    "external_side_effects": false,
    "destructive_actions": false,
    "targets": [
      "app/models.py",
      "tests.py"
    ]
  },
  "provenance": {
    "base_revision": "a975ef64864354867c88e0ed3a17ba7d17dca752",
    "created_by": "eclipse-architect",
    "created_at": "2026-08-13T00:00:00+08:00"
  }
}
```
