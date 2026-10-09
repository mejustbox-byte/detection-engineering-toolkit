# Облачная разработка

## Назначение

Имя среды: `detection-engineering-toolkit`. Публичный GitHub repository: `mejustbox-byte/detection-engineering-toolkit`. Репозиторий создан 2026-10-09; public visibility и права записи подтверждены. Публикация среды проверяется отдельно.

Локально в текущей рабочей среде подготовлен CPython 3.12.15, uv.lock и свежий venv. Это не публикация облачной среды в настройках ChatGPT.

## Установка из checkout

install_script должен исполняться из корня фактического checkout:

```bash
set -euo pipefail
uv sync --frozen --extra dev
uv run --frozen --extra dev pytest -q
uv run --frozen --extra dev ruff check .
uv run --frozen detkit list
```

Не используйте пути предыдущих сессий или `/workspace/onboarding`. Python 3.12.15 и uv 0.12.23 обеспечиваются базовым образом/официальным установщиком. При установке требуется PyPI; runtime offline. Credentials для SIEM/Atomic отсутствуют.

## Инструкция запуска работы

«Работай в актуальном checkout detection-engineering-toolkit. Сначала прочитай README, REQUIREMENTS, THREAT-MODEL, CORE-CONTRACT и VERIFICATION. Реализуй согласованные сценарии, обнови русские документы, проверь frozen install, pytest, lint, сборку и wheel вне checkout. Не запускай Atomic автоматически. Реальные SIEM/Windows проверки отдельно; synthetic pass их не заменяет. Используй штатное GitHub подключение; не извлекай credentials. До публикации результатов проверь точный commit и удалённый CI».

## Публикация и восстановление

Перед публикацией среды: подтвердить repo ID/branch, сохранившиеся install/start инструкции, сетевые зависимости без секретов и успешное восстановление в новой задаче. После публикации открыть среду заново и проверить checkout/commit. Существующий venv не является доказательством воспроизводимости.

Удалённый CI и публикация среды отмечаются отдельно в VERIFICATION. Пока подготовленный workflow не запускался на GitHub. Среда не должна ждать ветку другого проекта GITHUB-OPSEC.
