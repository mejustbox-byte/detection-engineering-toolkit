# Manifest readiness-1.0

Root fields are exactly schema_version, scope, synthetic and chains. Each chain contains id, risk, technique, telemetry, cases and delivery. IDs are unique strings up to 80 characters, risk and scope strings up to 128. Techniques are restricted to T1033, T1082 and T1016. synthetic is strictly boolean.

Telemetry contains source (windows.process_creation/unknown), available (boolean/null), mapped_fields (unique strings/null). Cases are null or 1–256 exact id/expected/event objects. Expected is boolean; event accepts only string Image/CommandLine values up to 4096 characters. Delivery contains state, target, execution_id, observed_at and rule_sha256. Target is splunk/defender; state verified/failed/not_run/unknown. Observation time is UTC YYYY-MM-DDTHH:MM:SSZ or null. Full example is examples/readiness.synthetic.json.

[Index](index.md)
