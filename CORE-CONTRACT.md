# Контракт CLI и данных

## Команды

| Команда | Результат |
|---|---|
| `detkit list` | JSON-каталог поддерживаемых сценариев |
| `detkit rule T1033` | Sigma YAML в stdout |
| `detkit convert T1033 --target splunk` | SPL в stdout |
| `detkit convert T1033 --target defender` | KQL в stdout |
| `detkit validate T1033 --cases cases.json` | JSON результата offline предиката |
| `detkit atomic-list T1033 --atomic-file T1033.yaml` | Список GUID, платформ и исходных команд |
| `detkit atomic-plan T1033 --atomic-file T1033.yaml --test-guid GUID` | План деталей/предпосылок/cleanup |
| `detkit bundle T1033 --output output/demo` | Новый каталог пакета |

`atomic-plan` и `bundle` допускают `--lab-ack`, чтобы добавить команду execute. Для bundle `--atomic-file` и `--test-guid` задаются вместе. Неизвестные техники отказываются; поддерживается один сценарий на технику. Код 0 — успешный offline результат/генерация, 1 — хотя бы один случай не совпал с expected, 2 — ошибка ввода/IO/конвертации. Ошибки argparse также имеют код 2.

## Нормализованные случаи

```json
[{"id":"positive","expected":true,"event":{"Image":"C:\Windows\System32\whoami.exe","CommandLine":"whoami"}}]
```

Корень — непустой массив. id — уникальная строка; expected — JSON boolean; event — объект. Если Image или CommandLine присутствуют, они строки. Отсутствующее Image не совпадает; отсутствие CommandLine не совпадает, если правило требует его. Неиспользуемые дополнительные поля игнорируются. Сравнение suffix/contains регистронезависимое (`casefold`); tokenizer не используется. Поэтому `/alligator` также содержит `/all`: это ограничение экспериментального правила.

## Отчёт и пакет

Validation содержит scope `offline_scenario_predicate`, passed, cases с actual/expected/pass и `siem_execution=not_run`, `atomic_execution=not_run`. Эти статусы не меняются от успеха генерации. Atomic план содержит SHA256 YAML, GUID, исходную команду и review-only статусы. При отсутствии Atomic входа план содержит причину not_run.

Manifest содержит version, technique, scenario и mapping имя файла → SHA256. Он не является цифровой подписью и не подтверждает происхождение пакета.

## Расширение

Добавьте запись сценария, review ATT&CK-сопоставления и telemetry prerequisites, положительные и пограничные негативные тесты, оба backend и лабораторный протокол. Если сценариев на технику станет несколько, CLI обязан добавить явный selector; текущий resolver отказывает неоднозначным данным. Версионирование семантики UUID обновляется осознанно.
