# Installation

The portable source of truth is `.agents/skills`. Copy each complete skill directory, including its `references/`, into a host-supported skill location.

For Codex, repository skills live under `.agents/skills`; project agent wrappers may live under `.codex/agents`. For Copilot, use the same skills plus `.github/agents` wrappers where supported. In manual mode, give each role its skill and the relevant contracts directly.

The optional `eclipse init` command copies packaged skills without overwriting existing directories. Adapter generation is separately opt-in and refuses to overwrite files without its generated marker.

No `.eclipse` configuration, run database, daemon, scheduler, or migration step is required.
