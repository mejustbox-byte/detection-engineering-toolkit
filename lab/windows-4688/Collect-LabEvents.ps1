#Requires -Version 5.1
[CmdletBinding()]
param(
    [Parameter(Mandatory=$true)][string]$OutputDirectory,
    [Parameter(Mandatory=$true)][switch]$LabAcknowledgement,
    [ValidateRange(1,60)][int]$WaitSeconds = 10
)
$ErrorActionPreference = 'Stop'
if (-not $LabAcknowledgement) { throw 'An isolated, authorized laboratory is required.' }
if ($env:OS -ne 'Windows_NT') { throw 'Windows is required.' }
if (Test-Path -LiteralPath $OutputDirectory) { throw 'Output directory must not exist.' }
$executionId = [guid]::NewGuid().ToString()
$started = [DateTime]::UtcNow
New-Item -ItemType Directory -Path $OutputDirectory | Out-Null
# No audit-policy changes, downloads, SIEM connection or log clearing.
$definitions = @(
    @{ id='whoami-positive'; technique='T1033'; expected=$true; executable='whoami.exe'; arguments=@() },
    @{ id='hostname-positive'; technique='T1082'; expected=$true; executable='hostname.exe'; arguments=@() },
    @{ id='ipconfig-positive'; technique='T1016'; expected=$true; executable='ipconfig.exe'; arguments=@('/all') },
    @{ id='other-process-negative'; technique='T1033'; expected=$false; executable='cmd.exe'; arguments=@('/c','ver') }
)
$commands = @()
foreach ($definition in $definitions) {
    $image = Join-Path $env:SystemRoot ('System32\' + $definition.executable)
    $parameters = @{ FilePath=$image; PassThru=$true; Wait=$true; NoNewWindow=$true;
        RedirectStandardOutput=(Join-Path $OutputDirectory ($definition.id + '.stdout.txt'));
        RedirectStandardError=(Join-Path $OutputDirectory ($definition.id + '.stderr.txt')) }
    if ($definition.arguments.Count -gt 0) { $parameters.ArgumentList = $definition.arguments }
    $process = Start-Process @parameters
    $commands += @{ id=$definition.id; technique=$definition.technique; expected=$definition.expected;
        pid=$process.Id; image=$image; exit_code=$process.ExitCode }
}
Start-Sleep -Seconds $WaitSeconds
$finished = [DateTime]::UtcNow
$events = @()
$collectionState = 'available'
try {
    $records = @(Get-WinEvent -FilterHashtable @{ LogName='Security'; Id=4688; StartTime=$started.ToLocalTime(); EndTime=$finished.ToLocalTime() } -MaxEvents 10000 -ErrorAction Stop)
    foreach ($record in $records) {
        [xml]$xml = $record.ToXml()
        $fields = @{}
        foreach ($node in $xml.Event.EventData.Data) { $fields[$node.Name] = [string]$node.'#text' }
        if (-not $fields.ContainsKey('NewProcessId')) { continue }
        $processId = [Convert]::ToInt64(($fields['NewProcessId'] -replace '^0x',''),16)
        $selected = @($commands | Where-Object { $_.pid -eq $processId -and $_.image -ieq $fields['NewProcessName'] })
        if ($selected.Count -ne 1) { continue }
        $events += @{ case_id=$selected[0].id; record_id=$record.RecordId;
            observed_at=$record.TimeCreated.ToUniversalTime().ToString('yyyy-MM-ddTHH:mm:ssZ');
            process_id=$processId; Image=$fields['NewProcessName'];
            CommandLine= $(if ($fields.ContainsKey('CommandLine')) { $fields['CommandLine'] } else { $null }) }
    }
    if ($records.Count -eq 10000) { $collectionState = 'truncated' }
} catch {
    $collectionState = 'unavailable'
}
$manifest = @{ schema_version='windows-lab-1.0'; synthetic=$false; execution_id=$executionId;
    started_at=$started.ToString('yyyy-MM-ddTHH:mm:ssZ'); completed_at=$finished.ToString('yyyy-MM-ddTHH:mm:ssZ');
    collection_state=$collectionState; commands=@($commands); events=@($events);
    siem_delivery='not_run'; provenance='operator_supplied_unverified' }
$json = $manifest | ConvertTo-Json -Depth 8
$utf8 = New-Object System.Text.UTF8Encoding($false)
[System.IO.File]::WriteAllText((Join-Path $OutputDirectory 'events.json'), $json, $utf8)
Write-Output ('Lab manifest written. Collection state: ' + $collectionState + '. SIEM delivery: not_run.')
if ($collectionState -ne 'available' -or $events.Count -ne $commands.Count) { exit 2 }
