# Finding classification

Use one type:

- `bounded-correction`
- `architecture-escalation`
- `invalid-contract`
- `insufficient-evidence`
- `acceptance-failure`
- `security-concern`
- `unauthorized-change`

Each finding needs an ID, severity, path/symbol, relevant criterion when applicable, observed evidence, impact, exact correction, and disposition (`worker`, `architect`, or `human`).

A finding must cite an observable defect or a criterion/invariant that remains
unverified. Do not turn the absence of an undeclared tool, optional host
attestation, or impossible negative proof into a worker defect. Route a material
task-contract gap to the architect and missing trusted host evidence to the
human/host.

Bounded worker corrections preserve the Task Contract. Public API, schema,
security, authorization, write-scope, or invariant changes require architect
revision. When `max_review_rounds` is exhausted, escalate with the remaining
findings and do not request another correction cycle.

Prioritize correctness, security, data integrity, concurrency, compatibility, and missing validation. Avoid style-only findings unless they conceal a substantive risk.
