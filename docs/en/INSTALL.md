# Installation

## From source

Supported runtime: CPython 3.12+. CI runs Python 3.12 on Windows and Linux; a full macOS validation has not been run. `uv.lock` locks dependencies; use uv 0.12.23 for reproduction. `.python-version` selects 3.12.15.

```bash
git clone https://github.com/mejustbox-byte/detection-engineering-toolkit.git
cd detection-engineering-toolkit
uv sync --frozen --extra dev
uv run --frozen detkit --version
uv run --frozen detkit doctor
uv run --frozen --extra dev pytest -q
```

Linux/macOS: `bash scripts/setup.sh`. Windows PowerShell: `./scripts/setup.ps1`. Review the script first. It installs dependencies and runs offline checks.

## From a wheel

Download the wheel and `SHA256SUMS` from the same GitHub Release. Verify the SHA256 before installing into a separate venv:

```bash
python -m venv .venv
# Linux/macOS
.venv/bin/python -m pip install detection_engineering_toolkit-0.1.0a2-py3-none-any.whl
.venv/bin/detkit doctor
```

On Windows use `.venv/Scripts/python.exe` and `.venv/Scripts/detkit.exe`. The wheel contains code and the built-in catalogue; the source ZIP/sdist includes full documentation and the lock. Wheel installation resolves transitive dependencies through pip; use source plus `uv.lock` for an exact frozen environment.

## Troubleshooting

- Missing `uv`: install the specified version from the official uv source and open a new shell.
- `No module named detection_toolkit`: use `uv run --frozen` or activate the venv containing the wheel.
- Existing output directory: choose a new path; export deliberately refuses to overwrite it.
- Conversion rejected: check the Sigma logsource and selected backend capabilities.
- First installation requires network access; the installed CLI only reads local inputs.

Next: [RUNBOOK.md](RUNBOOK.md) and [DEMO.md](DEMO.md).
