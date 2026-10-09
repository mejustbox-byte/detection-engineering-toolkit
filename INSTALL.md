# Установка

## Из исходников

Поддерживаемый runtime: CPython 3.12+. CI использует Python 3.12 на Windows и Linux; полная проверка macOS пока не выполнена. `uv.lock` закрепляет зависимости; версия uv для воспроизведения — 0.12.23. `.python-version` задаёт 3.12.15.

```bash
git clone https://github.com/mejustbox-byte/detection-engineering-toolkit.git
cd detection-engineering-toolkit
uv sync --frozen --extra dev
uv run --frozen detkit --version
uv run --frozen detkit doctor
uv run --frozen --extra dev pytest -q
```

Linux/macOS: `bash scripts/setup.sh`. Windows PowerShell: `./scripts/setup.ps1`. Перед запуском просмотрите скрипт. Он устанавливает зависимости и выполняет offline проверки.

## Из wheel

Скачайте wheel и `SHA256SUMS` из одного GitHub Release. Сверьте SHA256 до установки. Создайте отдельный venv:

```bash
python -m venv .venv
# Linux/macOS
.venv/bin/python -m pip install detection_engineering_toolkit-0.1.0a2-py3-none-any.whl
.venv/bin/detkit doctor
```

Windows: замените пути на `.venv/Scripts/python.exe` и `.venv/Scripts/detkit.exe`. Wheel содержит код и встроенный каталог; полная документация и lock доступны в исходном ZIP/sdist. Установка wheel разрешает версии транзитивных зависимостей через pip; для точного frozen окружения используйте source + `uv.lock`.

## Типичные проблемы

- `uv` не найден: установите официальный uv указанной версии, затем откройте новую оболочку.
- `No module named detection_toolkit`: работайте через `uv run --frozen` или активируйте venv, куда установлен wheel.
- Каталог output уже существует: выберите новый путь; экспорт специально запрещает перезапись.
- Конвертация отклонена: проверьте Sigma logsource и возможности выбранного backend.
- Интернет нужен при первой установке; после установки CLI использует только локальные входы.

Далее: [RUNBOOK.md](RUNBOOK.md) и [DEMO.md](DEMO.md).
