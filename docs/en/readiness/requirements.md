# Scope and acceptance

Detection Readiness extends the existing toolkit rather than creating a second rule engine. Three narrow chains link declared risk, Windows process-creation telemetry, generated Sigma, existing predicate cases and separate SIEM-delivery assertions: T1033/whoami, T1082/hostname and T1016/ipconfig /all.

The acceptance matrix distinguishes source availability, required field mapping, positive/negative offline predicate cases and externally supplied delivery evidence. Synthetic matching does not upgrade delivery to verified. Existing toolkit commands retain their interfaces; readiness adds an offline command and normalized assessment. No Atomic procedure or SIEM query is executed.

[Index](index.md)
