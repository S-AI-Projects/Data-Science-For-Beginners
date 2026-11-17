"""Save comparison cases and prove the suite rejects an incorrect status."""

import json
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import tempfile


OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
LAB = Path("4-Data-Science-Lifecycle/14-Introduction/applied-labs/r39-t019")
records = []


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def run(command, cwd=ROOT):
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True)
    return {"command": command, "exit": result.returncode,
            "stdout": result.stdout, "stderr": result.stderr}


def check_suite(actual, should_pass):
    match = re.search(r"Ran (\d+) tests?", actual["stderr"])
    require(match is not None and int(match.group(1)) == 9,
            "Expected 9 discovered tests")
    require((actual["exit"] == 0) == should_pass, "Unexpected suite exit")
    if not should_pass:
        require("AssertionError" in actual["stderr"], "No assertion failures reported")


def main():
    versions = {"python": sys.version, "platform": platform.platform()}
    for tool in ["git", "gh"]:
        versions[tool] = run([tool, "--version"])["stdout"].strip()
    (OUT / "versions.json").write_text(json.dumps(versions, indent=2) + "\n")
    fixture = json.loads((OUT / "fixtures.json").read_text())
    try:
        actual = run([sys.executable, "-c",
                      "import json; from example import SCENARIOS; "
                      "print(json.dumps(SCENARIOS))"], cwd=ROOT / LAB)
        records.append({"case": "saved input fixture", "expected": fixture["scenarios"],
                        "actual": actual})
        require(actual["exit"] == 0, "Unable to load fixture")
        require(json.loads(actual["stdout"]) == fixture["scenarios"], "Input fixture differs")

        for case in fixture["cases"]:
            actual = run([sys.executable, str(LAB / "example.py")] + case["args"])
            records.append({"fixture": case, "actual": actual})
            require(actual["exit"] == case["expected_exit"], case["case"] + ": wrong exit")
            if "first_status" in case:
                report = json.loads(actual["stdout"])
                require(report["results"][0]["status"] == case["first_status"],
                        case["case"] + ": wrong first result")
                require(report["size_comparison"] == fixture["size_comparison"],
                        case["case"] + ": size comparison changed")
                require(actual["stderr"] == "", "Unexpected stderr")
            else:
                require(actual["stdout"] == "", "Invalid args produced a report")
                require(case["error"] in actual["stderr"], "Wrong CLI error")

        default = run([sys.executable, str(LAB / "example.py")])
        expected = {"results": [
            {"status": "pass", "issues": [], "field_checks": 4} for _ in range(3)
        ], "size_comparison": fixture["size_comparison"]}
        records.append({"case": "exact expected default report", "expected": expected,
                        "actual": default})
        require(default["exit"] == 0 and json.loads(default["stdout"]) == expected,
                "Default report differs from expected output")

        for document in [ROOT / LAB / "README.md", ROOT / LAB.parents[1] / "README.md"]:
            blocks = re.findall(r"```json\n(.*?)\n```", document.read_text(), re.S)
            require(bool(blocks), "README missing JSON output")
            documented = json.loads(blocks[0])
            require(documented == expected, "README output disagrees with example")

        actual = run([sys.executable, "-m", "unittest", "discover", "-s",
                      str(LAB), "-p", "test_*.py"])
        records.append({"case": "required discovery", "expected": "9 tests; exit 0",
                        "actual": actual})
        check_suite(actual, True)

        with tempfile.TemporaryDirectory(prefix="r39-t019-") as directory:
            target = Path(directory)
            for filename in ["example.py", "test_example.py"]:
                shutil.copy2(ROOT / LAB / filename, target / filename)
            source = target / "example.py"
            text = source.read_text()
            old = 'return {"status": "pass", "issues": [], "field_checks": len(FIELDS)}'
            require(text.count(old) == 1, "Mutation target changed")
            source.write_text(text.replace(old,
                'return {"status": "review", "issues": [], "field_checks": len(FIELDS)}'))
            shutil.rmtree(target / "__pycache__", ignore_errors=True)
            actual = run([sys.executable, "-m", "unittest", "discover", "-s",
                          ".", "-p", "test_*.py"], cwd=target)
            records.append({"case": "deliberate wrong pass status",
                            "expected": "9 tests; nonzero exit; AssertionError",
                            "actual": actual})
            check_suite(actual, False)
    finally:
        (OUT / "results.json").write_text(json.dumps(records, indent=2) + "\n")
    print("PASS: 4 fresh-process cases, three sizes, 9 tests and deliberate failure")


if __name__ == "__main__":
    main()
