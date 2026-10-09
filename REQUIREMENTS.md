# Требования

## Пользователи и результат

Detection engineer создаёт и ревьюит правило, SOC проверяет поля SIEM и false positives, purple team связывает сценарий с одним Atomic GUID. Результат — переносимый пакет артефактов с проверяемой целостностью и явно указанным уровнем доказательств.

## Функциональные требования

| Возможность | Критерий готовности |
|---|---|
| Каталог | Четыре конкретных Windows Discovery сценария; неизвестный ID отклоняется |
| Генерация | Корректный Sigma YAML, стабильный UUID, ATT&CK reference и experimental status |
| Конвертация | SPL/KQL через pySigma; новый объект правил для каждого backend |
| Внешнее правило | Локальный UTF-8 YAML конвертируется либо возвращает явную ошибку |
| Offline случаи | Positive/negative примеры, строгие типы, код 1 при несовпадении |
| Atomic | Техника/GUID/Windows проверены; snapshot hash, cleanup, optional source SHA |
| Экспорт | Новый каталог, семь артефактов, manifest, без перезаписи |
| Integrity | Обнаружение изменения, отсутствия/лишних файлов; traversal отвергается |
| Readiness | doctor конвертирует каждый сценарий обоими backend |

## Нефункциональные требования

Runtime без сети, credentials и shell execution. UTF-8 на Windows/Linux. Входы до 8 MiB; YAML safe_load. Frozen source install. Документация RU/EN с одинаковым контрактом. CI проверяет оба OS и установку wheel вне checkout. Нет production или полного ATT&CK coverage claim.

## За границами 0.1.0a2

Полный STIX каталог, автоматическое выполнение Atomic, доставка событий, SIEM API, correlation rules, tuning по реальной статистике и криптографическая подпись bundles. Эти функции требуют отдельного проектирования и доказательств.
