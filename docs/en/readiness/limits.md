# Threat model and limits

Strict readiness JSON rejects duplicate keys, non-JSON constants, unknown fields, wrong types and unsupported chains. Loader caps are 8 MiB and depth 64. Up to 100 chains are accepted; --max-chains can lower this limit. No readiness input contains a command to execute. Output creation is exclusive and errors do not echo readiness source data.

Residual risks include false telemetry declarations, fabricated delivery records, sensitive risk labels, filesystem races and dependency/runtime bugs. Conversion output does not prove deployed-query behavior. No live Windows VM, SIEM or Atomic execution is supplied by this extension. Existing commands retain their earlier limits; the stricter readiness loader does not imply global parser hardening.

[Index](index.md)
