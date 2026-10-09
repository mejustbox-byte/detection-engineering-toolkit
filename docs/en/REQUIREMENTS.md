# Requirements

## Users and outcome

Detection engineers create and review rules, SOC analysts check SIEM fields and false positives, and purple teams connect a scenario to one Atomic GUID. The outcome is a portable artifact package with verifiable integrity and an explicit evidence level.

## Functional requirements

| Capability | Acceptance criterion |
|---|---|
| Catalogue | Four specific Windows Discovery scenarios; unknown IDs rejected |
| Generation | Valid Sigma YAML, stable UUID, ATT&CK reference and experimental status |
| Conversion | SPL/KQL via pySigma; fresh rule objects for every backend |
| External rule | Local UTF-8 YAML converts or returns an explicit error |
| Offline cases | Positive/negative cases, strict types, exit 1 on mismatch |
| Atomic | Technique/GUID/Windows checked; snapshot hash, cleanup, optional source SHA |
| Export | New directory, seven artifacts and manifest, no overwrite |
| Integrity | Detect modified, missing/extra files; reject traversal |
| Readiness | doctor converts every scenario with both backends |

## Nonfunctional requirements

No runtime network, credentials or shell execution. UTF-8 on Windows/Linux. Inputs up to 8 MiB; YAML safe_load. Frozen source installation. RU/EN documentation with the same contract. CI covers both OS and wheel installation outside the checkout. No production or full ATT&CK coverage claim.

## Outside 0.1.0a2

A full STIX catalogue, automatic Atomic execution, event delivery, SIEM APIs, correlation rules, tuning against real statistics and cryptographically signed bundles require separate design and evidence.
