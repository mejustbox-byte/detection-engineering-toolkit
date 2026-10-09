# Threat model

## Assets

Local files, rule/query integrity, accurate evidence and laboratory state. Real identifiers and events belong to the operator and should not enter public artifacts.

| Threat | Control | Residual risk |
|---|---|---|
| Shell injection in ID/GUID | ID regex, UUID parsing; no shell runner | An operator may manually execute a malicious Atomic command |
| Unsafe YAML objects | safe_load | Alias/structural exhaustion is not fully eliminated |
| Oversized input | Read at most 8 MiB + 1 | Parsed structures can exceed the input size |
| Atomic changes after parse | Parse and hash the same snapshot | User-supplied source SHA does not attest upstream provenance |
| Manifest traversal | Exact filename allowlist and SHA256 format | No signature; local races are not prevented |
| Package tampering | Missing/extra-file and hash checks | An attacker may also modify the manifest |
| False coverage claims | Experimental/low, not_run fields, distinct validation levels | SIEM mapping and tuning remain operator responsibilities |
| Supply chain | Pinned packages and regression CI | A full vulnerability audit has not been run |

## Operational boundaries

Manifest verification does not establish authenticity or command safety. A positive synthetic case does not establish real detection. Committing real logs or running Atomic on production is outside the intended workflow.

Isolate the laboratory separately. See [LOCAL-PC.md](LOCAL-PC.md) and [SECURITY.md](SECURITY.md).
