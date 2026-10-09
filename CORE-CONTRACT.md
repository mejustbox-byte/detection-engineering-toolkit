# Контракт продукта

## Сценарий → правило

Техника выбирается по ID `Tdddd` или `Tdddd.ddd`. Генерация поддерживает только четыре записи встроенного каталога. UUID зависит от scenario ID и namespace v1, не от момента запуска. Правило проверяет `Image|endswith`; для T1016 дополнительно применяется `CommandLine|contains|all: ['/all']`. Это поиск подстроки, не разбор аргументов: `/alligator` тоже содержит `/all`.

## Конвертация

Для каждого вызова создаётся новая `SigmaCollection`: pipeline может изменять правила. Splunk использует `splunk_windows_pipeline`, Defender — `microsoft_365_defender_pipeline`. `convert-file` принимает внешний YAML с одним или несколькими поддерживаемыми backend правилами. Произвольный logsource, correlation и каждый модификатор Sigma не гарантируются; ошибка конвертации возвращает код 2. Pipeline и конфигурация SIEM не настраиваются через CLI этой версии.

## Размеченные случаи

```json
[
  {"id":"positive","expected":true,"event":{"Image":"C:\\Windows\\System32\\whoami.exe","CommandLine":"whoami"}},
  {"id":"negative","expected":false,"event":{"Image":"C:\\Windows\\System32\\notepad.exe"}}
]
```

`id` — уникальная строка, `expected` — boolean, `event` — объект. Присутствующие `Image` и `CommandLine` должны быть строками. Отсутствующий Image означает отсутствие совпадения. `casefold` применяется к строковым suffix/substring проверкам. Поля времени, parent process, user и host не оцениваются. `validate` не принимает внешнее Sigma-правило и не доказывает равенство семантики backend.

## Входы и пакеты

UTF-8 JSON/YAML, максимум 8 MiB на прочитанный файл. YAML обрабатывается `safe_load`; Atomic metadata должно быть JSON-совместимым и без циклов. Это ограничение размера, не sandbox или полная защита от exhaustion.

Пакет содержит семь артефактов и manifest. Schema version 1 добавляет версию продукта. Проверка принимает также старый manifest 0.1.0a1 без schema_version. Точный список файлов обязателен; digest — 64 lowercase hex символа. Manifest сам не хешируется и не подписан; изменение файла вместе с manifest может остаться незамеченным. Symlink файлов отвергается, но проверка не защищена от конкурентной модификации локальным процессом.

## Atomic

Техника YAML, GUID и Windows platform проверяются. Хеш считается по тому же снимку, который разбирался. `source_commit` не проверяется через Git или сеть. Команды — данные; test behavior, зависимости и cleanup требуют ручного ревью. `--lab-ack` не является исполнителем.
