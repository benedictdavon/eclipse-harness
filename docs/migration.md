# Migration and interoperability

## soluna-workflow

The migrator recognizes legacy `.codex/config.toml`, `docs/ai/PROJECT_CONTEXT.md`, `plans/ACTIVE_PLAN.md`, and `plans/HANDOFF.md`.

```bash
eclipse migrate soluna-workflow /path/to/legacy --dry-run
eclipse migrate soluna-workflow /path/to/legacy --output /path/to/project
```

It maps `max_threads` conservatively to Eclipse writer concurrency and current generated Codex configuration. It does not preserve `max_depth` as a V2 recursion guarantee. It preserves project context and legacy Markdown for human review, but does not falsely claim lossless prose-to-JSON conversion. Current adapters replace legacy role files; existing sources remain untouched.

Migration is repository-bounded, rejects source symlinks that escape the selected legacy root, and refuses to overwrite any existing target. Run it into a clean destination and merge preserved prose only after human inspection.

## Other orchestrators

Eclipse's protocol can coexist with model/provider routers such as Codex-Orchestration: the external router selects/calls a verified executor, while Eclipse owns task semantics, evidence, concurrency, review, and run state. No provider configuration is duplicated in v0.1.

Broader skill routers such as Rune may load Eclipse skills alongside their own. Eclipse does not replace a host/router or inject a second instruction authority. A future adapter can translate policy metadata, but v0.1 has no dependency on either project.
