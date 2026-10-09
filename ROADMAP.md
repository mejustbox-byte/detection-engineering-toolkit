# План развития

## 0.1 — Offline фундамент

Реализованы четыре reviewed-by-code Discovery шаблона, Sigma generation, два backend, Atomic parser/plan, fixtures, отчёт и packaging. Завершение этапа требует удалённого репозитория, GitHub CI и проверки опубликованной среды. Экспертный и лабораторный review ещё открыты.

## 0.2 — Измеряемый purple-team цикл

Добавить manifest выбранных upstream Atomic GUID/commits и соответствие procedure → predicate; воспроизвести минимум по одному Windows-сценарию в Splunk и Defender; capture normalized raw event; отчёт различает generation, ingestion, query execution и detection verdict. Критерий: независимые доказательства positive/negative и latency.

## 0.3 — Расширение каталога и SIEM

Подключить pinned MITRE STIX snapshot с provenance и revoked/deprecated ID validation, несколько сценариев на технику, Sentinel/Elastic через реальные backend с явными pipelines, coverage по процедурам. Критерий: нет скрытого универсального покрытия по одному ID.

## 0.4 — Флагманская демонстрация

Подготовить очищенные reproducible lab артефакты, видео демонстрации и portfolio narrative. Web UI и SIEM connectors только по отдельному ADR. LLM может предлагать experimental candidates, но без автоматической публикации/запуска и без обхода review.

Это план, а не реализованные возможности. Сроки не обещаются без доступного стенда и reviewer.
