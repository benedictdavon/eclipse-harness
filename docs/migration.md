# Compatibility and manual migration

Eclipse v0.1 does not include a workflow-state migrator.

For an existing `soluna-workflow` setup:

1. preserve the original files;
2. install Eclipse skills and select a host adapter;
3. copy reusable project invariants into a Context Manifest;
4. convert only active work into current Task Contracts;
5. treat older Markdown plans and handoffs as human context, not canonical machine state;
6. verify generated adapter files before replacing any older generated profile.

Legacy `max_threads` and `max_depth` do not map automatically. Use current host capabilities and document any manual fallback. Contract-format changes should ship a documented field mapping and examples rather than a general migration runtime.

External routers may select or invoke workers while Eclipse supplies task, evidence, and review semantics. They remain responsible for provider configuration, execution, and workflow state.
