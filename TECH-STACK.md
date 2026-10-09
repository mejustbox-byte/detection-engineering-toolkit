# Технологический стек

| Компонент | Закреплённая версия | Роль |
|---|---|---|
| Python | source pin 3.12.15 | Локальный CLI, типы, cross-platform |
| uv | 0.12.23 | Lock, frozen sync, build |
| pySigma | 1.5.1 | Парсинг и модель правил |
| Splunk backend | 2.1.0 | SPL и Windows pipeline |
| Defender backend | 0.3.2 | KustoBackend и M365 Defender pipeline |
| PyYAML | 6.0.3 | Safe YAML parse/serialization |
| pytest / Ruff | 9.1.1 / 0.16.10 | Regression и lint/format |
| setuptools | 80.9.0 | Wheel/sdist |

Python выбран для зрелой Sigma экосистемы и простой установки. Используются настоящие backend, а не собственная неполная реализация SPL/KQL. Собственный evaluator сознательно ограничен несколькими полями и не выдаётся за Sigma engine.

`uv.lock` закрепляет транзитивные версии. CI runtime Python 3.12 может получать patch updates; воспроизводимость пакетов оценивается с указанной версией Python и lock, а не побитовой воспроизводимостью wheel между разными ОС. Изменение зависимости требует полного regression цикла и пересмотра запросов.
