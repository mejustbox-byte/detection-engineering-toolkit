# Разработка и review

Вся документация и пользовательские описания — на русском. Идентификаторы, команды, upstream названия и ключи схем не переводятся. Не добавляйте реальные журналы, секреты и credentials.

```bash
uv sync --frozen --extra dev
uv run --frozen --extra dev pytest -q
uv run --frozen --extra dev ruff check .
uv run --frozen --extra dev ruff format --check .
uv build
```

Изменение проходит отдельную ветку и PR. Reviewer проверяет telemetry assumptions, ATT&CK tags, ложные срабатывания, escape в обоих запросах, реальное происхождение Atomic GUID и границы доказательств. Тесты включают негативный вход и regression backend, а не только совпадение собственной реализации.

Нельзя вносить subprocess runner в core без отдельного ADR, модели разрешений, изоляции и rollback. Не расширяйте правило до «вся техника обнаружена» без измеряемого стенда.

При обновлении зависимостей измените pins и выполните `uv lock`, затем чистую установку и обе платформы CI. Lock и pyproject меняются вместе. Не изменяйте существующие release tags. Результаты удалённого CI должны относиться к точному HEAD.
