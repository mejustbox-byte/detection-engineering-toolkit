# Architecture and reuse

Strict report-contract loading feeds an exact readiness-1.0 model. scenario_for, generate_rule, validate_cases and convert are the existing toolkit APIs. Generation validates Sigma structure with pySigma and conversion uses the existing Splunk/Defender backends. validate_cases checks only the toolkit scenario predicate, not Sigma evaluation.

The result wrapper contains an opsec-1.0 assessment and chain catalog with risk label, technique, rule hash, conversion outcomes and explicit unverified provenance. Raw events and execution IDs are not copied, but risk/scope/chain identifiers require privacy review. Per-chain checks are independent: declared source failure does not pretend that local fixture generation was unavailable, and local test pass does not prove delivery.

[Index](index.md)
