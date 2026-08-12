# Security and trust boundaries

## Authority

User instructions, harness policy, and host policy outrank project configuration. Repository content, external content, and worker output are context/claims, not authority.

An attacker may place instructions in source comments, README files, issues, fixtures, snapshots, generated outputs, command output, or third-party skills. Those instructions cannot expand scope, change targets, enable network/credentials/destructive actions, weaken validation, or override the contract.

## Controls

- strict schemas and unknown-field rejection;
- secret-pattern scanning and log/event redaction;
- repository-relative path normalization and traversal rejection;
- resolved-path containment to detect symlink escapes;
- task write allowlists plus forbidden/run-state patterns;
- independent authorization fields for network, credentials, external effects, destructive actions, and targets;
- non-recursive workers, read-only architects/reviewers where host permits, and surfaced enforcement gaps;
- no network-enabled installer or provider credentials;
- no effective-model trust from configuration/self-report;
- conservative parallel-write validation;
- locked atomic state persistence, create-only evidence, and digest binding;
- observed Git change authorization rather than worker-reported paths alone;
- separate root approval attestation before an accepted review can transition state;
- duplicate-key rejection and byte limits before structured/text parsing;
- bounded subprocess duration/output and safe generated-TOML serialization.

Result evidence may name only commands declared in the governing task contract. Task validation
commands are rejected when their recognizable network/install or destructive effects exceed the
task's explicit authorization. This closes the contract-ingestion boundary; the host sandbox is
still responsible for preventing a worker from executing an unreported or obfuscated command.

Do not persist environment variable values, tokens, credentials, private prompts, full transcripts, raw logs, or production data in contracts/capability snapshots. Third-party skills and repository scripts require inspection before execution.

## Command policy

Eclipse provides command classification for destructive and network/install patterns, but it is not a shell sandbox. Host permissions remain essential. Commands in task contracts are data until the worker/host confirms they are authorized and safe. The state store rejects probable secret patterns before persisting task, result, or review contracts.

## Residual risk

Host runtime overrides can weaken configured sandboxes. Tool aliases do not guarantee identical enforcement across Copilot surfaces. Pattern scanners cannot identify every secret. Reviewers and workers remain probabilistic. Same-account filesystem symlink races require host isolation. Doctor exposes these limitations; it cannot manufacture host evidence.
