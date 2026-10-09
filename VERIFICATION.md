# Состояние проверок

## 0.1.0a2

На Linux в рабочем checkout выполнено 31 тест; все прошли. Ruff lint/format проверяются в CI. Новый CI должен подтвердить те же изменения на Windows и Linux и установку wheel вне checkout. Не считайте ожидаемый запуск уже пройденным: точный SHA и результат доступны в GitHub Actions и PR текущего изменения.

## Опубликованная базовая версия 0.1.0a1

- Merge commit: `5e7800fb8c042bdc171d7b5aa8ed810a63673fa6`.
- [CI Linux/Windows](https://github.com/mejustbox-byte/detection-engineering-toolkit/actions/runs/37953235395): успешно, по 20 тестов, lint, build и bundle smoke.
- [Release workflow](https://github.com/mejustbox-byte/detection-engineering-toolkit/actions/runs/37953436439): успешно, wheel install вне checkout и проверка скачанных SHA256.
- [Prerelease](https://github.com/mejustbox-byte/detection-engineering-toolkit/releases/tag/v0.1.0a1): wheel, sdist, source ZIP, notes и SHA256SUMS.

## Не выполнено

Реальные Windows VM тесты с upstream Atomic; доставка и match в Splunk/Defender; cleanup реального теста; полная проверка macOS; full dependency/CVE audit. Соответствующие результаты остаются `not_run`, даже при зелёном offline CI.

Разделение уровней описано в [VALIDATION.md](VALIDATION.md). Лабораторные свидетельства должны содержать версии, UTC время и результат каждого этапа.
