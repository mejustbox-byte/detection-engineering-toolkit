# Readiness alpha 0.1.0a3

Adds detkit readiness, three risk/event/rule/test chains, four consistency checks, common report-contract validation and explicit user_supplied_unverified delivery provenance. Existing 31 tests remain and the expanded suite passes 55 tests locally. Existing rule generation and both backend conversions are reused.

This is an alpha extension: no Sigma execution engine, SIEM connection, emulation or independent delivery verification. Default synthetic examples return incomplete coverage because delivery is not_run. Hosted CI 38243279691 passed all three platforms: 55 tests, readiness documentation and installed-wheel verification.

[Index](index.md)
