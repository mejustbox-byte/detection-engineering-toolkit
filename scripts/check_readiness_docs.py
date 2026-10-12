import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

from opsec_reports.core import validate

ROOT = Path(__file__).resolve().parents[1]
ru = {p.name for p in (ROOT / "docs/ru/readiness").glob("*.md")}
en = {p.name for p in (ROOT / "docs/en/readiness").glob("*.md")}
assert ru == en
for lang in ["ru", "en"]:
    for name in ru:
        p = ROOT / "docs" / lang / "readiness" / name
        text = p.read_text(encoding="utf-8")
        assert text.count("```") % 2 == 0
        for target in re.findall(r"\]\(([^)]+)\)", text):
            if "://" not in target:
                assert (p.parent / target).exists()
for name in ru:
    blocks = [
        re.findall(
            r"```\w*\n(.*?)```",
            (ROOT / "docs" / lang / "readiness" / name).read_text(encoding="utf-8"),
            re.S,
        )
        for lang in ["ru", "en"]
    ]
    assert blocks[0] == blocks[1]
with tempfile.TemporaryDirectory() as tmp:
    out = Path(tmp) / "report.json"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "detection_toolkit.cli",
            "readiness",
            str(ROOT / "examples/readiness.synthetic.json"),
            "--observed-at",
            "2026-10-12T00:00:00Z",
            "--output",
            str(out),
        ],
        capture_output=True,
        text=True,
    )
    assert result.returncode == 2, result.stdout + result.stderr
    report = json.loads(out.read_text(encoding="utf-8"))["assessment"]
    validate(report)
    assert report["summary"]["pass"] == 9 and report["summary"]["not_tested"] == 3
print(f"OK: {len(ru)} readiness RU/EN pairs and executable example")
