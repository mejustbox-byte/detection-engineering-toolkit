"""CLI без вызовов оболочки и сетевых подключений."""

import argparse
import json
import sys
from pathlib import Path

from opsec_reports.core import ReportError, outcome, write_new
from opsec_reports.core import load as strict_load
from sigma.exceptions import SigmaError

from . import __version__
from .core import (
    InputError,
    atomic_plan,
    atomic_tests,
    bundle,
    convert,
    convert_file,
    doctor,
    generate_rule,
    load_file,
    scenario_for,
    scenarios,
    validate_cases,
    verify_bundle,
)
from .lab_import import normalize as normalize_lab
from .readiness import assess as readiness_assess


def parser():
    root = argparse.ArgumentParser(description="ATT&CK → Sigma → SIEM → план Atomic")
    root.add_argument("--version", action="version", version=__version__)
    commands = root.add_subparsers(dest="command", required=True)
    importer = commands.add_parser(
        "lab-import", help="Validate operator-supplied Windows lab events"
    )
    importer.add_argument("path", type=Path)
    importer.add_argument("--output", type=Path, required=True)
    lab_check = commands.add_parser(
        "lab-check", help="Import and assess Windows lab events offline"
    )
    lab_check.add_argument("path", type=Path)
    lab_check.add_argument("--output", type=Path, required=True)
    lab_check.add_argument("--observed-at", required=True)
    ready = commands.add_parser("readiness", help="Assess offline risk/telemetry/test chains")
    ready.add_argument("path", type=Path)
    ready.add_argument("--observed-at", required=True)
    ready.add_argument("--output", type=Path, required=True)
    ready.add_argument("--max-chains", type=int, default=100)
    ready.add_argument("--maximum-age-days", type=int, default=30)
    commands.add_parser("list", help="Поддерживаемые сценарии")
    commands.add_parser("doctor", help="Check installed data and both conversion backends")
    verify = commands.add_parser("verify-bundle", help="Check bundle SHA256 integrity")
    verify.add_argument("path", type=Path)
    external = commands.add_parser("convert-file", help="Convert a local Sigma YAML file")
    external.add_argument("path", type=Path)
    external.add_argument("--target", choices=("splunk", "defender"), required=True)
    for name in ("rule", "convert", "validate", "bundle", "atomic-list", "atomic-plan"):
        cmd = commands.add_parser(name)
        cmd.add_argument("technique", help="ATT&CK ID")
        if name in ("atomic-list", "atomic-plan", "bundle"):
            cmd.add_argument("--atomic-file", type=Path, required=name != "bundle")
        if name in ("atomic-plan", "bundle"):
            cmd.add_argument(
                "--atomic-commit", help="Full upstream commit SHA (unverified provenance)"
            )
            cmd.add_argument("--test-guid", required=name == "atomic-plan")
            cmd.add_argument(
                "--lab-ack",
                action="store_true",
                help="Разрешить вывод команды запуска для согласованного стенда",
            )
        if name == "bundle":
            cmd.add_argument("--output", type=Path, required=True)
        if name == "convert":
            cmd.add_argument("--target", choices=("splunk", "defender"), required=True)
        if name == "validate":
            cmd.add_argument("--cases", type=Path, required=True)
    return root


def main(argv=None):
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8")
    args = parser().parse_args(argv)
    try:
        if args.command == "lab-check":
            result = readiness_assess(normalize_lab(strict_load(args.path)), args.observed_at)
            write_new(args.output, json.dumps(result, ensure_ascii=False, indent=2) + "\n")
            print("lab_assessment_written; siem_delivery=not_run")
            return outcome(result["assessment"])
        if args.command == "lab-import":
            result = normalize_lab(strict_load(args.path))
            write_new(args.output, json.dumps(result, ensure_ascii=False, indent=2) + "\n")
            print("lab_manifest_normalized; siem_delivery=not_run")
            return 0
        if args.command == "readiness":
            result = readiness_assess(
                strict_load(args.path), args.observed_at, args.max_chains, args.maximum_age_days
            )
            write_new(args.output, json.dumps(result, ensure_ascii=False, indent=2) + "\n")
            print("readiness_result_written")
            return outcome(result["assessment"])
        if args.command == "list":
            result = scenarios()
        elif args.command == "doctor":
            result = doctor()
        elif args.command == "verify-bundle":
            result = verify_bundle(args.path)
        elif args.command == "convert-file":
            print("\n".join(convert_file(args.path, args.target)))
            return 0
        elif args.command == "atomic-list":
            result = atomic_tests(args.atomic_file, args.technique)
        elif args.command == "atomic-plan":
            scenario_for(args.technique)
            result = atomic_plan(
                args.atomic_file, args.technique, args.test_guid, args.lab_ack, args.atomic_commit
            )
        elif args.command == "bundle":
            result = str(
                bundle(
                    args.technique,
                    args.output,
                    args.atomic_file,
                    args.test_guid,
                    args.lab_ack,
                    args.atomic_commit,
                )
            )
        else:
            scenario = scenario_for(args.technique)
            if args.command == "rule":
                print(generate_rule(scenario), end="")
                return 0
            if args.command == "convert":
                print("\n".join(convert(generate_rule(scenario), args.target)))
                return 0
            result = validate_cases(scenario, load_file(args.cases, "json"))
        print(json.dumps(result, ensure_ascii=False, indent=2))
        return 1 if isinstance(result, dict) and result.get("passed") is False else 0
    except ReportError:
        print("invalid_readiness_input_or_output", file=sys.stderr)
        return 3
    except (InputError, OSError, SigmaError, RecursionError) as exc:
        if args.command in ("readiness", "lab-import", "lab-check"):
            print("readiness_input_or_output_unavailable", file=sys.stderr)
            return 3
        print(f"Ошибка: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
