# Заметки к подготовленной версии 0.1.0a1

Локальная предварительная версия; публичного выпуска ещё нет.

Добавлены четыре Discovery сценария Windows: T1033/whoami, T1082/hostname, T1016/ipconfig /all, T1057/tasklist. CLI формирует experimental Sigma, SPL/KQL, synthetic fixtures, validation report, конкретный GUID-план Atomic и SHA256 manifest.

Документы описывают угрозы, контракты, установку, лабораторию и ограничения. Подготовлены frozen dependencies, setup scripts и GitHub Actions для Linux/Windows.

Ограничения: узкое наблюдаемое поведение, легитимные false positives, отсутствие полного ATT&CK каталога, SIEM API и automatic runner. Offline predicate validation не выполняет Sigma/SIEM. Windows VM, upstream Atomic и реальные SIEM query пока not_run. Offline CI прошёл на Linux и Windows: 20 тестов, lint, сборка и bundle smoke.
