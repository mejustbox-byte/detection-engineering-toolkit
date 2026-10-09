# План развития

| Этап | Результат | Статус |
|---|---|---|
| Offline MVP | Четыре сценария, Sigma, SPL/KQL, cases, Atomic plan | Реализовано в 0.1.0a1 |
| Рабочие процессы | doctor, external Sigma, integrity, snapshot provenance, RU/EN | Реализовано в 0.1.0a2 |
| Лабораторная валидация | Windows VM, реальные Atomic GUID, доставка и match в обоих SIEM | Не выполнено |
| Операционная пригодность | Полевая настройка, false-positive baseline, data-source profiles | Запланировано |
| Расширение каталога | Дополнительные конкретные сценарии и ATT&CK dataset provenance | Запланировано |
| Защита артефактов | Подписи, dependency audit и supply-chain provenance | Запланировано |

Следующий приоритет — лабораторное подтверждение существующих правил, а не количество новых техник. Acceptance: известные версии, один upstream GUID, наблюдаемая телеметрия, query match, negative case и cleanup. Без этого stable/production-ready статус не присваивается.

SIEM API и автоматический runner не имеют утверждённой реализации. Перед их добавлением нужна отдельная модель угроз, изоляция и управление credentials.
