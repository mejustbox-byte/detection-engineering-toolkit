# История изменений

## 0.1.0a2

Добавлены doctor, external Sigma conversion, bundle integrity и optional Atomic commit provenance. Исправлены parse/hash race и потеря cleanup metadata; некорректные/cyclic Atomic metadata отклоняются. Полная документация RU/EN, двуязычный REPORT, 31 тест и wheel smoke на обоих OS.

## 0.1.0a1 — 2026-10-09

Первый prerelease: четыре Discovery сценария, Sigma, Splunk/Defender, offline fixtures и validation, GUID Atomic plan, SHA256 bundles. Linux/Windows CI: 20 тестов. UTF-8 корректно выводится в legacy Windows pipe. Реальная лабораторная валидация не выполнялась.

До 1.0 CLI/JSON контракт может меняться между prerelease; опубликованные bundles остаются самостоятельными артефактами. Integrity verifier принимает manifest базовой версии 0.1.0a1.
