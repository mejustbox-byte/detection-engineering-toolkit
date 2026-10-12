# Check matrix

| ID | Pass evidence | Fail | not_tested |
|---|---|---|---|
| DET-001 | Declared available process-creation source | Available false | Unknown source/availability |
| DET-002 | Required mapping and positive event fields | Missing mapped or positive-event field | Missing mapping or positive cases |
| DET-003 | Positive and negative predicates match, both conversions produced | Predicate mismatch or empty conversion | Missing case class or cases |
| DET-004 | Complete, fresh delivery assertion with matching rule hash | Declared failure, wrong hash or stale assertion | No execution or incomplete evidence |

DET-001–003 failures are high; DET-004 failure critical. Required fields: Image for whoami/hostname; Image and CommandLine for ipconfig. Negative missing-field cases deliberately test non-match and do not represent a broken positive telemetry record. All passes remain scoped assertions, not technique completeness.

[Index](index.md)
