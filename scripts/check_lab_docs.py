import json
import re
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
pairs = [ROOT / "docs" / lang / "lab" for lang in ("ru", "en")]
assert {p.name for p in pairs[0].glob("*.md")} == {p.name for p in pairs[1].glob("*.md")}
for name in ("README.md", "case-template.md"):
    blocks = []
    for folder in pairs:
        p = folder / name
        text = p.read_text(encoding="utf-8")
        assert text.count("```") % 2 == 0
        blocks.append(re.findall(r"```\w*\n(.*?)```", text, re.S))
        for target in re.findall(r"\]\(([^)]+)\)", text):
            if "://" not in target:
                assert (p.parent / target).exists(), target
    assert blocks[0] == blocks[1]
with tempfile.TemporaryDirectory() as tmp:
    output = Path(tmp) / "assessment.json"
    result = subprocess.run(
        [
            sys.executable,
            "-m",
            "detection_toolkit.cli",
            "lab-check",
            str(ROOT / "examples/windows-lab.synthetic.json"),
            "--observed-at",
            "2026-10-13T10:00:20Z",
            "--output",
            str(output),
        ],
        text=True,
        capture_output=True,
    )
    assert result.returncode == 2, result.stdout + result.stderr
    report = json.loads(output.read_text(encoding="utf-8"))
    assert report["assessment"]["summary"]["pass"] == 9
    assert report["assessment"]["summary"]["not_tested"] == 3
print("OK: 2 laboratory RU/EN pairs and synthetic executable example")
