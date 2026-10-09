# Detection Engineering Toolkit

**Turn ATT&CK scenarios into reviewable detection packages.**

[Русский](README.ru.md) · [Documentation](docs/en/INDEX.md) · [CLI reference](docs/en/RUNBOOK.md) · [Lab guide](docs/en/LOCAL-PC.md)

Detection Engineering Toolkit is a local CLI for detection engineers, SOC analysts and purple teams. It connects a specific ATT&CK scenario to an experimental Sigma rule, Splunk SPL and Microsoft Defender KQL, synthetic test cases and a selected Atomic Red Team test plan. One package captures the outputs and checksums for review and repeatable verification.

## Why use it

- **Reproducible outputs:** locked dependencies, stable rule UUIDs and identical artifacts for identical inputs in the same version.
- **Portable detections:** real pySigma backends and processing pipelines for two target platforms.
- **Quality checks:** `doctor` exercises the installed tool, `validate` checks expected scenario behavior, and `verify-bundle` checks package integrity.
- **Bring your own rules:** `convert-file` converts local Sigma YAML independently of the built-in scenario catalogue.
- **Connect Red and Blue:** select one Atomic GUID, retain the YAML SHA256, prerequisites and cleanup; execution is a separate lab step.
- **Inspectable implementation:** source, tests, English/Russian documentation and Windows/Linux CI. Runtime makes no network requests and executes no emulation commands.

## Quick start

Python 3.12+ and uv 0.12.23 are required. Initial dependency installation uses the network.

```bash
git clone https://github.com/mejustbox-byte/detection-engineering-toolkit.git
cd detection-engineering-toolkit
uv sync --frozen --extra dev
uv run --frozen detkit doctor
uv run --frozen detkit bundle T1033 --output output/whoami
uv run --frozen detkit verify-bundle output/whoami
uv run --frozen detkit validate T1033 --cases output/whoami/fixtures.json
```

## Supported scenarios

| ATT&CK | Observable behavior | Telemetry |
|---|---|---|
| T1033 | `whoami.exe` process execution | Windows process creation |
| T1082 | `hostname.exe` process execution | Windows process creation |
| T1016 | `ipconfig.exe` with the `/all` substring | Windows process creation |
| T1057 | `tasklist.exe` process execution | Windows process creation |

A scenario does not cover an entire technique. These utilities have common legitimate uses; generated rules are `low` severity and `experimental`.

## Inside a package

`rule.yml`, `splunk.txt`, `defender.txt`, `fixtures.json`, `validation.json`, `atomic-plan.json`, bilingual `REPORT.md` and `manifest.json`. The manifest stores SHA256 digests for the other seven files. Export refuses to overwrite an existing directory.

```bash
uv run --frozen detkit rule T1016
uv run --frozen detkit convert T1016 --target splunk
uv run --frozen detkit convert-file output/whoami/rule.yml --target defender
```

## Product status

Version **0.1.0a2**, prerelease. The offline CLI is implemented and tested. Predicate validation does not execute Sigma or a SIEM query. Conversion does not establish telemetry delivery or detection in a particular SIEM. Real Windows VM, upstream Atomic and SIEM validation are **not run**. Follow the [lab guide](docs/en/LOCAL-PC.md) to collect that evidence.

Built for practical detection engineering in 2026: reproducible artifacts, recorded input provenance and clearly scoped results. No independent ranking, market leadership or production-ready status is claimed.

## Explore

[Installation](docs/en/INSTALL.md) · [End-to-end example](docs/en/DEMO.md) · [Contract](docs/en/CORE-CONTRACT.md) · [Threat model](docs/en/THREAT-MODEL.md) · [Security](docs/en/SECURITY.md) · [Verification](docs/en/VERIFICATION.md) · [Roadmap](docs/en/ROADMAP.md)
