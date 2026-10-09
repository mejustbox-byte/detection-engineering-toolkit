"""Детерминированные артефакты; выполнение эмуляции отсутствует."""

from __future__ import annotations

import hashlib
import json
import re
from datetime import date
from importlib.resources import files
from pathlib import Path
from uuid import NAMESPACE_URL, UUID, uuid5

import yaml
from sigma.collection import SigmaCollection

MAX_BYTES = 8 * 1024 * 1024
TECHNIQUE = re.compile(r"T\d{4}(?:\.\d{3})?\Z")


class InputError(ValueError):
    """Ошибка пользовательских данных."""


def load_file(path: Path, kind: str):
    with path.open("rb") as stream:
        data = stream.read(MAX_BYTES + 1)
    if len(data) > MAX_BYTES:
        raise InputError("Размер входа превышает 8 MiB")
    try:
        raw = data.decode("utf-8")
        return json.loads(raw) if kind == "json" else yaml.safe_load(raw)
    except (UnicodeError, ValueError, yaml.YAMLError, RecursionError) as exc:
        raise InputError("Некорректный UTF-8 / JSON / YAML") from exc


def scenarios() -> list[dict]:
    return json.loads(files("detection_toolkit.data").joinpath("scenarios.json").read_text("utf-8"))


def scenario_for(technique: str, scenario_id: str | None = None) -> dict:
    if not isinstance(technique, str) or not TECHNIQUE.fullmatch(technique):
        raise InputError("Ожидается ATT&CK ID вида T1033 или T1059.001")
    candidates = [s for s in scenarios() if s["technique"] == technique]
    if scenario_id is not None:
        candidates = [s for s in candidates if s["id"] == scenario_id]
    if len(candidates) != 1:
        raise InputError("Техника/сценарий не поддерживается или выбор неоднозначен")
    return candidates[0]


def generate_rule(scenario: dict) -> str:
    selection = {"Image|endswith": scenario["image"]}
    if scenario["contains"]:
        selection["CommandLine|contains|all"] = scenario["contains"]
    rule = {
        "title": scenario["name"],
        "id": str(uuid5(NAMESPACE_URL, f"https://detkit.local/scenarios/{scenario['id']}/v1")),
        "status": "experimental",
        "description": "Узкий поведенческий сигнал; не доказывает злонамеренность или покрытие всей техники.",
        "author": "Detection Engineering Toolkit",
        "date": date(2026, 10, 9).isoformat(),
        "references": [
            f"https://attack.mitre.org/techniques/{scenario['technique'].replace('.', '/')}/"
        ],
        "tags": ["attack.discovery", f"attack.{scenario['technique'].lower()}"],
        "logsource": {"product": "windows", "category": "process_creation"},
        "detection": {"selection": selection, "condition": "selection"},
        "falsepositives": scenario["falsepositives"],
        "level": "low",
    }
    result = yaml.safe_dump(rule, allow_unicode=True, sort_keys=False)
    SigmaCollection.from_yaml(result)
    return result


def convert(rule: str, target: str) -> list[str]:
    # Каждый backend получает свежую коллекцию: pipeline изменяет правила.
    collection = SigmaCollection.from_yaml(rule)
    if target == "splunk":
        from sigma.backends.splunk import SplunkBackend
        from sigma.pipelines.splunk import splunk_windows_pipeline

        backend = SplunkBackend(processing_pipeline=splunk_windows_pipeline())
    elif target == "defender":
        from sigma.backends.microsoft365defender import KustoBackend
        from sigma.pipelines.microsoft365defender import microsoft_365_defender_pipeline

        backend = KustoBackend(processing_pipeline=microsoft_365_defender_pipeline())
    else:
        raise InputError("Поддерживаются только splunk и defender")
    return backend.convert(collection)


def atomic_tests(path: Path, technique: str) -> list[dict]:
    if not TECHNIQUE.fullmatch(technique):
        raise InputError("Некорректный ID техники")
    data = load_file(path, "yaml")
    if not isinstance(data, dict) or data.get("attack_technique") != technique:
        raise InputError("Atomic YAML относится к другой технике")
    tests = data.get("atomic_tests")
    if not isinstance(tests, list) or not tests:
        raise InputError("atomic_tests должен быть непустым массивом")
    result = []
    seen = set()
    for item in tests:
        if not isinstance(item, dict):
            raise InputError("Некорректная запись Atomic")
        try:
            guid = str(UUID(item.get("auto_generated_guid", "")))
        except (ValueError, TypeError, AttributeError) as exc:
            raise InputError("Atomic test должен иметь GUID") from exc
        if guid in seen:
            raise InputError("Повторяющийся GUID Atomic")
        seen.add(guid)
        executor = item.get("executor")
        platforms = item.get("supported_platforms")
        if (
            not isinstance(item.get("name"), str)
            or not isinstance(executor, dict)
            or not isinstance(executor.get("name"), str)
            or not isinstance(executor.get("command"), str)
            or not isinstance(platforms, list)
            or not platforms
            or any(not isinstance(p, str) for p in platforms)
        ):
            raise InputError("Неполное описание Atomic test")
        result.append(
            {
                "guid": guid,
                "name": item["name"],
                "platforms": platforms,
                "executor": executor["name"],
                "command": executor["command"],
                "elevation_required": executor.get("elevation_required", False),
                "input_arguments": item.get("input_arguments", {}),
                "dependencies": item.get("dependencies", []),
            }
        )
    return result


def atomic_plan(path: Path, technique: str, guid: str, lab_ack: bool) -> dict:
    try:
        normalized = str(UUID(guid))
    except (ValueError, TypeError, AttributeError) as exc:
        raise InputError("Некорректный GUID") from exc
    selected = [t for t in atomic_tests(path, technique) if t["guid"] == normalized]
    if len(selected) != 1 or "windows" not in selected[0]["platforms"]:
        raise InputError("GUID не найден или тест не поддерживает Windows")
    prefix = f"Invoke-AtomicTest {technique} -TestGuids {normalized}"
    result = {
        "technique": technique,
        "test": selected[0],
        "atomic_yaml_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
        "coverage": "manual_review_required",
        "execution": "not_run",
        "show_details": prefix + " -ShowDetails",
        "check_prerequisites": prefix + " -CheckPrereqs",
        "cleanup": prefix + " -Cleanup",
        "warning": "Проверьте команду, зависимости, входные аргументы и соответствие сценарию. Cleanup также меняет систему.",
    }
    if lab_ack:
        result["execute"] = prefix
    return result


def matches(scenario: dict, event: dict) -> bool:
    image, command = event.get("Image"), event.get("CommandLine")
    if not isinstance(image, str):
        return False
    return image.casefold().endswith(scenario["image"].casefold()) and (
        not scenario["contains"]
        or isinstance(command, str)
        and all(value.casefold() in command.casefold() for value in scenario["contains"])
    )


def fixture_cases(scenario: dict) -> list[dict]:
    image = "C:\\Windows\\System32" + scenario["image"]
    positive = {"Image": image, "CommandLine": image + " " + " ".join(scenario["contains"])}
    cases = [
        {"id": "positive", "expected": True, "event": positive},
        {
            "id": "case-insensitive",
            "expected": True,
            "event": {k: v.upper() for k, v in positive.items()},
        },
        {
            "id": "other-process",
            "expected": False,
            "event": {"Image": "C:\\Windows\\notepad.exe", "CommandLine": "notepad.exe"},
        },
        {"id": "missing-image", "expected": False, "event": {"CommandLine": "whoami"}},
    ]
    if scenario["contains"]:
        cases += [
            {
                "id": "missing-argument",
                "expected": False,
                "event": {"Image": image, "CommandLine": image},
            },
            {"id": "missing-commandline", "expected": False, "event": {"Image": image}},
        ]
    return cases


def validate_cases(scenario: dict, cases: object) -> dict:
    if not isinstance(cases, list) or not cases:
        raise InputError("Нужен непустой массив случаев id/expected/event")
    results, seen = [], set()
    for case in cases:
        if (
            not isinstance(case, dict)
            or not isinstance(case.get("id"), str)
            or type(case.get("expected")) is not bool
            or not isinstance(case.get("event"), dict)
        ):
            raise InputError("Некорректный случай проверки")
        if case["id"] in seen:
            raise InputError("Повторяющийся id случая")
        seen.add(case["id"])
        event = case["event"]
        if any(
            key in event and not isinstance(event[key], str) for key in ("Image", "CommandLine")
        ):
            raise InputError("Image и CommandLine должны быть строками")
        actual = matches(scenario, event)
        results.append(
            {
                "id": case["id"],
                "expected": case["expected"],
                "actual": actual,
                "pass": actual == case["expected"],
            }
        )
    return {
        "scope": "offline_scenario_predicate",
        "passed": all(r["pass"] for r in results),
        "cases": results,
        "siem_execution": "not_run",
        "atomic_execution": "not_run",
        "limitation": "Проверка предиката сценария не исполняет Sigma или SIEM-запрос.",
    }


def bundle(
    technique: str,
    output: Path,
    atomic: Path | None = None,
    guid: str | None = None,
    lab_ack: bool = False,
) -> Path:
    scenario = scenario_for(technique)
    rule = generate_rule(scenario)
    payload = {"rule.yml": rule}
    for target in ("splunk", "defender"):
        payload[f"{target}.txt"] = "\n".join(convert(rule, target)) + "\n"
    cases = fixture_cases(scenario)
    payload["fixtures.json"] = json.dumps(cases, ensure_ascii=False, indent=2) + "\n"
    report = validate_cases(scenario, cases)
    payload["validation.json"] = json.dumps(report, ensure_ascii=False, indent=2) + "\n"
    if (atomic is None) != (guid is None):
        raise InputError("--atomic-file и --test-guid задаются вместе")
    if lab_ack and atomic is None:
        raise InputError("--lab-ack требует конкретного Atomic test")
    plan = (
        atomic_plan(atomic, technique, guid, lab_ack)
        if atomic
        else {"execution": "not_run", "reason": "Atomic YAML и GUID не предоставлены"}
    )
    payload["atomic-plan.json"] = json.dumps(plan, ensure_ascii=False, indent=2) + "\n"
    payload["REPORT.md"] = (
        f"# {scenario['name']}\n\nТехника: {technique}. Правило: experimental.\n\n"
        f"Локальные синтетические случаи: {len(cases)}, результат: pass.\n\n"
        "SIEM и Atomic: **НЕ ВЫПОЛНЕНО**. Полное покрытие техники не заявляется.\n\n"
        "Splunk: Windows process_creation, проверьте source/sourcetype/index и Image/CommandLine. "
        "Defender: DeviceProcessEvents, проверьте onboarding и доставку событий.\n\n"
        "План Atomic требует ручной проверки процедуры и её соответствия условию правила.\n"
    )
    manifest = {
        "version": "0.1.0a1",
        "technique": technique,
        "scenario": scenario["id"],
        "files": {
            name: hashlib.sha256(text.encode()).hexdigest()
            for name, text in sorted(payload.items())
        },
    }
    payload["manifest.json"] = json.dumps(manifest, indent=2) + "\n"
    output.mkdir(parents=True, exist_ok=False)
    for name, text in payload.items():
        with (output / name).open("x", encoding="utf-8", newline="\n") as stream:
            stream.write(text)
    return output
