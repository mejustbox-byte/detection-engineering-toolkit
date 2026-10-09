# CLI reference

From a source checkout run `uv run --frozen detkit`; for a wheel use `detkit` from its venv. stdout is UTF-8: JSON for structured results, YAML for `rule`, query text for `convert`/`convert-file`. CLI messages may be Russian or English; the JSON schema is shared.

| Command | Purpose |
|---|---|
| `--version` | Installed product version |
| `list` | Four built-in scenarios |
| `doctor` | Dependency versions and all scenarios converted by both backends |
| `rule T1033` | Experimental scenario Sigma |
| `convert T1033 --target splunk` | SPL; `defender` outputs KQL |
| `convert-file rule.yml --target defender` | Convert external Sigma YAML |
| `bundle T1033 --output output/run-01` | Full package in a new directory |
| `verify-bundle output/run-01` | SHA256, missing-file and unexpected-file checks |
| `validate T1033 --cases cases.json` | Evaluate the scenario predicate on labelled events |
| `atomic-list T1033 --atomic-file T1033.yaml` | List local tests and GUIDs |
| `atomic-plan T1033 --atomic-file T1033.yaml --test-guid GUID` | Plan one Windows test |

## Examples

```bash
uv run --frozen detkit bundle T1016 --output output/network-01
uv run --frozen detkit verify-bundle output/network-01
uv run --frozen detkit validate T1016 --cases output/network-01/fixtures.json
uv run --frozen detkit convert-file output/network-01/rule.yml --target splunk
```

Atomic commands accept a **local** YAML and an existing GUID. `--atomic-commit` takes a full 40-character SHA as unverified provenance. `--lab-ack` only adds the `execute` string; it never runs a command.

```bash
uv run --frozen detkit atomic-list T1033 --atomic-file /path/to/atomics/T1033/T1033.yaml
uv run --frozen detkit atomic-plan T1033 --atomic-file /path/to/atomics/T1033/T1033.yaml --test-guid REPLACE_WITH_REAL_GUID
```

`bundle` also accepts `--atomic-file`, `--test-guid`, `--atomic-commit` and `--lab-ack`. Replace the sample path and GUID; invented GUIDs are not runnable tests.

## Exit codes

`0`: successful processing or a passing check. `1`: labelled-case or package-integrity failure. `2`: argument, read, parse or conversion error. `doctor` does not test SIEM/API/Windows infrastructure. `verify-bundle` checks integrity, not signatures or detection quality.

See [CORE-CONTRACT.md](CORE-CONTRACT.md) for the event format and exact limits.
