# Contributing

Use a focused branch and keep changes within a clear protocol or implementation objective. Add tests for every behavioral change, including negative paths.

Development setup:

```bash
python -m pip install -e ".[dev]"
python -m pytest
ruff check .
mypy src
python -m build
```

When changing a schema, update the matching typed validator, examples, migration/compatibility notes, tests, and schema version when required. Generated Codex/Copilot files must be regenerated from `policies/sol-luna.json`; do not edit them by hand.

Pull requests should explain architecture impact, protocol compatibility, security impact, exact validation, and any known limitation. Do not include credentials, recorded private prompts, runtime `.eclipse/runs` data, or fabricated evaluation conclusions.
