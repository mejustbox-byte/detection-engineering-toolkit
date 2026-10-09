# Справочник CLI

Команды выполняются в корне source checkout через `uv run --frozen detkit`; для wheel используйте `detkit` из venv. stdout — UTF-8, JSON для структурированных результатов, YAML для `rule`, текст запросов для `convert`/`convert-file`. Сообщения CLI могут быть на русском и английском; схема JSON одинакова.

| Команда | Назначение |
|---|---|
| `--version` | Версия установленного продукта |
| `list` | Четыре встроенных сценария |
| `doctor` | Версии зависимостей и конвертация всех сценариев двумя backend |
| `rule T1033` | Experimental Sigma для сценария |
| `convert T1033 --target splunk` | SPL; `defender` выдаёт KQL |
| `convert-file rule.yml --target defender` | Конвертация внешнего Sigma YAML |
| `bundle T1033 --output output/run-01` | Полный пакет, новый каталог |
| `verify-bundle output/run-01` | Проверка SHA256, отсутствующих и лишних файлов |
| `validate T1033 --cases cases.json` | Проверка предиката на размеченных событиях |
| `atomic-list T1033 --atomic-file T1033.yaml` | Список локальных тестов и GUID |
| `atomic-plan T1033 --atomic-file T1033.yaml --test-guid GUID` | План одного Windows теста |

## Примеры

```bash
uv run --frozen detkit bundle T1016 --output output/network-01
uv run --frozen detkit verify-bundle output/network-01
uv run --frozen detkit validate T1016 --cases output/network-01/fixtures.json
uv run --frozen detkit convert-file output/network-01/rule.yml --target splunk
```

Atomic-команды принимают **локальный** YAML и существующий GUID. `--atomic-commit` принимает полный 40-символьный SHA как непроверенное указание происхождения. `--lab-ack` только добавляет строку `execute`, ничего не запускает.

```bash
uv run --frozen detkit atomic-list T1033 --atomic-file /path/to/atomics/T1033/T1033.yaml
uv run --frozen detkit atomic-plan T1033 --atomic-file /path/to/atomics/T1033/T1033.yaml --test-guid REPLACE_WITH_REAL_GUID
```

В `bundle` можно передать те же `--atomic-file`, `--test-guid`, `--atomic-commit`, `--lab-ack`. Путь и GUID выше необходимо заменить; вымышленные GUID не являются готовыми тестами.

## Коды завершения

`0` — команда успешно обработана или проверка прошла. `1` — размеченный случай или целостность пакета не прошли. `2` — ошибка аргументов, чтения, разбора или конвертации. `doctor` не проверяет SIEM/API/Windows стенд. `verify-bundle` проверяет целостность, не подпись и не качество детекции.

Формат событий и точные ограничения: [CORE-CONTRACT.md](CORE-CONTRACT.md).
