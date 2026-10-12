"""Readiness assessments reuse the existing scenario and conversion APIs."""

import hashlib
from datetime import datetime, timezone

from opsec_reports.adapters import result
from opsec_reports.core import ReportError, make_report

from . import __version__
from .core import convert, generate_rule, scenario_for, validate_cases

TECHNIQUES = {"T1033", "T1082", "T1016"}


def require(ok):
    if not ok:
        raise ReportError("invalid_readiness_input")


def exact(obj, names):
    require(isinstance(obj, dict) and set(obj) == set(names))


def timestamp(value):
    require(isinstance(value, str) and len(value) == 20 and value.endswith("Z"))
    try:
        return datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    except ValueError:
        raise ReportError("invalid_timestamp") from None


def assess(data, observed_at, max_chains=100, maximum_age_days=30):
    require(type(max_chains) is int and 1 <= max_chains <= 100)
    require(type(maximum_age_days) is int and 1 <= maximum_age_days <= 3650)
    exact(data, ["schema_version", "scope", "synthetic", "chains"])
    require(data["schema_version"] == "readiness-1.0")
    require(isinstance(data["scope"], str) and 0 < len(data["scope"]) <= 128)
    require(type(data["synthetic"]) is bool)
    require(isinstance(data["chains"], list) and 0 < len(data["chains"]) <= max_chains)
    now = timestamp(observed_at)
    records, details, seen = [], [], set()
    for chain in data["chains"]:
        exact(chain, ["id", "risk", "technique", "telemetry", "cases", "delivery"])
        require(isinstance(chain["id"], str) and 0 < len(chain["id"]) <= 80)
        require(chain["id"] not in seen)
        seen.add(chain["id"])
        require(isinstance(chain["risk"], str) and 0 < len(chain["risk"]) <= 128)
        require(isinstance(chain["technique"], str) and chain["technique"] in TECHNIQUES)
        scenario = scenario_for(chain["technique"])
        rule = generate_rule(scenario)
        digest = hashlib.sha256(rule.encode("utf-8")).hexdigest()
        telemetry = chain["telemetry"]
        exact(telemetry, ["source", "available", "mapped_fields"])
        require(telemetry["source"] in ["windows.process_creation", "unknown"])
        require(telemetry["available"] is None or type(telemetry["available"]) is bool)
        fields = telemetry["mapped_fields"]
        require(
            fields is None
            or (
                isinstance(fields, list)
                and len(fields) <= 64
                and all(isinstance(f, str) and 0 < len(f) <= 128 for f in fields)
            )
        )
        if fields is not None:
            require(len(set(fields)) == len(fields))
        source = (
            "not_tested"
            if telemetry["source"] == "unknown" or telemetry["available"] is None
            else "pass"
            if telemetry["available"]
            else "fail"
        )
        required = ["Image"] + (["CommandLine"] if scenario["contains"] else [])
        mapping = (
            "not_tested" if fields is None else "pass" if set(required) <= set(fields) else "fail"
        )
        cases = chain["cases"]
        tested = None
        if cases is not None:
            require(isinstance(cases, list) and 0 < len(cases) <= 256)
            for case in cases:
                exact(case, ["id", "expected", "event"])
                require(isinstance(case["id"], str) and 0 < len(case["id"]) <= 80)
                require(type(case["expected"]) is bool and isinstance(case["event"], dict))
                require(set(case["event"]) <= {"Image", "CommandLine"})
                require(all(isinstance(v, str) and len(v) <= 4096 for v in case["event"].values()))
            tested = validate_cases(scenario, cases)
            positives = [c for c in cases if c["expected"]]
            if not positives and mapping == "pass":
                mapping = "not_tested"
            if positives and any(not all(k in c["event"] for k in required) for c in positives):
                mapping = "fail"
            predicate = (
                "fail"
                if not tested["passed"]
                else "pass"
                if positives and any(not c["expected"] for c in cases)
                else "not_tested"
            )
        else:
            predicate = "not_tested"
            if mapping == "pass":
                mapping = "not_tested"
        conversions = {target: bool(convert(rule, target)) for target in ["splunk", "defender"]}
        if not all(conversions.values()):
            predicate = "fail"
        delivery = chain["delivery"]
        exact(delivery, ["state", "target", "execution_id", "observed_at", "rule_sha256"])
        require(delivery["state"] in ["verified", "failed", "not_run", "unknown"])
        require(delivery["target"] in ["splunk", "defender"])
        for key in ["execution_id", "rule_sha256"]:
            require(
                delivery[key] is None
                or (isinstance(delivery[key], str) and len(delivery[key]) <= 128)
            )
        delivered_at = (
            None if delivery["observed_at"] is None else timestamp(delivery["observed_at"])
        )
        require(delivered_at is None or delivered_at <= now)
        delivered = "fail" if delivery["state"] == "failed" else "not_tested"
        if (
            delivery["state"] == "verified"
            and delivery["execution_id"]
            and delivered_at
            and delivery["rule_sha256"]
        ):
            delivered = (
                "pass"
                if delivery["rule_sha256"] == digest
                and (now - delivered_at).total_seconds() <= maximum_age_days * 86400
                else "fail"
            )
        for i, status in enumerate([source, mapping, predicate, delivered], 1):
            record = result(
                f"DET-00{i}",
                chain["id"],
                status,
                ("critical" if i == 4 else "high") if status == "fail" else "info",
            )
            record["message"] = "Readiness declaration " + status
            records.append(record)
        details.append(
            {
                "chain_id": chain["id"],
                "risk": chain["risk"],
                "technique": chain["technique"],
                "rule_sha256": digest,
                "conversion_targets": conversions,
                "predicate_scope": "offline_scenario_predicate",
                "siem_delivery": delivery["state"],
                "provenance": "user_supplied_unverified",
                "sigma_execution": "not_run",
                "atomic_execution": "not_run",
            }
        )
    assessment = make_report(
        "detection-engineering-toolkit",
        __version__,
        f"readiness-1.0-age-{maximum_age_days}d",
        data["scope"],
        observed_at,
        data["synthetic"],
        records,
    )
    return {"schema_version": "readiness-result-1.0", "assessment": assessment, "chains": details}
