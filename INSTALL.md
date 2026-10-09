# Установка и удаление

## Из исходников

Требуются Python 3.12.15, uv 0.12.23 и доступ к PyPI при первой установке. Получите официальные installers; исходники распакуйте в отдельный каталог.

POSIX:

```bash
cd detection-engineering-toolkit
bash scripts/setup.sh
uv run --frozen detkit --version
uv run --frozen detkit bundle T1033 --output output/demo
```

Windows PowerShell:

```powershell
Set-Location detection-engineering-toolkit
.\scripts\setup.ps1
uv run --frozen detkit --version
uv run --frozen detkit bundle T1033 --output output/demo
```

При локальной политике запрета PowerShell scripts выполните строки из setup.ps1 вручную в согласованной оболочке; не отключайте защитную политику. На macOS Intel CLI может работать через установленный CPython; запуск Windows Atomic требует отдельной Windows VM. macOS здесь не тестировалась.

## Из wheel

После проверки SHA256:

```bash
uv venv .wheel-venv --python 3.12.15
uv pip install --python .wheel-venv/bin/python dist/detection_engineering_toolkit-0.1.0a1-py3-none-any.whl
.wheel-venv/bin/detkit list
```

На Windows замените путь Python на `.wheel-venv\Scripts\python.exe`, CLI — `.wheel-venv\Scripts\detkit.exe`. Установка одного wheel разрешает зависимости по прямым pins; для точного транзитивного окружения используйте исходники и `uv sync --frozen`.

## Проверка

`detkit --version` показывает 0.1.0a1; bundle создаёт новую папку и validation с not_run для SIEM. Уже существующий output вызывает отказ. См. [RUNBOOK.md](RUNBOOK.md) для ошибок.

## Удаление

Удалите только созданный для проекта venv и каталог исходников после сохранения нужных отчётов. Пакеты глобального Python не меняются при uv sync. Отчёты могут содержать внутренние данные; порядок хранения/удаления определяется владельцем. Atomic-модуль устанавливается независимо и этим инструментом не удаляется.
