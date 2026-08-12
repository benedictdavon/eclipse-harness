# Known limitations

- Eclipse v0.1 is guidance, contracts, adapters, evals, and optional validators—not an agent or workflow runtime.
- The host or user must store the current plan revision and workflow status.
- Effective model, reasoning, permission, and sandbox attestation depends on trustworthy host metadata; configuration and self-report remain unverified.
- Codex and Copilot surfaces may differ or apply runtime overrides.
- Copilot profiles inherit host model selection and do not claim Sol/Luna parity.
- Glob overlap detection is conservative and cannot prove arbitrary semantic independence.
- Command recognition cannot prove the effects of scripts, interpreters, encoded commands, or unreported commands.
- Secret scanning is pattern based and cannot replace host secret isolation.
- JSON Schema covers structural interoperability; Python validators add cross-contract and command semantics.
- The optional doctor inspects requested configuration but cannot manufacture effective-runtime evidence.
- No canonical run database, lock manager, event journal, recovery engine, worktree manager, migration runtime, autonomous provider execution, billing probe, GUI, or marketplace is included.
- Evaluation infrastructure ships recorded fixtures and methodology, not live benchmark conclusions or savings claims.
