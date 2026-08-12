# Manual and generic adapter

Manual mode is a complete supported workflow, not a reduced runtime fallback.

1. An architect or human creates an approved plan revision, Context Manifest, Task Contracts, and execution waves.
2. Give one current task plus its referenced context to a capable worker following `eclipse-execute`.
3. The host or user supplies the repository checkout, tools, permissions, and git isolation.
4. Require one Result Contract with acceptance and validation evidence.
5. Give the original requirement, current plan, task, result, actual diff, and host-observed evidence to an independent reviewer following `eclipse-review`.
6. Route bounded corrections to a worker, architecture decisions to the architect, and new authority to a human.

The JSON Schemas and examples can be checked manually or by any JSON Schema implementation. The Python CLI is optional.

Model and permission fields remain preferences or unverified observations unless the external host supplies trustworthy runtime metadata.
