# Методика проверки

## Уровни доказательств

| Уровень | Что подтверждает | Что не подтверждает |
|---|---|---|
| Sigma parse | Структура правила принимается pySigma | Качество сигнала |
| Backend conversion | Из выбранной модели получается SPL/KQL | Работу запроса в конкретном SIEM |
| Offline predicate | Suffix/substring поведение на размеченных случаях | Исполнение Sigma, запросов или эквивалентность всех backend |
| Bundle integrity | Совпадение байтов и manifest | Подлинность, безопасность, full coverage |
| Real lab | Факт execution, доставки события, query match и cleanup | Универсальность во всех окружениях |

## Автоматический цикл

```bash
uv sync --frozen --extra dev
uv run --frozen --extra dev pytest -q
uv run --frozen --extra dev ruff check .
uv run --frozen --extra dev ruff format --check .
uv run --frozen detkit doctor
uv build
```

CI Windows/Linux дополнительно строит bundle, проверяет manifest и устанавливает wheel в отдельный venv вне checkout. Тесты проверяют каждый сценарий/оба backend, некорректные входы, Atomic GUID и snapshot provenance, legacy pipe UTF-8, external Sigma, modified/missing/extra artifacts и traversal.

## Регрессия

При изменении rule, dependency или pipeline сравните запросы и ручной контракт. Добавляйте негативный случай, соответствующий причине исправления. Не назначайте unknown событию expected=false автоматически: разметка должна быть обоснованной. Реальную телеметрию обезличивайте до публикации.

Состояние проверок: [VERIFICATION.md](VERIFICATION.md). Протокол стенда: [LOCAL-PC.md](LOCAL-PC.md).
