# User guide

The synthetic example writes a wrapper and returns 2: nine local declaration checks pass and three SIEM-delivery checks remain not_tested. Code 1 indicates a known failure, 3 an invalid readiness input/output. Existing commands keep their earlier codes. Output must not exist. Use --maximum-age-days for explicit delivery age policy. The assessment field is opsec-1.0; the outer chain catalog is not a report-contract envelope.

```bash
uv sync --frozen --extra dev
uv run --frozen detkit readiness examples/readiness.synthetic.json --observed-at 2026-10-12T00:00:00Z --output readiness.json
```

[Index](index.md)
