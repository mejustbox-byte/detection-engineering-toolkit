# Источники и происхождение

Официальные источники для проверяемых контрактов:

- MITRE ATT&CK: https://attack.mitre.org/techniques/T1033/ , https://attack.mitre.org/techniques/T1082/ , https://attack.mitre.org/techniques/T1016/ , https://attack.mitre.org/techniques/T1057/ . Каталог содержит собственные компактные сопоставления, а не полный STIX dataset.
- pySigma: https://github.com/SigmaHQ/pySigma . Правила валидируются реальным parser, backends отдельно.
- Splunk backend: https://github.com/SigmaHQ/pySigma-backend-splunk . Используется splunk_windows pipeline.
- Defender backend: https://github.com/SigmaHQ/pySigma-backend-microsoft365defender . Установленный 0.3.2 экспортирует KustoBackend и microsoft_365_defender_pipeline.
- Pipelines: https://sigmahq.io/docs/digging-deeper/pipelines . Mapping проверяется на реальной телеметрии.
- Atomic definitions: https://github.com/redcanaryco/atomic-red-team . Upstream YAML не включён в архив; оператор выбирает pinned checkout.
- Invoke module и локальный запуск: https://github.com/redcanaryco/invoke-atomicredteam/wiki/Execute-Atomic-Tests-%28Local%29 . План использует TestGuids, ShowDetails, CheckPrereqs и Cleanup.

Дата сверки интерфейсов: 2026-10-09. Версии Python backend API дополнительно проверены установленными пакетами и тестами. Полные внешние описания и команды не копируются. Synthetic Atomic test в тестах собственный и не выдаётся за upstream.

Перед включением сторонних правил/каталогов нужны license review и сохранение provenance. Текущий проект не присваивает авторство правилам SigmaHQ; генерируемые шаблоны собственные.
