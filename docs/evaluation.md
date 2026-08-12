# Evaluation methodology

Eclipse provides a result format and runner for comparing workflow strategies without manufacturing conclusions.

Representative strategies include:

- one strong model for the whole task;
- architect + economical worker + independent reviewer;
- alternative routing/reasoning policies.

Cases declare a fixture, objective, acceptance IDs, and forbidden paths. Results record task success, criterion satisfaction, test pass rate, regressions, review findings, architectural violations, unauthorized scope, latency, architect/worker invocations, retries, and usage.

Usage must be labelled `measured`, `estimated`, or `unavailable`. Cost is recorded only with a source and currency. API list prices must not be projected onto subscription accounting as though they were measured spend.

CI uses deterministic recorded hosts:

```bash
eclipse eval run examples/evaluation/suite.json \
  --outcomes examples/evaluation/recorded-outcomes.json \
  --output evaluation-results/example.json
```

The example outcomes exercise the data pipeline; they are fixtures, not benchmark evidence. Live evaluation requires a separate host integration, credentials supplied outside repository state, reproducible model/settings, and the same case suite. Reports deliberately leave `conclusion` null so analysis is based on observed runs.
