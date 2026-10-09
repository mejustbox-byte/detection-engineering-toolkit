# ADR 0001: Deterministic offline CLI

Status: accepted. Date: 2026-10-09.

## Context

The path from ATT&CK to a query and lab test needs to be inspectable without SIEM credentials or host changes. Generating an arbitrary rule from an ID alone can imply complete technique coverage incorrectly.

## Decision

Use four specific authored scenarios, stable UUIDs, pySigma backends/pipelines and a separate limited evaluator. Select Atomic tests from local YAML by GUID; parsing and SHA256 use one snapshot. Convert external Sigma separately. Write bundles to a new directory and verify against their manifest. The Python CLI contains no shell/network runner.

## Consequences

Inputs/outputs are straightforward to review; runtime needs no network or secrets. The catalogue is narrow, the predicate is not universal and SIEM mapping is deployment-specific. Unsigned integrity does not establish authenticity. Real delivery, query matches and cleanup require a manual lab. Future runners/APIs require a new ADR and threat model.
