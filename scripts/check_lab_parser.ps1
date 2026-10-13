$ErrorActionPreference = 'Stop'
$path = Join-Path $PSScriptRoot '../lab/windows-4688/Collect-LabEvents.ps1'
$tokens = $null
$errors = $null
[System.Management.Automation.Language.Parser]::ParseFile($path, [ref]$tokens, [ref]$errors) | Out-Null
if ($errors.Count -gt 0) { throw ($errors | Out-String) }
Write-Output 'Collector syntax parsed; collection and SIEM delivery were not executed.'
