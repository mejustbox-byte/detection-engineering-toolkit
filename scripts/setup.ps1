$ErrorActionPreference = 'Stop'
Set-Location (Join-Path $PSScriptRoot '..')
uv sync --frozen --extra dev
if ($LASTEXITCODE -ne 0) { throw 'Ошибка установки' }
uv run --frozen --extra dev pytest -q
if ($LASTEXITCODE -ne 0) { throw 'Ошибка тестов' }
uv run --frozen --extra dev ruff check .
if ($LASTEXITCODE -ne 0) { throw 'Ошибка lint' }
uv run --frozen detkit doctor
if ($LASTEXITCODE -ne 0) { throw 'Ошибка smoke test' }
