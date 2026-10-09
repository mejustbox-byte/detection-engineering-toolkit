# Верификация

## Проверенное окружение

CPython 3.12.15, uv 0.12.23, зависимости из uv.lock. Локальные проверки выполнены на Linux. GitHub Actions проверяет Linux и Windows.

## Результаты

| Проверка | Результат |
|---|---|
| 20 unit/integration тестов | pass на Linux и Windows |
| Sigma parsing и SPL/KQL conversion четырёх сценариев | pass |
| UTF-8 stdout при исходной cp1252 кодировке | pass |
| ruff check | pass |
| Frozen install | pass |
| Wheel/sdist build | pass |
| Offline bundle smoke | pass на Linux и Windows |
| Установка wheel в отдельный venv вне checkout | pass на Linux |

CI для commit `809356434742dea86a14bb7ae97908a080f21c1b`: https://github.com/mejustbox-byte/detection-engineering-toolkit/actions/runs/37943840949 . Исправление UTF-8 дополнительно прошло в предыдущем run: https://github.com/mejustbox-byte/detection-engineering-toolkit/actions/runs/37943677116 .

Первый Windows run выявил чтение UTF-8 JSON через системную cp1252 кодировку в тесте. Чтение файлов теперь явно использует UTF-8; CLI также устанавливает UTF-8 для stdout/stderr. Regression test проверяет CLI в процессе с исходной cp1252 pipe encoding.

## Воспроизведение

```bash
uv sync --frozen --extra dev
uv run --frozen --extra dev pytest -q
uv run --frozen --extra dev ruff check .
uv run --frozen --extra dev ruff format --check .
uv build
uv run --frozen detkit bundle T1033 --output output/demo
```

## Непроверенные области

Реальные upstream Atomic procedures, Windows endpoint telemetry, SIEM query execution, ingestion latency, macOS runtime, CVE audit и публикация release: **not_run**. Успех Windows CI подтверждает offline Python-пакет, а не лабораторное обнаружение.

Тестовая Atomic запись собственная синтетическая. Она проверяет контракт parser/plan, а не совместимость выбранной upstream procedure. Для реального доказательства нужен протокол [LOCAL-PC.md](LOCAL-PC.md).
