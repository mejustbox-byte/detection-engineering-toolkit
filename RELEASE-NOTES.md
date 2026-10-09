# Detection Engineering Toolkit 0.1.0a2

## Русский

Рабочие offline процессы и полная документация на двух языках.

- `doctor`: проверка установленного каталога, зависимостей и обоих backend.
- `convert-file`: конвертация локального внешнего Sigma YAML в Splunk SPL/Defender KQL.
- `verify-bundle`: проверка SHA256, отсутствующих/лишних файлов и allowlist manifest.
- Atomic: parse/hash одного снимка, сохранение cleanup, строгие типы metadata и optional upstream commit (непроверенный).
- Двуязычные README, технические документы, справочник CLI и лабораторный протокол; REPORT содержит русский и английский текст.
- 29 regression тестов; CI Windows/Linux дополнен wheel install вне checkout, doctor и integrity smoke.

Четыре встроенных Discovery сценария сохраняют статус experimental/low. Offline predicate не выполняет Sigma/SIEM. Real Windows VM, upstream Atomic, Splunk/Defender query validation, полный macOS цикл и dependency/CVE audit остаются not_run. Полный ATT&CK каталог, automatic runner и SIEM API отсутствуют. Выпуск — prerelease.


## English

Working offline workflows and complete documentation in two languages.

- `doctor` checks installed catalogue, dependencies and both backends.
- `convert-file` converts external local Sigma YAML into Splunk SPL/Defender KQL.
- `verify-bundle` checks SHA256, missing/extra files and the manifest allowlist.
- Atomic uses one parse/hash snapshot, retains cleanup, checks metadata types and records an optional upstream commit (unverified).
- Bilingual READMEs, technical documents, CLI reference and lab protocol; REPORT includes Russian and English text.
- 31 regression tests; Windows/Linux CI adds wheel installation outside checkout, doctor and integrity smoke.

The four built-in Discovery scenarios remain experimental/low. Offline predicates do not execute Sigma/SIEM. Real Windows VM, upstream Atomic, Splunk/Defender query validation, full macOS validation and dependency/CVE audit remain not_run. No full ATT&CK catalogue, automatic runner or SIEM API. This is a prerelease.
