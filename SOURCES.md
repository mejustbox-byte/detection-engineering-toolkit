# Источники

Первичные источники для модели правил, telemetry и ручного лабораторного процесса. Проверены при подготовке 0.1.0a3; содержимое upstream может изменяться.

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

Встроенные рецепты и synthetic fixtures созданы в этом проекте; upstream Sigma/Atomic правила не включены. Для реального Atomic сохраните полный commit и SHA256 YAML. Версии Python dependencies фиксируются в pyproject/uv.lock.
