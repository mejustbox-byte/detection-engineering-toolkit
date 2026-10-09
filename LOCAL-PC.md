# Реальная лаборатория на локальном ПК

## Стенд

Одноразовая Windows VM с snapshot и явно согласованным владельцем; Sysmon process creation для Splunk либо onboarded Defender endpoint для DeviceProcessEvents; разрешённый SIEM workspace. На macOS Intel используйте отдельный доступный Windows x86-64 стенд; конкретный hypervisor выбирает оператор. Контейнер Linux не доказывает Windows telemetry.

## Подготовка

Запишите OS/build, time sync, Sysmon config hash либо Defender onboarding, SIEM версии, таблицы, fields и index. Возьмите Atomic Red Team и Invoke-AtomicRedTeam из официальных источников, зафиксируйте оба commit. Прочитайте procedure и dependencies; автоматического GetPrereqs нет. Snapshot создаётся до теста; проверяется возможность отката.

## Протокол одного сценария

1. Создайте bundle и проверьте hashes. Запишите ATT&CK ID, scenario, UUID правила и версии dependencies.
2. Выполните `atomic-list` на локальном YAML. Выберите Windows GUID, чья процедура действительно использует наблюдаемый процесс/аргумент. Не используйте весь список техники.
3. Сверьте input arguments, elevation и cleanup. В плане SHA256 должен совпасть с файлом установленного Atomic checkout.
4. В согласованной VM выполните ShowDetails и CheckPrereqs по плану. Наличие зависимостей ещё не означает запуск теста.
5. Согласуйте окно UTC, host scope и изменения. Сформируйте execute с `--lab-ack`; выполните вручную только выбранный GUID. Зафиксируйте начало, конец, stdout/stderr и исходный endpoint event.
6. Проверьте ingestion: event поступил, Image/CommandLine mapping совпал, timestamp находится в окне. Отсутствующий raw event — проблема телеметрии, не доказательство качества правила.
7. Выполните подготовленный SPL/KQL с ограниченным scope. Сохраните query hash, raw event ID, результат и latency. Backend conversion сама по себе не подтверждает valid query в вашей версии SIEM.
8. Проверьте отрицательные случаи и типичный легитимный шум. Discovery правила могут совпадать на легитимной диагностике; фиксируйте это как ожидаемые false positives.
9. Выполните reviewed cleanup, затем восстановите snapshot и проверьте состояние. Заполните verdict: pass/fail/unknown/not_run с причиной.

## Шаблон доказательства

Поля: scenario, ATT&CK ID, правило SHA256, backend/pipeline/version, Atomic GUID/YAML SHA256/upstream commits, VM snapshot, OS, UTC interval, raw event reference, query SHA256, matches, negative results, latency, cleanup verification, reviewer и verdict. Реальные данные хранятся приватно; в git включается синтетический аналог.

Все перечисленные реальные проверки на дату подготовки **НЕ ВЫПОЛНЕНЫ**. Отчёт offline_scope нельзя копировать как результат SIEM.
