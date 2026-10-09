# Architecture

## Components

| Module | Responsibility |
|---|---|
| `cli.py` | argparse, UTF-8 stdout, dispatch and exit codes |
| `core.py` | Inputs, scenarios, Sigma, conversion, validation, Atomic, export, integrity and doctor |
| `data/scenarios.json` | Four inspectable recipes with false positives |
| pySigma and backends | Sigma parsing and field/condition conversion into target queries |

## Data flow

`bundle` prepares all strings in memory: scenario → Sigma → two queries → fixtures/report → optional Atomic plan → manifest. It creates a new output directory only after preparation succeeds. Preparation failures create no directory. A write failure can leave a partial directory; inspect it and remove it or choose a new path. Atomic directory publication is not implemented.

`convert-file` reads external Sigma independently of the catalogue. `validate` evaluates only the built-in predicate. `verify-bundle` compares local bytes with the manifest. `doctor` exercises real backends and packaged data but does not test backend APIs.

## Trust boundaries

The checkout/installed dependencies are code. Input YAML/JSON is untrusted data. Atomic commands are retained as text, never executed. SIEM/Windows VM are external systems validated manually. The manifest records local integrity without signatures.

Installation and CI use the network; runtime CLI does not. Secrets and real events stay outside Git. See the [ADR](adr/0001-deterministic-offline.md).
