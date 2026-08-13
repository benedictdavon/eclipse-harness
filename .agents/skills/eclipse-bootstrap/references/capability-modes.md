# Capability modes

Label each host feature independently:

- `native` — the host directly provides it;
- `emulated` — a host-supported combination preserves the semantics;
- `manual` — the user transfers contracts or selects roles explicitly;
- `unsupported` — the workflow cannot provide that feature on this host.

Use the same labels for delegation, per-role model selection, reasoning effort, reviewer isolation, scoped writes, parallel agents, and shared context. A limitation in one capability does not invalidate the contract workflow.

Requested or configured model and permission values remain intent until trustworthy host metadata establishes the effective value.
