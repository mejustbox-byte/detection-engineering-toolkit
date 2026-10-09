import hashlib
import json
import subprocess
import sys

import pytest
import yaml

from detection_toolkit.cli import main
from detection_toolkit.core import (
    InputError,
    atomic_plan,
    atomic_tests,
    bundle,
    convert_file,
    doctor,
    verify_bundle,
)


def test_doctor_exercises_every_installed_scenario():
    result = doctor()
    assert result["passed"]
    assert {c["technique"] for c in result["checks"]} == {"T1033", "T1082", "T1016", "T1057"}
    assert result["siem_execution"] == result["atomic_execution"] == "not_run"


def test_external_sigma_is_converted_without_catalogue_dependency(tmp_path):
    rule = tmp_path / "custom.yml"
    rule.write_text(
        """title: Custom local process detection
id: e9115ee7-6c4c-47f6-bcf2-22b8fba7bcd8
status: experimental
logsource:
  product: windows
  category: process_creation
detection:
  selection:
    Image|endswith: '\\example.exe'
    CommandLine|contains: '--inventory'
  condition: selection
level: low
""",
        encoding="utf-8",
    )
    for target in ("splunk", "defender"):
        query = convert_file(rule, target)[0]
        assert "example.exe" in query and "--inventory" in query
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "detection_toolkit.cli",
            "convert-file",
            str(rule),
            "--target",
            "defender",
        ],
        capture_output=True,
    )
    assert result.returncode == 0 and b"DeviceProcessEvents" in result.stdout


@pytest.mark.parametrize(
    "content",
    ["", "not: a-sigma-rule", "\xff", "detection: [", "!!python/object/apply:os.system [echo bad]"],
)
def test_external_sigma_errors_are_structured(tmp_path, content, capsys):
    path = tmp_path / "bad.yml"
    path.write_bytes(content.encode("latin1"))
    assert main(["convert-file", str(path), "--target", "splunk"]) == 2
    assert "Traceback" not in capsys.readouterr().err


def test_integrity_detects_tampering_missing_and_unexpected_files(tmp_path):
    output = tmp_path / "bundle"
    bundle("T1033", output)
    assert verify_bundle(output)["passed"]
    (output / "splunk.txt").write_text("changed", encoding="utf-8")
    assert not verify_bundle(output)["passed"]
    assert main(["verify-bundle", str(output)]) == 1
    (output / "splunk.txt").unlink()
    assert not verify_bundle(output)["passed"]
    (output / "extra.txt").write_text("extra")
    assert verify_bundle(output)["unexpected_files"] == ["extra.txt"]


def test_manifest_path_traversal_rejected_before_reading(tmp_path):
    output = tmp_path / "bundle"
    bundle("T1033", output)
    manifest = output / "manifest.json"
    data = json.loads(manifest.read_text())
    data["files"]["../secret"] = "0" * 64
    manifest.write_text(json.dumps(data))
    with pytest.raises(InputError):
        verify_bundle(output)


def test_atomic_plan_hashes_the_parsed_snapshot_and_records_provenance(tmp_path):
    path = tmp_path / "atomic.yml"
    guid = "12345678-1234-1234-1234-123456789abc"
    path.write_text(
        yaml.safe_dump(
            {
                "attack_technique": "T1033",
                "atomic_tests": [
                    {
                        "name": "Synthetic interface case",
                        "auto_generated_guid": guid,
                        "supported_platforms": ["windows"],
                        "executor": {
                            "name": "command_prompt",
                            "command": "whoami",
                            "cleanup_command": "echo done",
                        },
                    }
                ],
            }
        ),
        encoding="utf-8",
    )
    result = atomic_plan(path, "T1033", guid, False, "a" * 40)
    assert result["atomic_yaml_sha256"] == hashlib.sha256(path.read_bytes()).hexdigest()
    assert result["source_provenance"] == "user_supplied_unverified"
    assert result["test"]["cleanup_command"] == "echo done"
    assert "execute" not in result
    with pytest.raises(InputError):
        atomic_plan(path, "T1033", guid, False, "short-sha")
    data = yaml.safe_load(path.read_text())
    data["atomic_tests"][0]["executor"]["elevation_required"] = "false"
    path.write_text(yaml.safe_dump(data), encoding="utf-8")
    with pytest.raises(InputError):
        atomic_tests(path, "T1033")


def test_recursive_atomic_metadata_does_not_escape_as_traceback(tmp_path, capsys):
    path = tmp_path / "cycle.yml"
    path.write_text("""attack_technique: T1033
atomic_tests:
  - name: Synthetic interface case
    auto_generated_guid: 12345678-1234-1234-1234-123456789abc
    supported_platforms: [windows]
    executor: {name: command_prompt, command: whoami}
    input_arguments: &cycle
      loop: *cycle
""")
    assert main(["atomic-list", "T1033", "--atomic-file", str(path)]) == 2
    assert "Traceback" not in capsys.readouterr().err
