# Sources

Primary references for rule models, telemetry and the manual laboratory workflow. Checked while preparing 0.1.0a2; upstream content may change.

- [MITRE ATT&CK T1033](https://attack.mitre.org/techniques/T1033/)
- [MITRE ATT&CK T1082](https://attack.mitre.org/techniques/T1082/)
- [MITRE ATT&CK T1016](https://attack.mitre.org/techniques/T1016/)
- [MITRE ATT&CK T1057](https://attack.mitre.org/techniques/T1057/)
- [Sigma backends](https://sigmahq.io/docs/digging-deeper/backends)
- [Sigma processing pipelines](https://sigmahq.io/docs/digging-deeper/pipelines.html)
- [pySigma](https://github.com/SigmaHQ/pySigma)
- [Splunk backend](https://github.com/SigmaHQ/pySigma-backend-splunk)
- [Microsoft 365 Defender backend](https://github.com/SigmaHQ/pySigma-backend-microsoft365defender)
- [Atomic Red Team](https://github.com/redcanaryco/atomic-red-team)
- [Invoke-AtomicRedTeam execution](https://github.com/redcanaryco/invoke-atomicredteam/wiki/Execute-Atomic-Tests-%28Local%29)
- [Atomic prerequisites](https://github.com/redcanaryco/invoke-atomicredteam/wiki/Check-or-Get-Prerequisites-for-Atomic-Tests)
- [Sysmon process creation](https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon)
- [Windows 4688](https://learn.microsoft.com/windows/security/threat-protection/auditing/event-4688)
- [DeviceProcessEvents](https://learn.microsoft.com/en-us/defender-xdr/advanced-hunting-deviceprocessevents-table)

Built-in recipes and synthetic fixtures are authored in this project; upstream Sigma/Atomic rules are not bundled. Record the full commit and YAML SHA256 for real Atomic use. Python dependency versions are recorded in pyproject/uv.lock.
