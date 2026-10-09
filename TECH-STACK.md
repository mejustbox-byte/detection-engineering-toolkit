# Технологический стек

| Компонент | Версия | Причина |
|---|---|---|
| Python | 3.12.15 для разработки | Проверенный runtime, доступные пакеты Windows/Linux |
| uv | 0.12.23 | Lock и чистое воспроизведение окружения |
| pySigma | 1.5.1 | Разбор реального Sigma и интеграция backends |
| Splunk backend | 2.1.0 | SPL и splunk_windows pipeline |
| Microsoft365Defender backend | 0.3.2 | KQL с Defender pipeline; транзитивный Kusto backend |
| PyYAML | 6.0.3 | safe_load локального Atomic YAML |
| pytest | 9.1.1 | Unit/integration проверки ошибок и конвертации |
| ruff | 0.16.10 | Статические проверки и форматирование |
| build | 1.6.1 | Разработка упаковки; основная сборка uv build |
| setuptools | 80.9.0 | Закреплённый build backend |

Прямые зависимости закреплены в pyproject.toml, транзитивные и хеши — в uv.lock. `.python-version` задаёт 3.12.15. Метаданные wheel допускают Python >=3.12, но остальные версии не подтверждены тестами.

Почему не собственный Sigma-to-SIEM transpiler: поддержка escaping, modifiers и logsource требует специализированных backend. Почему без LLM: первая версия должна быть воспроизводимой и проверяемой; генерация по одному ID не может вывести требования к данным и универсальную детекцию.

Почему CLI: минимальная поверхность атаки и отсутствие credentials. Web UI, API SIEM и удалённая эмуляция появятся только после отдельного ADR. Текущий pipeline Defender — не Sentinel; перенос KQL между ними требует отдельного backend и проверки таблиц.
