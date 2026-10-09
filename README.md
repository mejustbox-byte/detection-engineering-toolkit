# Detection Engineering Toolkit

Инструмент detection engineering: воспроизводимая цепочка ATT&CK → наблюдаемый сценарий → Sigma → запрос SIEM → план Atomic Red Team → доказательства проверки.

Версия разработки **0.1.0a1**. Реализован offline CLI; публичный репозиторий создан: https://github.com/mejustbox-byte/detection-engineering-toolkit . Удалённый CI и публикация Cloud-среды пока ожидают проверки. Реальные Atomic/SIEM-проверки **НЕ ВЫПОЛНЕНЫ**.

## Что работает

| ATT&CK | Сценарий | Условие | Телеметрия |
|---|---|---|---|
| T1033 | whoami | Image оканчивается на `\whoami.exe` | Windows process_creation |
| T1082 | hostname | Image оканчивается на `\hostname.exe` | Windows process_creation |
| T1016 | ipconfig | Image оканчивается на `\ipconfig.exe`, CommandLine содержит `/all` | Windows process_creation |
| T1057 | tasklist | Image оканчивается на `\tasklist.exe` | Windows process_creation |

Правила собственные, детерминированные и experimental. Генератор использует явные шаблоны наблюдаемого поведения. ID техники сам по себе не определяет универсальную детекцию. Правила discovery имеют низкую критичность и ожидаемые ложные срабатывания при администрировании.

Конвертация выполняется pySigma: Splunk SPL с `splunk_windows` и Defender KQL с `microsoft_365_defender_pipeline`. Backend Defender возвращает запрос к DeviceProcessEvents. Это не адаптер Microsoft Sentinel.

## Быстрый старт

Установите Python 3.12.15 и uv 0.12.23 из официальных источников, распакуйте исходники, перейдите в каталог:

```bash
uv sync --frozen --extra dev
uv run --frozen detkit list
uv run --frozen detkit bundle T1033 --output output/whoami
uv run --frozen detkit validate T1033 --cases output/whoami/fixtures.json
```

В каталоге появятся `rule.yml`, `splunk.txt`, `defender.txt`, синтетические события, отчёт, Atomic-план и manifest SHA256. Каталог назначения должен отсутствовать. Инструмент ничего не исполняет на узлах и не подключается к SIEM.

## Документация

- [Требования](REQUIREMENTS.md), [архитектура](ARCHITECTURE.md), [стек](TECH-STACK.md), [ADR](docs/adr/0001-deterministic-offline.md).
- [Модель угроз](THREAT-MODEL.md), [безопасность](SECURITY.md), [контракт CLI](CORE-CONTRACT.md).
- [Установка](INSTALL.md), [разработка](CONTRIBUTING.md), [эксплуатация](RUNBOOK.md), [Cloud](CLOUD-DEVELOPMENT.md).
- [Локальный стенд](LOCAL-PC.md), [матрица проверок](VALIDATION.md), [фактические проверки](VERIFICATION.md).
- [План развития](ROADMAP.md), [выпуск](RELEASE.md), [чеклист](RELEASE-CHECKLIST.md), [заметки](RELEASE-NOTES.md), [изменения](CHANGELOG.md).
- [Источники и происхождение](SOURCES.md), [демонстрационный сценарий](DEMO.md).

## Ограничения

Нет LLM-генерации произвольных правил, импорта полного ATT&CK STIX, автоматического запуска Atomic, SIEM API, измерения задержки доставки и проверки реальной полноты обнаружения. Обрабатываются только четыре перечисленных сценария. Инструмент отказывает неизвестным техникам. Atomic YAML выбирается локально оператором; выбор теста по GUID не доказывает соответствие правилу.
