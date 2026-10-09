# Процесс выпуска

1. Согласуйте version в pyproject, `__init__`, lock и notes; обновите RU/EN документы.
2. Запустите проверки [VALIDATION.md](VALIDATION.md), убедитесь в отсутствии приватных данных.
3. Откройте PR; проверьте diff и дождитесь успешного Windows/Linux CI на точном HEAD.
4. Слейте PR, дождитесь CI main и запишите полный merge SHA.
5. В Actions запустите «Выпуск prerelease» из main: укажите merge SHA в `commit`, тег версии в `tag`, например `v0.1.0a2`.
6. Build job проверяет checkout=main SHA и tag=package version, выполняет frozen тесты, lint, doctor, build и wheel smoke вне checkout.
7. Publish job с `contents: write` создаёт новый GitHub prerelease; assets скачиваются и проверяются по SHA256SUMS.
8. Проверьте страницу релиза, tag commit, все assets и Success workflow. Не передвигайте опубликованный тег.

## Артефакты

Wheel, sdist, tracked source ZIP, двуязычные notes и SHA256SUMS. Source ZIP включает lock, scripts, tests, docs и workflow. Wheel install через pip не эквивалентен frozen source install. SHA256SUMS не является цифровой подписью.

## Ошибки

Существующий tag/release не перезаписывается. Если publish создал release, но проверка assets завершилась ошибкой, сначала исследуйте опубликованные файлы; не запускайте повторно create вслепую. Новый исправленный продукт получает новую версию. Real lab `not_run` указывается явно.
