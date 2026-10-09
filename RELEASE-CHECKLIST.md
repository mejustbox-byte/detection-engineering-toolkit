# Чеклист выпуска

Эта форма заполняется для конкретного release commit; пустой пункт не означает pass.

- [ ] Package version, runtime version, lock и tag согласованы.
- [ ] Все команды и документация RU/EN соответствуют реализации.
- [ ] PR diff проверен; Windows/Linux CI успешен на точном HEAD.
- [ ] Merge SHA совпадает с main; main CI успешен.
- [ ] Frozen install, тесты, lint/format и doctor успешны.
- [ ] Wheel установлен вне checkout; bundle integrity успешна.
- [ ] Source ZIP содержит весь tracked source и двуязычные docs.
- [ ] Нет secrets, реальных событий и приватных endpoints.
- [ ] Real Atomic/SIEM результаты отмечены pass/fail/not_run с обоснованием.
- [ ] Prerelease flag и ограничения присутствуют в notes.
- [ ] Новый tag относится к проверенному SHA и не передвигался.
- [ ] Wheel/sdist/source/notes/SHA256SUMS опубликованы.
- [ ] Скачанные assets прошли SHA256 check.

Методика: [RELEASE.md](RELEASE.md). Состояние: [VERIFICATION.md](VERIFICATION.md).
