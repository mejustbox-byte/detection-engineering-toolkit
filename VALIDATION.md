# Матрица проверок

| Область | Доступная проверка | Требуемая реальная проверка | Статус реальной |
|---|---|---|---|
| ATT&CK | Whitelist четырёх ID, отказ неизвестным | Экспертный review сопоставления наблюдаемого поведения | not_run |
| Sigma | Парсинг pySigma, стабильный UUID, tags | Review качества и false positives | not_run |
| Splunk | Backend conversion, ожидаемые поля и fragments | Выполнение SPL на доставленных Windows events | not_run |
| Defender | Kusto backend, DeviceProcessEvents и fragments | Выполнение KQL на onboarded endpoint | not_run |
| Atomic | GUID/platform/schema, show/execute gating | Конкретная upstream procedure в VM | not_run |
| Offline events | positive/negative/case/missing fields | Достоверность telemetry и ingestion | not_run |
| Packaging | frozen install, build, wheel smoke | Windows/macOS clean install | not_run |
| CI | Валидный подготовленный workflow | Удалённый exact-HEAD Linux/Windows Actions | not_run |

## Критерии

Offline tests обязаны отказывать повреждённому YAML, инъекции ID/GUID, неоднозначному/неподдерживаемому сценарию, неверному event type и перезаписи. Validation failure имеет exit code 1, input failure — 2.

Сценарный evaluator намеренно ограничен suffix/contains. Он не претендует на универсальную семантику Sigma и не подтверждает преобразованную SIEM семантику. При расширении modifiers требуется новый validator либо настоящий test backend с отдельным ADR.

В реальном стенде правило проходит только если positive raw event поступил и query возвратил ожидаемый result, а negative набор оценён на том же pipeline и time window. Общая техника не получает «covered» от одной процедуры. Неуспешная/недоступная проверка сохраняет fail/unknown/not_run.
