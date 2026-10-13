# Detection validation case

Use synthetic or reviewed anonymized data for publication. Keep raw source evidence private. A blank field means not tested, not successful.

| Evidence | Baseline | After change |
| --- | --- | --- |
| Data class: synthetic / operator-supplied live | | |
| Windows build, PowerShell, SIEM version | | |
| Effective audit policy and change | | |
| UTC execution ID and interval | | |
| Positive/negative controls and event IDs | | |
| Event ingestion time and latency | | |
| Image/CommandLine mapping | | |
| Rule/query SHA256 and actual query | | |
| Positive matches / expected count | | |
| Negative matches / expected zero | | |
| Sigma/SIEM execution status | | |
| Exceptions, false positives, unknowns | | |
| Private evidence location and reviewer | | |
| Snapshot/policy rollback result | | |

Specify the failure trigger, the exact change and the measured result. Distinguish predicate tests, conversion, ingestion and actual SIEM execution. No latency or detection-rate claim is valid without measured events. Record review and sanitization separately; neither proves source authenticity.
