# Выпуск

Текущая версия 0.1.0a1 подготовлена локально и не опубликована. Первый выпуск должен быть prerelease: полная лабораторная цепочка не проверена.

Порядок: документация и tests → PR → удалённый CI точного HEAD → review → разрешённое merge → checkout итогового commit → чистая сборка → tag → prerelease с assets → скачивание и сравнение SHA256. Существующие tags не перемещаются.

Артефакты: wheel, sdist, полный source archive с uv.lock/документами/scripts/workflow, SHA256SUMS. Стандартный sdist сам по себе может не включать CI; MANIFEST.in специально добавляет документы и setup scripts.

```bash
uv sync --frozen --extra dev
uv run --frozen --extra dev pytest -q
uv run --frozen --extra dev ruff check .
uv build
```

CVE-аудит и real lab checks имеют отдельные статусы и не заменяются синтетикой. Prerelease notes явно перечисляют not_run. Выпуск стабильной версии требует критериев из REQUIREMENTS и LOCAL-PC.

