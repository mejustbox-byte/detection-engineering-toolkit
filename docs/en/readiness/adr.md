# ADR: extend existing APIs

Use the existing Python 3.12 toolkit, pySigma backends and frozen uv dependency workflow. Add exact report-contract 0.1.0a1 through its released wheel with the published SHA-256. Shared loading and status validation avoid a competing report model. uv.lock records the dependency update.

A new Sigma interpreter is deliberately excluded. The existing predicate API stays explicitly labeled offline_scenario_predicate, while Sigma parsing/conversion and SIEM delivery are separate evidence types. CI adds macOS to Linux/Windows and exercises existing commands, readiness, documentation and installed-wheel resources.

[Index](index.md)
