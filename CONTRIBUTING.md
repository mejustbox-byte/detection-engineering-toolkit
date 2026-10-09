# Участие в разработке

## Рабочий цикл

Создайте отдельную ветку от актуального main. Воспроизведите ошибку, определите ожидаемое поведение и уровень validation. Изменяйте код и документы RU/EN вместе; синтетические inputs обязательны для публикуемых примеров.

```bash
uv sync --frozen --extra dev
uv run --frozen --extra dev pytest -q
uv run --frozen --extra dev ruff check .
uv run --frozen --extra dev ruff format --check .
uv run --frozen detkit doctor
uv build
```

Для нового сценария укажите ATT&CK reference, конкретное поведение, logsource, positive/negative cases и false positives. Проверяйте оба backend. Добавление записи каталога не означает покрытие всей техники.

## Ревью

PR описывает проблему, итоговое поведение, проверки и ограничения. Проверьте поведение malformed input, version/lock alignment, packaged data и wheel install. Перед слиянием должны пройти Windows/Linux CI. Изменение контракта требует ADR или пояснения совместимости. Для лабораторного результата приложите обезличенный protocol, не исходные журналы.

Не включайте личные данные, credentials, внутренние endpoints или служебную переписку в код, документы, commit messages и release notes. Security reports: [SECURITY.md](SECURITY.md).
