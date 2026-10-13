import copy
import json

import pytest
from opsec_reports.core import ReportError

from detection_toolkit.cli import main
from detection_toolkit.lab_import import EXPECTED, normalize
from detection_toolkit.readiness import assess

NOW = "2026-10-13T10:00:20Z"


def fixture():
    commands, events = [], []
    for pid, (cid, (tech, expected, exe)) in enumerate(EXPECTED.items(), 100):
        image = "C:\\Windows\\System32\\" + exe
        commands.append(
            dict(id=cid, technique=tech, expected=expected, pid=pid, image=image, exit_code=0)
        )
        events.append(
            dict(
                case_id=cid,
                record_id=pid,
                observed_at="2026-10-13T10:00:05Z",
                process_id=pid,
                Image=image,
                CommandLine=image + (" /all" if exe == "ipconfig.exe" else ""),
            )
        )
    return dict(
        schema_version="windows-lab-1.0",
        synthetic=True,
        execution_id="synthetic-only",
        started_at="2026-10-13T10:00:00Z",
        completed_at="2026-10-13T10:00:10Z",
        collection_state="available",
        commands=commands,
        events=events,
        siem_delivery="not_run",
        provenance="operator_supplied_unverified",
    )


def test_synthetic_end_to_end_and_no_siem_execution():
    normalized = normalize(fixture())
    assert normalized["synthetic"] is True
    r = assess(normalized, NOW)
    assert r["assessment"]["summary"]["pass"] == 9
    assert r["assessment"]["summary"]["not_tested"] == 3
    assert all(c["siem_delivery"] == "not_run" for c in r["chains"])


@pytest.mark.parametrize("synthetic", [True, False])
def test_classification_preserved(synthetic):
    data = fixture()
    data["synthetic"] = synthetic
    assert normalize(data)["synthetic"] is synthetic


@pytest.mark.parametrize(
    "mutation",
    [
        lambda d: d.pop("synthetic"),
        lambda d: d.update(synthetic="false"),
        lambda d: d.update(siem_delivery="verified"),
        lambda d: d["events"].append(copy.deepcopy(d["events"][0])),
        lambda d: d["events"][0].update(process_id=999),
        lambda d: d["events"][0].update(observed_at="2026-10-14T10:00:00Z"),
        lambda d: d["events"][1].update(record_id=d["events"][0]["record_id"]),
        lambda d: d["commands"][1].update(pid=d["commands"][0]["pid"]),
        lambda d: d["commands"][0].update(expected=1),
        lambda d: d["commands"][0].update(image="wrong.exe"),
        lambda d: d.update(completed_at="2026-10-13T12:00:00Z"),
    ],
)
def test_inconsistent_or_unclassified_evidence_rejected(mutation):
    data = fixture()
    mutation(data)
    with pytest.raises(ReportError):
        normalize(data)


@pytest.mark.parametrize("state", ["unavailable", "truncated"])
def test_unavailable_collection_is_unknown(state):
    data = fixture()
    data["collection_state"] = state
    assert all(
        c["cases"] is None and c["telemetry"]["available"] is None
        for c in normalize(data)["chains"]
    )


def test_missing_command_line_fails_ipconfig_mapping():
    data = fixture()
    data["events"][2]["CommandLine"] = None
    result = assess(normalize(data), NOW)
    assert result["assessment"]["results"][9]["status"] == "fail"


def test_missing_negative_control_is_not_tested():
    data = fixture()
    data["events"].pop()
    result = assess(normalize(data), NOW)
    assert result["assessment"]["results"][6]["status"] == "not_tested"


def test_cli_new_output_and_invalid_input(tmp_path):
    source = tmp_path / "events.json"
    source.write_text(json.dumps(fixture()), encoding="utf-8")
    out = tmp_path / "assessment.json"
    args = ["lab-check", str(source), "--output", str(out), "--observed-at", NOW]
    assert main(args) == 2
    original = out.read_bytes()
    assert main(args) == 3
    assert out.read_bytes() == original
    source.write_text(json.dumps(fixture()), encoding="utf-8-sig")
    assert main(["lab-import", str(source), "--output", str(tmp_path / "bad.json")]) == 3
