# Validation methodology

## Evidence levels

| Level | Establishes | Does not establish |
|---|---|---|
| Sigma parsing | pySigma accepts the rule structure | Signal quality |
| Backend conversion | The selected model produces SPL/KQL | Query execution in a particular SIEM |
| Offline predicate | Suffix/substring behavior on labelled cases | Sigma/query execution or all-backend semantic equivalence |
| Bundle integrity | Bytes match the manifest | Authenticity, safety or full coverage |
| Real lab | Execution, event delivery, query match and cleanup occurred | Universality across deployments |

## Automated checks

```bash
uv sync --frozen --extra dev
uv run --frozen --extra dev pytest -q
uv run --frozen --extra dev ruff check .
uv run --frozen --extra dev ruff format --check .
uv run --frozen detkit doctor
uv build
```

Windows/Linux CI also builds a bundle, checks the manifest and installs the wheel into a separate venv outside the checkout. Tests cover every scenario/both backends, invalid inputs, Atomic GUID/snapshot provenance, legacy-pipe UTF-8, external Sigma, modified/missing/extra artifacts and traversal.

## Regression discipline

When changing a rule, dependency or pipeline, compare queries and the manual contract. Add a negative case tied to the actual defect. Do not automatically label unknown events expected=false: labels need a rationale. Sanitize real telemetry before publication.

See [VERIFICATION.md](VERIFICATION.md) for status and [LOCAL-PC.md](LOCAL-PC.md) for the lab protocol.
