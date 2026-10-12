# Delivery evidence and provenance

DET-004 is evaluated independently from fixture and conversion success. verified needs a nonempty execution ID, timestamp and generated rule hash. The hash must match the exact generated YAML bytes. Maximum age defaults to 30 days and can be set to 1–3650; exact boundary passes and one second older fails. Future timestamps reject the input.

The toolkit does not access SIEM logs, validate an execution ID or authenticate this assertion. The catalog always labels provenance user_supplied_unverified. A verified assertion passing these consistency checks is not independently verified delivery. not_run/unknown and incomplete verified records stay not_tested. Failed delivery remains fail even with absent metadata.

[Index](index.md)
