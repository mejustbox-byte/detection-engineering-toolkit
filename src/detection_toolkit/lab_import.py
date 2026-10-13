"""Validate operator-supplied Windows laboratory evidence without claiming SIEM delivery."""

from .readiness import require, timestamp

EXPECTED = {
    "whoami-positive": ("T1033", True, "whoami.exe"),
    "hostname-positive": ("T1082", True, "hostname.exe"),
    "ipconfig-positive": ("T1016", True, "ipconfig.exe"),
    "other-process-negative": ("T1033", False, "cmd.exe"),
}


def normalize(data):
    require(
        isinstance(data, dict)
        and set(data)
        == {
            "schema_version",
            "synthetic",
            "execution_id",
            "started_at",
            "completed_at",
            "collection_state",
            "commands",
            "events",
            "siem_delivery",
            "provenance",
        }
    )
    require(data["schema_version"] == "windows-lab-1.0")
    require(type(data["synthetic"]) is bool)
    require(isinstance(data["execution_id"], str) and 0 < len(data["execution_id"]) <= 80)
    start, end = timestamp(data["started_at"]), timestamp(data["completed_at"])
    require(start <= end and (end - start).total_seconds() <= 3600)
    require(data["collection_state"] in ["available", "truncated", "unavailable"])
    require(
        data["siem_delivery"] == "not_run" and data["provenance"] == "operator_supplied_unverified"
    )
    commands = data["commands"]
    require(isinstance(commands, list) and len(commands) == 4)
    catalog = {}
    for command in commands:
        require(
            isinstance(command, dict)
            and set(command) == {"id", "technique", "expected", "pid", "image", "exit_code"}
        )
        require(
            isinstance(command["id"], str)
            and command["id"] in EXPECTED
            and command["id"] not in catalog
        )
        technique, expected, executable = EXPECTED[command["id"]]
        require(
            command["technique"] == technique
            and type(command["expected"]) is bool
            and command["expected"] == expected
        )
        require(
            type(command["pid"]) is int and command["pid"] > 0 and type(command["exit_code"]) is int
        )
        require(
            isinstance(command["image"], str)
            and command["image"].casefold().endswith("\\" + executable)
        )
        require(len(command["image"]) <= 4096)
        catalog[command["id"]] = command
    require(len({c["pid"] for c in commands}) == len(commands))
    events = data["events"]
    require(isinstance(events, list) and len(events) <= 256)
    selected = {}
    record_ids = set()
    for event in events:
        require(
            isinstance(event, dict)
            and set(event)
            == {"case_id", "record_id", "observed_at", "process_id", "Image", "CommandLine"}
        )
        require(isinstance(event["case_id"], str) and event["case_id"] in catalog)
        require(type(event["record_id"]) is int and event["record_id"] > 0)
        require(event["record_id"] not in record_ids)
        record_ids.add(event["record_id"])
        require(
            type(event["process_id"]) is int
            and event["process_id"] == catalog[event["case_id"]]["pid"]
        )
        require(
            isinstance(event["Image"], str)
            and event["Image"].casefold() == catalog[event["case_id"]]["image"].casefold()
        )
        require(
            event["CommandLine"] is None
            or (isinstance(event["CommandLine"], str) and len(event["CommandLine"]) <= 4096)
        )
        require(start <= timestamp(event["observed_at"]) <= end)
        require(event["case_id"] not in selected)
        selected[event["case_id"]] = event
    chains = []
    for technique in ["T1033", "T1082", "T1016"]:
        relevant = [c for c in commands if c["technique"] == technique]
        cases = []
        fields = {"Image", "CommandLine"}
        complete = data["collection_state"] == "available"
        for command in relevant:
            event = selected.get(command["id"])
            if event is None or command["exit_code"] != 0:
                complete = False
                continue
            mapped = {"Image": event["Image"]}
            if event["CommandLine"]:
                mapped["CommandLine"] = event["CommandLine"]
            else:
                fields.discard("CommandLine")
            cases.append({"id": command["id"], "expected": command["expected"], "event": mapped})
        # A real negative control collected once can be evaluated against every scenario.
        negative = selected.get("other-process-negative")
        if (
            technique != "T1033"
            and negative is not None
            and catalog["other-process-negative"]["exit_code"] == 0
        ):
            mapped = {"Image": negative["Image"]}
            if negative["CommandLine"]:
                mapped["CommandLine"] = negative["CommandLine"]
            cases.append({"id": "other-process-negative", "expected": False, "event": mapped})
        chains.append(
            {
                "id": technique,
                "risk": "lab-process-discovery",
                "technique": technique,
                "telemetry": {
                    "source": "windows.process_creation",
                    "available": True if complete else None,
                    "mapped_fields": sorted(fields) if complete else None,
                },
                "cases": cases if complete else None,
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
        "scope": "windows-lab-" + data["execution_id"],
        "synthetic": data["synthetic"],
        "chains": chains,
    }
