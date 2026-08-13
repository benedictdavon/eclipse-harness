# Routing Policy

Routing is intent expressed in vendor-neutral terms: role, capability tier, risk, complexity, cost tier, reasoning effort, tools, permissions, platform availability, and fallback behavior.

The Sol/Luna reference policy uses strong reasoning for architecture and independent review, economical workers for bounded implementation, and a higher worker-effort step for difficult but still local work. Architecture, scope, interface, migration-design, concurrency-design, and security-design decisions return to the architect. New authority and destructive effects return to a human.

Model identifiers belong to policies and adapters, not to core role semantics. Distinguish:

- `requested` — policy preference;
- `configured` — value written into a host profile;
- `effective` — runtime value reported by trustworthy host evidence;
- `verified` — effective value matches the request.

If effective routing cannot be verified, label it policy-only or manual, or require verification in the invoking workflow. Do not infer quality or cost from requested/configured values alone.
