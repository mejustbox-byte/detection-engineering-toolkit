# Contributing

## Workflow

Create a branch from current main. Reproduce the defect, identify expected behavior and the validation level. Update code and RU/EN documentation together; published examples require synthetic inputs.

```bash
uv sync --frozen --extra dev
uv run --frozen --extra dev pytest -q
uv run --frozen --extra dev ruff check .
uv run --frozen --extra dev ruff format --check .
uv run --frozen detkit doctor
uv build
```

New scenarios need an ATT&CK reference, specific behavior, logsource, positive/negative cases and false positives. Exercise both backends. A catalogue entry does not imply complete technique coverage.

## Review

A PR describes the problem, resulting behavior, checks and limitations. Review malformed-input handling, version/lock alignment, packaged data and wheel installation. Windows/Linux CI must pass before merge. Contract changes need an ADR or compatibility explanation. Laboratory evidence should be a sanitized protocol, not raw logs.

Keep personal data, credentials, internal endpoints and operational correspondence out of code, documents, commit messages and release notes. See [SECURITY.md](SECURITY.md).
