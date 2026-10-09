# Состояние проверок

## 0.1.0a2

Локальный Linux цикл: 31 тест, Ruff lint/format, doctor, внешняя Sigma конвертация и проверка ссылок — pass. Чистая установка wheel вне checkout: doctor и четыре bundle/integrity процесса — pass.

[CI для реализации 0.1.0a2](https://github.com/mejustbox-byte/detection-engineering-toolkit/actions/runs/37956459675) прошёл на Windows и Linux для commit `591dbdbd656f5143933c8397f517dbe5b9cb40d5`: по 31 тесту, lint/format, doctor, build, bundle/integrity и wheel install вне checkout. Для финального merge commit и release проверяйте отдельные запуски Actions; результат другого SHA не заменяет эту проверку.

## Опубликованная базовая версия 0.1.0a1

- Merge commit: `5e7800fb8c042bdc171d7b5aa8ed810a63673fa6`.
- [CI Linux/Windows](https://github.com/mejustbox-byte/detection-engineering-toolkit/actions/runs/37953235395): успешно, по 20 тестов, lint, build и bundle smoke.
- [Release workflow](https://github.com/mejustbox-byte/detection-engineering-toolkit/actions/runs/37953436439): успешно, wheel install вне checkout и проверка скачанных SHA256.
- [Prerelease](https://github.com/mejustbox-byte/detection-engineering-toolkit/releases/tag/v0.1.0a1): wheel, sdist, source ZIP, notes и SHA256SUMS.

## Не выполнено

Реальные Windows VM тесты с upstream Atomic; доставка и match в Splunk/Defender; cleanup реального теста; полная проверка macOS; full dependency/CVE audit. Соответствующие результаты остаются `not_run`, даже при зелёном offline CI.

Разделение уровней описано в [VALIDATION.md](VALIDATION.md). Лабораторные свидетельства должны содержать версии, UTC время и результат каждого этапа.
