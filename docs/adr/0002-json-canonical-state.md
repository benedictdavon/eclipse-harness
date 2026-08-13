# ADR 0002: Eclipse-owned canonical run state

Status: superseded by ADR 0004 before v0.1 release

The initial implementation made `.eclipse/runs/<id>/run.json` canonical and added state transitions, locks, journals, evidence ingestion, rendered views, recovery, and git/worktree support.

PR review found that this made the optional Python package a workflow engine and contradicted the skills-first product boundary. The persistence design, schema, CLI commands, and runtime modules were removed before release. Contract digests and plan revisions remain portable protocol semantics; the host owns current workflow state.
