# Detection Engineering Toolkit

**От техники ATT&CK к проверяемому пакету детекции.**

[English](README.md) · [Документация](docs/ru/INDEX.md) · [CLI](RUNBOOK.md) · [Лаборатория](LOCAL-PC.md)

Detection Engineering Toolkit — локальный CLI для detection engineers, SOC и purple team. Он связывает конкретный сценарий ATT&CK, экспериментальное Sigma-правило, запросы Splunk SPL и Microsoft Defender KQL, синтетические проверки и план выбранного теста Atomic Red Team. Один пакет сохраняет результат и контрольные суммы для ревью и повторной проверки.

## Практическая ценность

- **Воспроизводимость:** закреплённые зависимости, стабильные UUID правил и одинаковые артефакты при одинаковых входах в той же версии.
- **Переносимость детекций:** настоящие pySigma backend и processing pipeline для двух систем.
- **Контроль качества:** `doctor` проверяет установленный инструмент, `validate` — ожидаемое поведение сценария, `verify-bundle` — целостность пакета.
- **Работа с собственными правилами:** `convert-file` конвертирует локальный Sigma YAML; каталог встроенных сценариев не ограничивает эту команду.
- **Связь Red/Blue:** Atomic-план выбирает один GUID, сохраняет SHA256 YAML, prerequisites и cleanup; выполнение остаётся отдельным лабораторным этапом.
- **Открытая проверяемость:** код, тесты, документация RU/EN и CI Windows/Linux. Runtime не обращается к сети и не исполняет команды эмуляции.

## Быстрый старт

Требуются Python 3.12+ и uv 0.12.23. Первичная установка зависимостей использует сеть.

```bash
git clone https://github.com/mejustbox-byte/detection-engineering-toolkit.git
cd detection-engineering-toolkit
uv sync --frozen --extra dev
uv run --frozen detkit doctor
uv run --frozen detkit bundle T1033 --output output/whoami
uv run --frozen detkit verify-bundle output/whoami
uv run --frozen detkit validate T1033 --cases output/whoami/fixtures.json
```

## Поддерживаемые сценарии

| ATT&CK | Наблюдаемое поведение | Источник событий |
|---|---|---|
| T1033 | Запуск `whoami.exe` | Windows process creation |
| T1082 | Запуск `hostname.exe` | Windows process creation |
| T1016 | Запуск `ipconfig.exe` с подстрокой `/all` | Windows process creation |
| T1057 | Запуск `tasklist.exe` | Windows process creation |

Один сценарий не покрывает всю технику. Эти утилиты часто используются легитимно; правила имеют уровень `low` и статус `experimental`.

## Что находится в пакете

`rule.yml`, `splunk.txt`, `defender.txt`, `fixtures.json`, `validation.json`, `atomic-plan.json`, двуязычный `REPORT.md` и `manifest.json`. Manifest содержит SHA256 остальных семи файлов. Новый экспорт не перезаписывает существующий каталог.

```bash
uv run --frozen detkit rule T1016
uv run --frozen detkit convert T1016 --target splunk
uv run --frozen detkit convert-file output/whoami/rule.yml --target defender
```

## Состояние продукта

Версия **0.1.0a2**, prerelease. Offline CLI реализован и покрыт тестами. Проверка предиката не исполняет Sigma или SIEM-запрос. Конвертация не доказывает корректную доставку событий или обнаружение в конкретном SIEM. Реальные Windows VM, upstream Atomic и SIEM проверки пока **не выполнены**. Протокол воспроизведения: [LOCAL-PC.md](LOCAL-PC.md).

Инструмент разработан для практики detection engineering в 2026 году: воспроизводимые артефакты, проверяемое происхождение входов и чёткое разделение результатов. Независимый рейтинг, лидерство на рынке и production-ready статус не заявляются.

## Следующие шаги

[Установка](INSTALL.md) · [Пример полного процесса](DEMO.md) · [Контракт](CORE-CONTRACT.md) · [Модель угроз](THREAT-MODEL.md) · [Безопасность](SECURITY.md) · [Результаты проверок](VERIFICATION.md) · [План развития](ROADMAP.md)
