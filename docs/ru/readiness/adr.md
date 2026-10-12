# ADR: расширить существующие API

Используются существующий Python 3.12 toolkit, pySigma backends и frozen uv workflow. Добавляется точный report-contract 0.1.0a1 через выпущенный wheel с опубликованным SHA-256. Общие загрузка и статусы исключают конкурирующую модель отчёта. Обновление зависимости записано в uv.lock.

Новый интерпретатор Sigma исключён. Предикат остаётся явно offline_scenario_predicate; разбор/конвертация Sigma и доставка SIEM — разные свидетельства. CI добавляет macOS к Linux/Windows и проверяет прежние команды, readiness, документы и ресурсы установленного wheel.

[Index](index.md)
