# Манифест readiness-1.0

Корень: ровно schema_version, scope, synthetic и chains. Цепочка содержит id, risk, technique, telemetry, cases и delivery. ID уникальны, до 80 символов; risk/scope — до 128. Techniques ограничены T1033, T1082 и T1016. Synthetic — строго boolean.

Telemetry содержит source (windows.process_creation/unknown), available (boolean/null), mapped_fields (уникальные строки/null). Cases — null либо 1–256 точных объектов id/expected/event. Expected — boolean; event принимает только строковые Image/CommandLine до 4096 символов. Delivery содержит state, target, execution_id, observed_at и rule_sha256. Target — splunk/defender; state — verified/failed/not_run/unknown. Время — UTC YYYY-MM-DDTHH:MM:SSZ либо null. Полный пример — examples/readiness.synthetic.json.

[Index](index.md)
