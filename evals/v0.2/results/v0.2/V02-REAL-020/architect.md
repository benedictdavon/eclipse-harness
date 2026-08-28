# Architecture disposition

Executable vertical-slice task `V02-REAL-020-T01` is approved. Keeping types, the minimal fixture, component state, and focused check under one owner avoids an intermediate invalid status contract.

Wave 1 contains only this task. The host starts from the trusted clean base and captures its patch/status and frozen validation evidence before integration; no concurrent writer is authorized on the invoice status interface.

Risk is medium due to cross-file type consistency and accessibility. Route to a bounded-complex low-cost/high-reasoning executor; preferred identity is policy-only because runtime observations are unverified. The packet command is the sole required validation. No network, credentials, external effects, destructive actions, dependency installation, descendants, package/lockfile changes, or writes beyond four scoped paths are authorized. Database/business-rule expansion returns to the architect; host owns isolation, artifact capture, and integration.
