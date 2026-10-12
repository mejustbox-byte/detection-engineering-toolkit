import copy
import hashlib
import json

import pytest
from opsec_reports.core import ReportError, compare, outcome

from detection_toolkit.cli import main
from detection_toolkit.core import InputError, fixture_cases, generate_rule, scenario_for
from detection_toolkit.readiness import assess

NOW = "2026-10-12T00:00:00Z"


def fixture():
    chains = []
    for technique in ["T1033", "T1082", "T1016"]:
        scenario = scenario_for(technique)
        chains.append(
            {
                "id": scenario["id"],
                "risk": "synthetic-discovery",
                "technique": technique,
                "telemetry": {
                    "source": "windows.process_creation",
                    "available": True,
                    "mapped_fields": ["Image", "CommandLine"],
                },
                "cases": fixture_cases(scenario),
                "delivery": {
                    "state": "not_run",
                    "target": "splunk",
                    "execution_id": None,
                    "observed_at": None,
                    "rule_sha256": None,
                },
            }
        )
    return {
        "schema_version": "readiness-1.0",
        "scope": "synthetic-readiness",
        "synthetic": True,
        "chains": chains,
    }


def statuses(data):
    return [r["status"] for r in assess(data, NOW)["assessment"]["results"][:4]]


def test_three_chains_reuse_existing_api_without_siem_claim():
    r = assess(fixture(), NOW)
    assert r["assessment"]["summary"]["pass"] == 9
    assert r["assessment"]["summary"]["not_tested"] == 3
    assert outcome(r["assessment"]) == 2
    assert all(c["sigma_execution"] == c["atomic_execution"] == "not_run" for c in r["chains"])
    assert all(all(c["conversion_targets"].values()) for c in r["chains"])


@pytest.mark.parametrize("available,expected", [(False, "fail"), (None, "not_tested")])
def test_sources(available, expected):
    d = fixture()
    d["chains"][0]["telemetry"]["available"] = available
    assert statuses(d)[0] == expected


def test_field_mapping_missing_and_unknown():
    d = fixture()
    d["chains"][2]["telemetry"]["mapped_fields"] = ["Image"]
    assert assess(d, NOW)["assessment"]["results"][9]["status"] == "fail"
    d["chains"][0]["telemetry"]["mapped_fields"] = None
    assert statuses(d)[1] == "not_tested"


def test_positive_event_missing_required_field():
    d = fixture()
    d["chains"][0]["cases"][0]["event"].pop("Image")
    assert statuses(d)[1:3] == ["fail", "fail"]


def test_wrong_expected_predicate():
    d = fixture()
    d["chains"][0]["cases"][0]["expected"] = False
    assert statuses(d)[2] == "fail"


def test_missing_negative_and_absent_cases():
    d = fixture()
    d["chains"][0]["cases"] = [c for c in d["chains"][0]["cases"] if c["expected"]]
    assert statuses(d)[2] == "not_tested"
    d["chains"][0]["cases"] = None
    assert statuses(d)[1:3] == ["not_tested", "not_tested"]


def verified():
    d = fixture()
    c = d["chains"][0]
    c["delivery"].update(
        state="verified",
        execution_id="synthetic-execution",
        observed_at=NOW,
        rule_sha256=hashlib.sha256(
            generate_rule(scenario_for(c["technique"])).encode()
        ).hexdigest(),
    )
    return d


def test_delivery_verified_is_explicit_unverified_declaration():
    d = verified()
    assert statuses(d)[3] == "pass"
    assert assess(d, NOW)["chains"][0]["provenance"] == "user_supplied_unverified"


@pytest.mark.parametrize("key", ["execution_id", "observed_at", "rule_sha256"])
def test_delivery_incomplete(key):
    d = verified()
    d["chains"][0]["delivery"][key] = None
    assert statuses(d)[3] == "not_tested"


def test_delivery_failure_and_wrong_hash():
    d = fixture()
    d["chains"][0]["delivery"]["state"] = "failed"
    assert statuses(d)[3] == "fail"
    d = verified()
    d["chains"][0]["delivery"]["rule_sha256"] = "0" * 64
    assert statuses(d)[3] == "fail"


def test_delivery_age_boundary():
    d = verified()
    d["chains"][0]["delivery"]["observed_at"] = "2026-09-12T00:00:00Z"
    assert statuses(d)[3] == "pass"
    d["chains"][0]["delivery"]["observed_at"] = "2026-09-11T23:59:59Z"
    assert statuses(d)[3] == "fail"


def test_future_delivery_rejected():
    d = verified()
    d["chains"][0]["delivery"]["observed_at"] = "2027-01-01T00:00:00Z"
    with pytest.raises(ReportError):
        assess(d, NOW)


@pytest.mark.parametrize(
    "mutation", ["extra", "duplicate", "unsupported", "boolean", "event-type", "empty"]
)
def test_invalid_manifest(mutation):
    d = fixture()
    if mutation == "extra":
        d["extra"] = "synthetic"
    if mutation == "duplicate":
        d["chains"].append(copy.deepcopy(d["chains"][0]))
    if mutation == "unsupported":
        d["chains"][0]["technique"] = "T9999"
    if mutation == "boolean":
        d["chains"][0]["telemetry"]["available"] = 1
    if mutation == "event-type":
        d["chains"][0]["cases"][0]["event"]["Image"] = 1
    if mutation == "empty":
        d["chains"] = []
    with pytest.raises((ReportError, InputError)):
        assess(d, NOW)


def test_budgets():
    with pytest.raises(ReportError):
        assess(fixture(), NOW, max_chains=1)
    with pytest.raises(ReportError):
        assess(fixture(), NOW, maximum_age_days=True)


def test_cli_preserves_coverage_and_refuses_overwrite(tmp_path):
    p = tmp_path / "in.json"
    p.write_text(json.dumps(fixture()), encoding="utf-8")
    args = ["readiness", str(p), "--observed-at", NOW, "--output", str(tmp_path / "out.json")]
    assert main(args) == 2
    assert main(args) == 3


def test_cli_strict_json_no_echo(tmp_path, capsys):
    p = tmp_path / "bad.json"
    p.write_text('{"SENSITIVE_MARKER":NaN}', encoding="utf-8")
    assert (
        main(["readiness", str(p), "--observed-at", NOW, "--output", str(tmp_path / "out.json")])
        == 3
    )
    assert "SENSITIVE_MARKER" not in capsys.readouterr().err


def test_different_delivery_age_policy_is_not_comparable():
    before = assess(fixture(), NOW, maximum_age_days=30)["assessment"]
    after = assess(fixture(), NOW, maximum_age_days=90)["assessment"]
    assert not compare(before, after)["comparable"]
