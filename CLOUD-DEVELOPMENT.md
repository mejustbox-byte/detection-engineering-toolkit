# Среда разработки

Среда использует чистый checkout main, runtime из `.python-version` и frozen зависимости из `uv.lock`. Команды запускаются в корне репозитория. При первичной установке нужен доступ к официальным Python/uv/PyPI источникам; credentials runtime не нужны.

```bash
uv sync --frozen --extra dev
uv run --frozen detkit doctor
uv run --frozen --extra dev pytest -q
uv run --frozen --extra dev ruff check .
uv run --frozen --extra dev ruff format --check .
uv build
```

Храните cache/venv отдельно от публикуемых файлов. Временные output каталоги не заменяют source checkout и не должны попадать в PR. Восстановление среды проверяется новым checkout и повторением frozen install, а не наличием старого venv.

Linux cloud runtime подходит для offline разработки; реальные Windows Atomic/SIEM проверки требуют стенда из [LOCAL-PC.md](LOCAL-PC.md). Не храните реальные журналы и secrets в source tree. Source pin и CI patch runtime могут отличаться; записывайте фактическую версию через doctor.
