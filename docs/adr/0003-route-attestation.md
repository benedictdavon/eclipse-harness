# ADR 0003: Model route attestation is separate from configuration

Status: accepted for v0.1

The researched Codex behavior and general host portability boundary show that configured role/model intent may not equal the effective child model. Self-report cannot prove identity.

Eclipse stores requested, configured, effective, and verification separately. `effective_model` is accepted only with trusted host-observed metadata. A mismatch is `broken`; absent evidence is `unverified`. Strict mode fails closed, while standard/manual mode labels the workflow policy-only.

This prevents false cost claims at the expense of sometimes withholding a guarantee even when the host happened to route correctly but exposed no proof.
