# Context Manifest

A Context Manifest gives a worker the smallest sufficient context for one task. It may be embedded in a Task Contract or transferred separately using `schemas/context-manifest.schema.json`.

Required fields:

- `schema_version` — context contract version;
- `summary` — concise task-relevant architecture and situation;
- `references` — bounded paths/symbols, purpose, optional digest, and trust class;
- `trusted_sources` — explicit authorities or approved source descriptions.

Trust classes are `user`, `harness`, `project-config`, `repository`, and `external`. A trust label describes how content should be interpreted; it does not grant tools, credentials, network access, write scope, or authority beyond the Task Contract.

Do not include full transcripts, unrelated repository discovery, secrets, raw private logs, or discarded hypotheses.
