import hashlib
import json
import os
import subprocess
import sys
from uuid import UUID

import pytest
import yaml
from sigma.collection import SigmaCollection

from detection_toolkit.cli import main
from detection_toolkit.core import (
    InputError,
    atomic_plan,
    atomic_tests,
    bundle,
    convert,
    fixture_cases,
    generate_rule,
    load_file,
    scenario_for,
    scenarios,
    validate_cases,
)


@pytest.mark.parametrize("scenario", scenarios(), ids=lambda s: s["id"])
def test_rules_and_backends(scenario):
    rule = generate_rule(scenario)
    parsed = SigmaCollection.from_yaml(rule)
    assert len(parsed.rules) == 1
    assert UUID(str(parsed.rules[0].id))
    assert scenario["technique"].lower() in rule
    splunk = convert(rule, "splunk")[0]
    kql = convert(rule, "defender")[0]
    assert scenario["image"].split("\\")[-1] in splunk
    assert "DeviceProcessEvents" in kql
    assert scenario["image"].split("\\")[-1] in kql
    assert "Image" in splunk
    for fragment in scenario["contains"]:
        assert fragment in splunk and fragment in kql
    assert rule == generate_rule(scenario)
    assert convert(rule, "splunk") == [splunk]
    assert validate_cases(scenario, fixture_cases(scenario))["passed"]


@pytest.mark.parametrize("technique", ["T9999", "T1033;whoami", "../T1033", "t1033", ""])
def test_reject_unsupported(technique):
    with pytest.raises(InputError):
        scenario_for(technique)


def test_predicate_wrong_expected_fails():
    scenario = scenario_for("T1033")
    cases = fixture_cases(scenario)
    cases[0]["expected"] = False
    assert validate_cases(scenario, cases)["passed"] is False


@pytest.mark.parametrize(
    "cases",
    [
        [],
        {},
        [{"id": "x", "expected": "false", "event": {}}],
        [{"id": "x", "expected": False, "event": {"Image": 7}}],
    ],
)
def test_invalid_cases(cases):
    with pytest.raises(InputError):
        validate_cases(scenario_for("T1033"), cases)


@pytest.fixture
def atomic(tmp_path):
    path = tmp_path / "atomic.yml"
    path.write_text(
        yaml.safe_dump(
            {
                "attack_technique": "T1033",
                "atomic_tests": [
                    {
                        "auto_generated_guid": "12345678-1234-1234-1234-123456789abc",
                        "name": "Синтетический тест интерфейса, не upstream Atomic",
                        "supported_platforms": ["windows"],
                        "executor": {"name": "command_prompt", "command": "whoami"},
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    return path


def test_atomic_guid_selection(atomic):
    guid = atomic_tests(atomic, "T1033")[0]["guid"]
    plan = atomic_plan(atomic, "T1033", guid, False)
    assert "execute" not in plan
    assert plan["execution"] == "not_run"
    assert "-TestGuids " + guid in plan["show_details"]
    assert atomic_plan(atomic, "T1033", guid, True)["execute"].endswith(guid)
    assert plan["coverage"] == "manual_review_required"
    with pytest.raises(InputError):
        atomic_tests(atomic, "T1082")
    with pytest.raises(InputError):
        atomic_plan(atomic, "T1033", "00000000-0000-0000-0000-000000000000", True)
    with pytest.raises(InputError):
        atomic_plan(atomic, "T1033", "'; whoami", True)


def test_bundle_manifest_and_no_overwrite(tmp_path):
    output = tmp_path / "out"
    bundle("T1016", output)
    manifest = json.loads((output / "manifest.json").read_text(encoding="utf-8"))
    for name, digest in manifest["files"].items():
        assert hashlib.sha256((output / name).read_bytes()).hexdigest() == digest
    assert (
        json.loads((output / "validation.json").read_text(encoding="utf-8"))["siem_execution"]
        == "not_run"
    )
    with pytest.raises(FileExistsError):
        bundle("T1016", output)
    with pytest.raises(InputError):
        bundle("T9999", tmp_path / "invalid")
    assert not (tmp_path / "invalid").exists()


def test_bundle_requires_guid(tmp_path, atomic):
    with pytest.raises(InputError):
        bundle("T1033", tmp_path / "out", atomic=atomic)
    assert not (tmp_path / "out").exists()


def test_cli_codes(tmp_path, capsys):
    assert main(["list"]) == 0
    assert main(["rule", "T9999"]) == 2
    assert "Ошибка" in capsys.readouterr().err
    cases = tmp_path / "cases.json"
    cases.write_text(json.dumps([{"id": "x", "expected": True, "event": {}}]))
    assert main(["validate", "T1033", "--cases", str(cases)]) == 1


def test_yaml_unsafe_tag_rejected(tmp_path):
    path = tmp_path / "evil.yml"
    path.write_text('!!python/object/apply:os.system ["echo bad"]')
    with pytest.raises(InputError):
        load_file(path, "yaml")


def test_cli_utf8_with_legacy_pipe_encoding():
    env = dict(os.environ, PYTHONIOENCODING="cp1252")
    result = subprocess.run(
        [sys.executable, "-m", "detection_toolkit.cli", "list"],
        env=env,
        capture_output=True,
        check=True,
    )
    catalogue = json.loads(result.stdout.decode("utf-8"))
    assert catalogue[0]["name"].startswith("Обнаружение")
