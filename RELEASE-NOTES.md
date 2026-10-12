# Detection Engineering Toolkit 0.1.0a3 — Detection Readiness

## Русский

Detection Readiness расширяет существующий toolkit: три цепочки риск/telemetry/правило/тест для T1033, T1082 и T1016. Добавлены строгий readiness-1.0 JSON, четыре контроля, opsec-1.0 assessment и отдельный каталог цепочек. Генерация Sigma, конвертация Splunk/Defender и проверка предиката используют прежние API.

Локально прошли 55 теста (включая прежние 31), Ruff и чистая установка wheel с doctor/bundle/readiness/валидацией assessment. Добавлены 11 пар RU/EN readiness-документов. Hosted CI 38243279691 прошёл Linux, Windows и macOS на 25149ae4b32c3dcdb84d2ec94c3076640560cb41: 55 тестов и чистая установка.

Синтетический пример сохраняет delivery not_run и возвращает код 2. DET-004 проверяет только согласованность предоставленного заявления: ID исполнения, время и хеш правила; provenance всегда user_supplied_unverified. Предикат не исполняет Sigma, SIEM или Atomic. Реальные Windows VM/SIEM/Atomic и dependency/CVE audit не выполнены. Alpha не готова для production.

## English

Detection Readiness extends the existing toolkit with three risk/telemetry/rule/test chains for T1033, T1082 and T1016. Adds strict readiness-1.0 JSON, four checks, an opsec-1.0 assessment and separate chain catalog. Sigma generation, Splunk/Defender conversion and predicate validation reuse the existing APIs.

Local verification passed 55 tests (including the existing 31), Ruff and clean wheel installation with doctor/bundle/readiness/assessment validation. Eleven RU/EN readiness documentation pairs were added. Hosted CI 38243279691 passed Linux, Windows and macOS on 25149ae4b32c3dcdb84d2ec94c3076640560cb41: 55 tests and clean installation.

The synthetic example retains delivery not_run and returns code 2. DET-004 checks only consistency of a supplied assertion: execution ID, time and rule hash; provenance is always user_supplied_unverified. Predicate testing does not execute Sigma, SIEM or Atomic. Real Windows VM/SIEM/Atomic and dependency/CVE auditing were not performed. This alpha is not production-ready.
