# End-to-end demonstration

## 1. Prepare the tool

```bash
uv sync --frozen --extra dev
uv run --frozen detkit doctor
```

Record the checkout version and doctor output. Its `passed` field establishes local catalogue and backend availability.

## 2. Build a T1016 package

```bash
uv run --frozen detkit bundle T1016 --output output/demo-network
uv run --frozen detkit verify-bundle output/demo-network
uv run --frozen detkit validate T1016 --cases output/demo-network/fixtures.json
```

Inspect Sigma, SPL/KQL and the JSON report. Confirm the negative cases exist. The observable signal is `ipconfig.exe` with `/all`; ordinary diagnostics also match.

## 3. Convert your own rule

```bash
uv run --frozen detkit convert-file output/demo-network/rule.yml --target defender
```

This converts a file from disk. External rules can use other backend-supported conditions; built-in scenario validation does not validate those rules.

## 4. Connect Atomic

Obtain upstream Atomic Red Team separately through a controlled process, pin its commit and select a Windows GUID using `atomic-list`. Create a **new** bundle with `--atomic-file`, `--test-guid` and `--atomic-commit`. Compare the actual command with the rule. Review ShowDetails, prerequisites, input arguments and cleanup. `--lab-ack` is only required to output the execution command.

## 5. Collect laboratory evidence

Follow [LOCAL-PC.md](LOCAL-PC.md) to obtain Splunk/Defender events, run the query, check a negative case and complete cleanup. Record exact versions, UTC time, delivery latency and results. Until then, the accurate demonstration result is “artifacts generated, offline cases passed, real SIEM/Atomic not_run”.

The demonstration provides a traceable chain and exposes gaps between behavior, telemetry and the query.
