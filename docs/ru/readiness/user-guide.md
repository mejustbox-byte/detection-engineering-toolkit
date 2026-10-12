# Руководство

Синтетический пример записывает обёртку и возвращает 2: девять локальных проверок проходят, три SIEM-delivery остаются not_tested. Код 1 — известный отказ, 3 — неверный readiness-вход/выход. Прежние команды сохраняют прежние коды. Выход не должен существовать. --maximum-age-days задаёт политику давности. Assessment — opsec-1.0; внешняя обёртка каталога не является envelope контракта отчёта.

```bash
uv sync --frozen --extra dev
uv run --frozen detkit readiness examples/readiness.synthetic.json --observed-at 2026-10-12T00:00:00Z --output readiness.json
```

[Index](index.md)
