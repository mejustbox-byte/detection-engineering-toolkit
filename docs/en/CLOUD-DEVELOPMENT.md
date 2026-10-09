# Development environment

Use a clean main checkout, the runtime in `.python-version` and frozen dependencies from `uv.lock`. Run commands from the repository root. Initial setup needs official Python/uv/PyPI access; runtime requires no credentials.

```bash
uv sync --frozen --extra dev
uv run --frozen detkit doctor
uv run --frozen --extra dev pytest -q
uv run --frozen --extra dev ruff check .
uv run --frozen --extra dev ruff format --check .
uv build
```

Keep caches/venvs separate from published files. Temporary output directories are not source checkouts and should not enter a PR. Validate restoration through a new checkout and frozen installation, not the existence of an old venv.

A Linux cloud runtime supports offline development; real Windows Atomic/SIEM validation needs the lab in [LOCAL-PC.md](LOCAL-PC.md). Keep real logs and secrets outside the source tree. Source pin and CI patch runtimes may differ; record the actual version with doctor.
