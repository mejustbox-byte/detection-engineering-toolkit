# Фактическая верификация

Дата: 2026-10-09. Runtime: Linux, CPython 3.12.15. На этапе подготовки успешно выполнены 19 unit/integration тестов, парсинг Sigma, SPL/KQL конвертация четырёх сценариев. Финальные результаты упаковки и проверки документов фиксируются ниже после выполнения.

Команды:

```bash
uv sync --frozen --extra dev
uv run --frozen --extra dev pytest -q
uv run --frozen --extra dev ruff check .
uv run --frozen --extra dev ruff format --check .
uv build
uv run --frozen detkit bundle T1033 --output output/demo
```

Не выполнено: Windows и macOS исполнение CLI, реальные Atomic upstream procedures, Windows endpoint telemetry, SIEM query execution, ingestion latency, CVE audit, удалённый Actions CI, публикация Cloud-среды. Подготовленный workflow не является успешным CI run. Публичный release не создавался.

Тестовая Atomic запись в pytest собственная синтетическая и явно так названа; она проверяет контракт parser/plan, а не совместимость выбранной upstream procedure. Для настоящего proof нужен протокол LOCAL-PC.

## Завершённые локальные проверки

- 19 тестов: успешно, включая обе конвертации для всех четырёх сценариев.
- ruff check и ruff format --check: успешно.
- uv sync --frozen --extra dev в новом venv с CPython 3.12.15: успешно.
- uv build: wheel и sdist собраны.
- Wheel установлен в отдельный venv; bundle выполнен из /tmp вне checkout: успешно.

Эти результаты локальные; GitHub Actions run/commit SHA отсутствуют.

Удалённый публичный репозиторий создан 2026-10-09; owner mejustbox-byte, права push/admin подтверждены.
