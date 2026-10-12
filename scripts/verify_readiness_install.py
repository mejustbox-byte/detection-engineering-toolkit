import json
import os
import subprocess
import tempfile
import venv
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
wheel = next((ROOT / "dist").glob("*.whl"))


def run(args, cwd, expected=0):
    result = subprocess.run(args, cwd=cwd, text=True, capture_output=True)
    assert result.returncode == expected, result.stdout + result.stderr


with tempfile.TemporaryDirectory() as directory:
    temp = Path(directory)
    venv.EnvBuilder(with_pip=True).create(temp / "venv")
    bindir = temp / "venv" / ("Scripts" if os.name == "nt" else "bin")
    python = bindir / ("python.exe" if os.name == "nt" else "python")
    run([str(python), "-m", "pip", "install", str(wheel)], temp)
    run([str(python), "-m", "pip", "check"], temp)
    cli = [str(python), "-m", "detection_toolkit.cli"]
    run(cli + ["doctor"], temp)
    run(cli + ["bundle", "T1033", "--output", str(temp / "smoke")], temp)
    run(cli + ["verify-bundle", str(temp / "smoke")], temp)
    out = temp / "readiness.json"
    run(
        cli
        + [
            "readiness",
            str(ROOT / "examples/readiness.synthetic.json"),
            "--observed-at",
            "2026-10-12T00:00:00Z",
            "--output",
            str(out),
        ],
        temp,
        2,
    )
    report = json.loads(out.read_text(encoding="utf-8"))
    assert report["assessment"]["summary"]["not_tested"] == 3
    assert len(report["chains"]) == 3
    assessment = temp / "assessment.json"
    assessment.write_text(json.dumps(report["assessment"]), encoding="utf-8")
    run([str(python), "-m", "opsec_reports", "validate", str(assessment)], temp, 2)
print("Installed wheel doctor, bundle, readiness and report validation passed.")
