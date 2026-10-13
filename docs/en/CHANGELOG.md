# Changelog

## 0.1.0a4

Windows 4688 laboratory collector, explicit synthetic classification, strict import, unified lab-check and 19 new tests. SIEM delivery remains not_run.

## 0.1.0a3

Three Readiness chains on existing APIs, strict import and opsec-1.0 assessment, separate SIEM-delivery assertions and eleven RU/EN guides. Local suite: 55 tests; CI adds macOS.

## 0.1.0a2

Added doctor, external Sigma conversion, bundle integrity and optional Atomic commit provenance. Fixed the parse/hash race and lost cleanup metadata; malformed/cyclic Atomic metadata is rejected. Complete RU/EN documentation, bilingual REPORT, 31 tests and wheel smoke on both OS.

## 0.1.0a1 — 2026-10-09

First prerelease: four Discovery scenarios, Sigma, Splunk/Defender, offline fixtures/validation, GUID Atomic plans and SHA256 bundles. Linux/Windows CI: 20 tests. UTF-8 output supports legacy Windows pipes. Real laboratory validation was not run.

Before 1.0 the CLI/JSON contract may change between prereleases; published bundles remain standalone artifacts. The integrity verifier accepts the baseline 0.1.0a1 manifest.
