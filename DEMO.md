# Полный демонстрационный процесс

## 1. Подготовить инструмент

```bash
uv sync --frozen --extra dev
uv run --frozen detkit doctor
```

Сохраните версию checkout и результат doctor. Его `passed` подтверждает локальную доступность каталога и двух backend.

## 2. Построить пакет T1016

```bash
uv run --frozen detkit bundle T1016 --output output/demo-network
uv run --frozen detkit verify-bundle output/demo-network
uv run --frozen detkit validate T1016 --cases output/demo-network/fixtures.json
```

Откройте Sigma, SPL/KQL и JSON отчёт. Убедитесь, что негативные случаи присутствуют. Наблюдаемый сигнал — `ipconfig.exe` с `/all`; обычная диагностика тоже совпадёт.

## 3. Проверить собственное правило

```bash
uv run --frozen detkit convert-file output/demo-network/rule.yml --target defender
```

Этот пример конвертирует файл с диска. Внешнее правило может использовать другие поддерживаемые backend условия; `validate` встроенного сценария не проверяет такое правило.

## 4. Связать с Atomic

Получите upstream Atomic Red Team отдельным контролируемым способом, закрепите commit и выберите Windows GUID через `atomic-list`. Создайте **новый** bundle с `--atomic-file`, `--test-guid` и `--atomic-commit`. Сравните реальную команду с правилом. Просмотрите ShowDetails, prerequisites, входные аргументы и cleanup. `--lab-ack` нужен только для вывода команды запуска.

## 5. Собрать лабораторные доказательства

По [LOCAL-PC.md](LOCAL-PC.md) получите события в Splunk/Defender, выполните запрос, отрицательную проверку и cleanup. Запишите точные версии, UTC время, задержку доставки и результат. Пока этого нет, корректный вывод демонстрации — «артефакты построены, offline случаи прошли, real SIEM/Atomic not_run».

Ценность демонстрации — прослеживаемая цепочка и возможность обнаружить разрыв между поведением, телеметрией и запросом.
