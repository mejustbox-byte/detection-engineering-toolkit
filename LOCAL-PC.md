# Лаборатория на локальном ПК

## Стенд

Используйте отдельную Windows VM со snapshot, контролируемой сетью, рабочим источником process creation и отдельными тестовыми учётными записями. Для Windows событий подходят соответствующим образом настроенные Sysmon Event ID 1 или Security 4688; сбор CommandLine для 4688 нужно включать отдельно. Для Defender требуется onboarding устройства и доставка DeviceProcessEvents. macOS/Linux могут строить пакет, но не заменяют Windows стенд.

## Телеметрия и запросы

| Цель | Поля и проверка |
|---|---|
| Splunk | Убедитесь, что Windows process events имеют `Image`/`CommandLine`; ограничьте index, sourcetype, host и интервал времени согласно локальному deployment |
| Defender | Откройте Advanced Hunting; проверьте `DeviceProcessEvents`, `FileName`/`FolderPath`/`ProcessCommandLine` и устройство |

Проверьте фактический сгенерированный запрос: pipeline может менять имена полей. Не добавляйте field aliases без проверки исходного события. Отсутствие результата может означать отсутствие телеметрии, задержку доставки или несовпадение схемы.

## Протокол одного сценария

1. Запишите commit Toolkit, Python/backend версии, Windows build, версии сенсора/SIEM.
2. Закрепите upstream Atomic commit, путь YAML и Windows GUID; сохраните SHA256.
3. Сделайте snapshot. Просмотрите test command, defaults, elevated права, prerequisites и cleanup. Не устанавливайте prerequisites автоматически без ревью.
4. Постройте пакет, выполните `verify-bundle`; просмотрите Sigma/SPL/KQL и соответствие выбранному тесту.
5. Через ShowDetails и CheckPrereqs проверьте readiness. Укажите правильный `PathToAtomicsFolder` в Invoke-AtomicRedTeam отдельно от пути YAML Toolkit.
6. Запишите UTC начало/окончание и вручную выполните один одобренный тест в VM. Toolkit его не запускает.
7. Сохраните локально исходное событие и Event ID/Record ID либо Defender timestamp/device ID. Установите факт доставки в SIEM.
8. Выполните запрос в ограниченном временном окне; подтвердите совпадение конкретного события и запишите задержку.
9. Выполните негативный случай с другой утилитой и легитимный совпадающий случай. Последний показывает false positive, а не поломку правила.
10. Выполните проверенный cleanup и убедитесь в восстановлении состояния; при необходимости верните snapshot.

## Результат

Запишите `pass`, `fail` или `not_run` отдельно для execution, telemetry delivery, query match, negative case и cleanup. Для `fail` укажите наблюдение и шаг воспроизведения. Реальные события и host/user identifiers остаются вне публичного репозитория. Публикуйте только обезличенный отчёт и синтетические примеры.

Реальные лабораторные результаты этого проекта пока не получены. Работающие Linux/Windows offline тесты их не заменяют.
