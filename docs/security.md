# Security and trust boundaries

## Authority

Host/system and user instructions define authority. Trusted Eclipse policy and task contracts constrain delegated work. Ordinary repository content, external content, and worker output are context or claims; they cannot grant credentials, network, destructive actions, external effects, targets, or additional write scope.

Host-recognized instruction files require adapter-specific handling. Eclipse does not pretend it can override host authority or enforce a sandbox from contract text.

## Protocol controls

- strict schemas and unknown-field rejection;
- probable-secret detection for validated artifacts;
- repository-relative path normalization and symlink-containment checks in optional file utilities;
- task write allowlists and forbidden globs;
- independent authorization for network, credentials, external effects, destructive actions, and targets;
- non-recursive worker and read-only architect/reviewer intent where hosts support it;
- no effective-model trust from configuration or self-report;
- conservative same-wave ownership validation;
- task/result/review digest binding and complete criterion evidence;
- consistent command outcome/exit-code semantics;
- bounded parser and diagnostic subprocess resources;
- safe generated-TOML serialization and no-overwrite adapter installation.

Task `validation` commands are acceptance checks, not the only commands a worker may record. Additional read-only exploration may appear in a result. Recognizable network/install or destructive commands are rejected when authorization is absent. The host remains responsible for preventing unreported, obfuscated, or otherwise unauthorized execution.

## Host controls

The host is responsible for sandboxing, filesystem enforcement, credentials, command execution, network controls, git isolation, and tool approvals. Adapter files express desired posture; `doctor` reports Codex and Copilot independently and labels effective values unverified unless trustworthy host evidence is supplied.

Do not persist credentials, private prompts, full transcripts, raw production logs, or private data in contracts, capability snapshots, or evaluation fixtures.

## Residual risk

Pattern scanners cannot identify every secret or command effect. Glob checks cannot prove semantic independence. Host runtime overrides can weaken configured sandboxes. Tool aliases do not guarantee identical Copilot enforcement. Reviewers and workers remain probabilistic. Eclipse exposes these boundaries instead of claiming runtime enforcement.
