# ADR 0001: детерминированный offline CLI

Статус: принят для MVP. Дата: 2026-10-09.

## Контекст

Пользователь хочет цепочку ATT&CK/Sigma/SIEM/Atomic для флагманского портфолио. Один technique ID не задаёт telemetry или procedure; произвольная генерация создаёт ложную полноту. Автоматический Atomic runner требует изоляции и отдельных механизмов разрешения.

## Решение

Python CLI с собственным явным каталогом сценариев; реальные pySigma backends; локальный Atomic YAML с конкретным GUID; только вывод плана, без исполнения; synthetic predicate tests отдельно от lab verdict. Первые сценарии — discovery через Windows process creation.

## Альтернативы

LLM с универсальным rule generation: гибко, но недетерминированно и требует expert review. Собственный Sigma transpiler: контроль формата, но дублирование сложной семантики. SIEM web service: удобнее collaboration, но credentials и attack surface. Полный Atomic runner: автоматизация, но привилегии/rollback/контроль сети требуют отдельного проекта безопасности.

## Последствия

MVP воспроизводим и ограничен четырьмя сценариями; отвечает на неизвестные техники отказом. Реальная цепочка завершается только после VM/SIEM протокола. Каталог расширяется с independent review и negative cases; автоматическое execution не добавляется без нового ADR.
