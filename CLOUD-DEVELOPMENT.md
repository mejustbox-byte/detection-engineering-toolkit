# Облачная среда разработки

## Конфигурация

Репозиторий: https://github.com/mejustbox-byte/detection-engineering-toolkit .
Ветка по умолчанию: `main`. Имя среды: `detection-engineering-toolkit`.
Runtime: CPython 3.12.15 и uv 0.12.23. Зависимости закреплены в uv.lock.

Среда предназначена для разработки offline CLI, синтетических тестов и упаковки. Реальные Windows/Atomic/SIEM проверки выполняются на отдельном стенде по [LOCAL-PC.md](LOCAL-PC.md).

## Установка из checkout

Рабочий каталог — корень репозитория. При первоначальной установке нужен доступ к официальным Python/uv источникам и PyPI. При запуске продукт не требует сети или credentials.

```bash
set -euo pipefail
uv sync --frozen --extra dev
uv run --frozen --extra dev pytest -q
uv run --frozen --extra dev ruff check .
uv run --frozen --extra dev ruff format --check .
uv run --frozen detkit list
```

## Рабочий цикл

Перед изменениями изучите REQUIREMENTS, THREAT-MODEL и CORE-CONTRACT. Выполните тесты и оба backend regression checks. После изменений обновите документацию, соберите wheel/sdist и проверьте wheel вне checkout.

Команды и пути должны разрешаться относительно текущего checkout. Сохранённый venv не заменяет чистую установку. Не сохраняйте реальные журналы и credentials в репозитории. Atomic-планы остаются данными; автоматический запуск отсутствует.

## Проверка сохранённой конфигурации

После публикации среды откройте её повторно, проверьте привязку репозитория и воспроизведите frozen install в новой задаче. Установка и стартовые инструкции должны соответствовать текущим scripts/setup.sh и CONTRIBUTING.md.

Удалённый CI проверяется для точного commit отдельно от установки среды. Фактические результаты и ограничения перечислены в [VERIFICATION.md](VERIFICATION.md).
