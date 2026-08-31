# V02-REAL-012 architecture plan

## Decision

Issue two independent worker contracts and allow Wave 1 to run concurrently only in host-provided isolated worktrees:

1. `V02-REAL-012-avatar-validation` owns only `app/models.py` and `tests.py`.
2. `V02-REAL-012-404-copy` owns only `app/templates/errors/404.html`.

The contracts have no file overlap, no shared interface change, no dependency edge, no migration/manifest/lockfile/generated-file overlap, and no shared external service. The Python task's tests use a process-local in-memory SQLite database. Both workers inspect the same application configuration and may run Python validation, but isolation gives them separate worktree bytecode state and each compile command uses a distinct `/tmp` bytecode prefix. Therefore the shared logical test environment does not create a same-wave write conflict.

If isolated worktrees are unavailable, the host must run the tasks sequentially in the integration order below. `parallel_safe: true` is conditional on that isolation; it is not scheduling authority.

## Frozen plan identity

- Run: `V02-REAL-012-baseline`
- Revision: `1`
- Plan digest: `60f8dc183ce8814b02e017f1b62ef0d742e54e829a5b26be9d1d618f8c35090f`
- Base revision: `a975ef64864354867c88e0ed3a17ba7d17dca752`
- Source requirement digest: `e02e0ed37b2aa32edc53ee386a7b35c2517623ea4a087bc76fd564dc0207db1a`
- Complete machine-readable contracts: `task.json` and `task-2.json`

Any architecture or acceptance change requires a new plan revision and digest; both current nonterminal contracts must then be superseded.

## Frozen behavior

The avatar contract accepts only a non-boolean `int` from 1 through 2048 inclusive. It raises `ValueError("size must be an integer between 1 and 2048")` for all other values before URL construction. Valid inputs preserve the current lowercase-email MD5 digest and `https://www.gravatar.com/avatar/{digest}?d=identicon&s={size}` output. Tests retain the size-128 regression assertion, cover valid boundaries 1 and 2048, and cover `0`, `-1`, `2049`, `True`, `128.0`, `"128"`, and `None` as invalid.

The 404 contract uses exactly:

- Heading: `Page Not Found`
- Sentence: `The page you requested could not be found.`
- Link: `Return to the home page`

All strings remain gettext-wrapped. Template inheritance, the content block, `url_for('main.index')`, HTTP status, handlers, and JSON error behavior remain unchanged. Translation catalogs are deliberately out of scope because the acceptance packet authorizes only the template.

## Execution waves and integration

### Wave 1 — isolated parallel implementation and task-local validation

- Dispatch `task.json` and `task-2.json` from the same clean base revision.
- The host must provide one isolated worktree per task and verify the plan identity before dispatch.
- Each worker runs every required command in its own contract and returns criterion-indexed evidence.
- A worker must stop rather than expand scope, install dependencies, use the network, request credentials, weaken tests, or resolve an architecture/product decision.

### Wave 2 — sequential host integration and merged validation

Integrate the avatar task first and the template task second. Before accepting either result, verify its base revision, plan revision/digest, complete evidence, and unfiltered changed-path list. Reject or return any result that writes outside its contract.

On the merged tree, run sequentially:

1. `PYTHONDONTWRITEBYTECODE=1 python -m unittest tests.UserModelCase -v`
2. `PYTHONDONTWRITEBYTECODE=1 python -c "from tests import TestConfig; from app import create_app; app = create_app(TestConfig); response = app.test_client().get('/definitely-missing', headers={'Accept': 'text/html'}); body = response.get_data(as_text=True); assert response.status_code == 404; assert 'Page Not Found' in body; assert 'The page you requested could not be found.' in body; assert 'Return to the home page' in body"`
3. `python -m compileall -q app tests.py`
4. `git diff --check -- app/models.py tests.py app/templates/errors/404.html`
5. Verify the merged change list is exactly `app/models.py`, `tests.py`, and `app/templates/errors/404.html`.

The third command is the acceptance packet's exact required validation and may create ignored bytecode in the integration workspace; it is deliberately sequential rather than part of concurrent shared-state execution.

## Acceptance and evidence gate

The integrated result is acceptable only when:

- `AVA-1` through `AVA-4` in `task.json` each have direct satisfied evidence.
- `ERR-1` through `ERR-4` in `task-2.json` each have direct satisfied evidence.
- Every required task-local command and every Wave 2 command has its exact command, exit status, and pass/fail summary recorded.
- Both worker results prove their exclusive write scope with unfiltered `git diff --name-only` and focused diffs.
- The merged diff has only the three packet-authorized paths, existing tests were not weakened, and no unapproved generated file is included.

Missing criterion evidence, missing command evidence, contradictory output, stale plan identity, base mismatch, or path expansion makes the result incomplete and requires rejection or bounded correction.

## Routing and budgets

Per `sol-luna-v0.1`, the avatar task is a normal bounded Python change routed policy-only to Luna/high, and the 404 task is a tiny deterministic template edit routed policy-only to Luna/medium. The host has not supplied trusted effective-model observations, so neither configured preference is asserted as the effective route or as a cost guarantee. Equivalent host-verified worker profiles are permitted if they meet each contract's capabilities and authorization.

Each worker has at most two implementation attempts and one review round. A bounded review finding may become a correction contract within that budget. Architecture, interface, security, migration, concurrency, localization-policy, or new product-copy decisions return to the architect.

## Risk and human boundaries

The avatar task is medium risk because it tightens a public method's accepted inputs and Python booleans require explicit rejection. The template task is low risk but introduces untranslated source strings by an explicit scope decision. Parallel execution is safe only with the specified isolation and disjoint ownership; merged validation is sequential.

Human authority is required before any network use, credentials, external side effect, destructive action, new dependency, write outside the three packet paths, translation-catalog expansion, or change to the frozen input/copy contract. Environment or dependency failure is evidence to report, not authority to install, bypass, or broaden scope.
