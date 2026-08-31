# Skills Design Standard

The operational behavior belongs in concise `SKILL.md` files; supporting detail belongs in one-level `references/`. Core wording must express vendor-neutral role semantics and let adapters explain host-specific mechanisms.

- Orchestrate resolves ambiguity, freezes decisions and invariants, defines scope and acceptance, chooses routing, and authorizes only safe concurrency.
- Execute performs bounded implementation and validation, produces evidence, and stops when architecture or authority must change.
- Review independently checks the requirement, task, actual diff, evidence, scope, and invariants, then distinguishes bounded correction from architect or human escalation.
- Bootstrap selects the adapter, installs or copies the bundle, explains degraded/manual behavior, and validates structure.

Sol/Luna remains a reference policy. Provider or model changes must not require rewriting the core roles.
