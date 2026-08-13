# Dependency waves and host-owned git isolation

Eclipse separates three questions:

1. Is the dependency graph valid and acyclic?
2. Which tasks are ready in the same execution wave?
3. Are tasks within that wave safe to run concurrently?

A dependency edge is ordering, not a concurrency defect. `T002 depends on T001` produces two waves. Independent siblings may share a wave; downstream tasks wait until every dependency is complete.

Within a candidate wave, the optional checker conservatively rejects overlapping write globs, shared interfaces, exclusive resources, tasks not marked parallel-safe, or write tasks that request read-only isolation. Different files alone do not establish semantic independence: APIs, schemas, manifests, lockfiles, migrations, generated outputs, and shared test environments must be declared.

```bash
eclipse check-concurrency T001.json T002.json T003.json --max-writers 2
```

This command calculates guidance only. The host owns task scheduling, branches, worktrees, filesystem isolation, merges, and conflict resolution. A host's native parallel-agent feature does not by itself prove write or git isolation.
