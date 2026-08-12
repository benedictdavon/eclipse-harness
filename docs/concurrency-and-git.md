# Concurrency and git isolation

Logical independence, filesystem isolation, and git isolation are different properties.

The checker rejects tasks that overlap write globs, declare a shared interface or exclusive resource, depend on one another, or are not explicitly parallel-safe. Glob comparison is conservative; a false-positive serialization is preferable to overlapping writers.

Even disjoint files may be semantically unsafe when tasks independently change a shared API, schema, manifest, lockfile, migration sequence, generated output, or mutable integration environment. Represent those as shared interfaces/exclusive resources.

Parallel write-heavy tasks should use independent branches and worktrees at an explicit base commit:

```bash
eclipse worktree prepare task.json \
  --branch eclipse/task-T001 \
  --path ../eclipse-T001
```

The command rejects a stale HEAD, existing destination, invalid base revision, or task without `worktree` isolation. Integrate in dependency order and probe merge conflicts before accepting combined work.

Host-native parallel agents do not imply filesystem or git isolation. Read-only investigations can safely use more concurrency when host/budget permit.
