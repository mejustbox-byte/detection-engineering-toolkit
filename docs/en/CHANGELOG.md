# Changelog

## 0.1.0a2

Added doctor, external Sigma conversion, bundle integrity and optional Atomic commit provenance. Fixed the parse/hash race and lost cleanup metadata; malformed/cyclic Atomic metadata is rejected. Complete RU/EN documentation, bilingual REPORT, 29 tests and wheel smoke on both OS.

## 0.1.0a1 — 2026-10-09

First prerelease: four Discovery scenarios, Sigma, Splunk/Defender, offline fixtures/validation, GUID Atomic plans and SHA256 bundles. Linux/Windows CI: 20 tests. UTF-8 output supports legacy Windows pipes. Real laboratory validation was not run.

Before 1.0 the CLI/JSON contract may change between prereleases; published bundles remain standalone artifacts. The integrity verifier accepts the baseline 0.1.0a1 manifest.
