# Windows process-event laboratory

Status: alpha preparation. Linux offline import and assessment are tested. Windows collection, SIEM ingestion, rule execution and Atomic execution remain untested. PowerShell syntax parsing in Windows CI is not a collection test.

## Scope and preparation

Use a disposable Windows VM with a local test account, no production credentials and a snapshot. Keep the VM away from production networks. Record Windows build, PowerShell version, SIEM version and baseline audit settings privately before changing anything.

Manually enable successful Audit Process Creation in Advanced Audit Policy / Detailed Tracking, and Include command line in process creation events under Administrative Templates / System / Audit Process Creation. Names vary with OS language and policy management. Confirm effective settings on the selected VM. Domain policy may override local settings. The collector does not configure policies.

Command-line auditing records arguments in plain text for all audited processes; passwords and other sensitive arguments may appear in the Security log. Use only laboratory data. After testing, restore the snapshot or the previously recorded policy values. Do not clear production logs.

## Collection on Windows

From the repository root, run Windows PowerShell 5.1 with permission to read the Security log. The output directory must not exist. No execution-policy change is required by the toolkit; follow the laboratory's script policy.

```powershell
.\lab\windows-4688\Collect-LabEvents.ps1 -OutputDirectory .\lab-output\run-001 -LabAcknowledgement
```

The collector runs whoami, hostname, ipconfig /all and cmd /c ver as a negative control. It reads Security event 4688 for their PID/image pairs within the bounded time window. It makes no audit-policy changes or SIEM connections. It writes UTF-8 without BOM. Exit 0 means the four event records were collected; exit 2 means incomplete collection, and a terminating PowerShell error means setup/execution failure. Exit 0 does not prove required fields, Sigma execution or SIEM detection.

The private output includes stdout/stderr and events.json. It may expose usernames, hostnames, addresses and command lines. Create the output under an access-restricted private directory. lab-output is git-ignored as an accidental-commit precaution, not an access control. Never publish real raw output. Retain original Security XML privately if source traceability is needed; this manifest is unsigned operator-supplied evidence and does not establish authenticity.

## Offline assessment on Linux or Windows

Install the toolkit using the repository setup guide. For real collection, use its events.json. For the executable offline example below, the source is explicitly synthetic.

```bash
detkit lab-check examples/windows-lab.synthetic.json --observed-at 2026-10-13T10:00:20Z --output lab-assessment.json
```

Expected exit 2: nine checks pass and three SIEM delivery checks remain not_tested. The output must not already exist. Codes: 0 complete, 1 failed checks, 2 incomplete assessment, 3 invalid input/output. lab-import only validates and normalizes, returning 0 on import success; it does not assess readiness.

## Contract and SIEM handoff

windows-lab-1.0 requires schema_version, synthetic (strict boolean), execution_id, started_at, completed_at, collection_state, commands, events, siem_delivery=not_run and provenance=operator_supplied_unverified. The checked-in example defines exact command/event keys. Four known commands, unique positive PID values and unique record IDs are required. Time window is at most one hour; at most 256 selected events are accepted. Unknown keys, duplicate JSON keys and UTF-8 BOM are rejected. Classification is supplied by the operator and remains unverified. Old manifests missing synthetic must be recollected or explicitly classified after provenance review.

Mapping: NewProcessName → Image; CommandLine → CommandLine; hexadecimal NewProcessId → decimal process_id; EventRecordID → record_id. Missing telemetry stays unknown. Missing ipconfig command-line data fails its field check. These predicates are offline approximations, not Sigma execution.

For SIEM validation, configure the actual event source and field mapping in the chosen laboratory, generate the toolkit rule/query for each technique, and run it against the collected positive and negative controls. Save private ingestion times, SIEM event IDs, query/rule hashes, actual matches and negative-control results. No automatic SIEM uploader or result verifier is included; imported manifests retain delivery=not_run. Manual JSON editing cannot establish independently verified detection. Record the before/after result in the case template.

## Sources

- [Microsoft: event 4688](https://learn.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4688)
- [Microsoft: command-line process auditing](https://learn.microsoft.com/en-us/windows-server/identity/ad-ds/manage/component-updates/command-line-process-auditing)
- [Case template](case-template.md)
- [Collector](../../../lab/windows-4688/Collect-LabEvents.ps1)
