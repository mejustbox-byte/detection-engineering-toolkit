# Detection Engineering Toolkit 0.1.0a4 — Windows laboratory preparation

## Русский

Добавлен лабораторный сборщик четырёх процессов и событий Windows Security 4688, строгий windows-lab-1.0 импорт и единый lab-check. Признак synthetic обязателен и сохраняется при оценке; SIEM delivery всегда not_run. Исправлена запись UTF-8 без BOM для PowerShell 5.1. Дублирующиеся PID/ID записей, несогласованные события и заявления о SIEM-доставке отклоняются. Реальные данные оператора не считаются независимо подтверждёнными.

Linux / Python 3.12.15: 74 теста, Ruff, сборка, чистая установка wheel и проверки документации. Добавлены две пары RU/EN руководств со сбором, откатом политик, приватностью и шаблоном кейса до/после. Windows CI разбирает только синтаксис сборщика. Результат hosted CI для конкретного commit проверяется в Actions.

Реальный сбор Windows, доставка/совпадения SIEM, исполнение Sigma/Atomic и CVE-аудит зависимостей не выполнены. Синтетический пример даёт 9 pass / 3 not_tested и код 2. Автоматической настройки политик, загрузки в SIEM или доказательства подлинности здесь нет. Alpha не готова для production.

## English

Adds a four-process Windows Security 4688 laboratory collector, strict windows-lab-1.0 import and unified lab-check. The required synthetic classification is preserved; SIEM delivery always remains not_run. Windows PowerShell 5.1 output uses UTF-8 without BOM. Duplicate PID/record IDs, inconsistent events and claimed SIEM delivery are rejected. Operator-supplied live data is not independently authenticated.

Linux / Python 3.12.15: 74 tests, Ruff, build, clean wheel installation and documentation checks. Two RU/EN guide pairs cover collection, policy rollback, privacy and a before/after case template. Windows CI only parses collector syntax. Consult Actions for hosted CI on the exact commit.

Real Windows collection, SIEM delivery/matching, Sigma/Atomic execution and dependency CVE auditing were not performed. The synthetic example returns 9 pass / 3 not_tested and exit 2. No automatic policy configuration, SIEM upload or authenticity proof is included. This alpha is not production-ready.
