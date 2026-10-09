# Local laboratory guide

## Environment

Use a separate Windows VM with a snapshot, controlled network, working process-creation telemetry and dedicated test accounts. Appropriately configured Sysmon Event ID 1 or Security 4688 can provide Windows events; command-line collection for 4688 must be enabled separately. Defender needs device onboarding and DeviceProcessEvents delivery. macOS/Linux can build packages but cannot replace the Windows lab.

## Telemetry and queries

| Target | Fields and checks |
|---|---|
| Splunk | Confirm Windows process events expose `Image`/`CommandLine`; restrict index, sourcetype, host and time according to the local deployment |
| Defender | Open Advanced Hunting; verify `DeviceProcessEvents`, `FileName`/`FolderPath`/`ProcessCommandLine` and the device |

Inspect the actual generated query: the pipeline may transform field names. Do not introduce aliases without inspecting the source event. Missing results can mean missing telemetry, delivery latency or a schema mismatch.

## Single-scenario protocol

1. Record the Toolkit commit, Python/backend versions, Windows build and sensor/SIEM versions.
2. Pin the upstream Atomic commit, YAML path and Windows GUID; retain the SHA256.
3. Take a snapshot. Review the test command, defaults, elevation, prerequisites and cleanup. Review prerequisite installation separately.
4. Build the package and run `verify-bundle`; review Sigma/SPL/KQL and correspondence to the selected test.
5. Use ShowDetails and CheckPrereqs to check readiness. Configure the correct Invoke-AtomicRedTeam `PathToAtomicsFolder` separately from Toolkit's YAML path.
6. Record UTC start/end and manually run one approved test in the VM. Toolkit does not execute it.
7. Retain the raw event and Event ID/Record ID or Defender timestamp/device ID locally. Establish actual SIEM delivery.
8. Execute the query in a narrow time window; identify the specific matching event and record delivery latency.
9. Run a negative case with another utility and a legitimate matching case. The latter demonstrates a false positive, not rule breakage.
10. Perform reviewed cleanup and confirm restored state; revert the snapshot if needed.

## Evidence

Record `pass`, `fail` or `not_run` separately for execution, telemetry delivery, query match, negative case and cleanup. For failures include the observation and reproduction step. Keep real events and host/user identifiers outside the public repository. Publish only sanitized reports and synthetic examples.

Real laboratory results have not yet been obtained for this project. Linux/Windows offline tests do not replace them.
