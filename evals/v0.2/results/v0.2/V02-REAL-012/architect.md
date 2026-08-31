# Architect result — V02-REAL-012

Two executable contracts are approved. `V02-REAL-012-T1` exclusively owns `app/models.py` and `tests.py`; `V02-REAL-012-T2` exclusively owns `app/templates/errors/404.html`.

## Fixed decisions

- T1 rejects `User.avatar` sizes `<= 0` with exactly `ValueError("size must be positive")`, tests `0` and `-1`, and preserves the exact size-128 URL.
- T2 changes only translatable 404 copy: heading “Page Not Found”, explanatory text “The page you requested could not be found.”, and link “Back to home”. It preserves template inheritance, block structure, and `main.index` target.

## Execution and integration

Wave 1 contains T1 and T2. Their files and interfaces are disjoint and no dependency edge exists, so they are ownership-parallel-safe. Actual concurrency is host-controlled. Because the supplied checkout and compile artifacts are shared, the host will serialize execution, capture each task patch/status at its boundary, and run the exact frozen compile validation for each; isolated worktrees would be required for true concurrency. After integration, the host may repeat the same frozen command as integration evidence, but it is already the only required acceptance command in each contract.

Both tiny changes route by policy to Luna/medium. Effective model and permissions are unverified. No network, installation, credentials, external effects, destructive actions, database/template expansion, or other writes are authorized.
