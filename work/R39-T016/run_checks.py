"""Compare the saved baseline with the extraction in fresh Python processes."""

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
LAB = Path("3-Data-Visualization/11-visualization-proportions/applied-labs/r39-t016")
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
        require("AssertionError" in actual["stderr"], "No assertion failure")


def main():
    versions = {"python": sys.version, "platform": platform.platform()}
    for tool in ["git", "gh"]:
        versions[tool] = run([tool, "--version"])["stdout"].strip()
    (OUT / "versions.json").write_text(json.dumps(versions, indent=2) + "\n")
    fixtures = json.loads((OUT / "fixtures.json").read_text())
    try:
        baseline = OUT / "baseline_example.py"
        saved = run(["git", "show", "6976372:" + str(LAB / "example.py")])
        require(saved["exit"] == 0 and saved["stdout"] == baseline.read_text(),
                "Baseline snapshot differs from the original committed version")
        for fixture in fixtures:
            raw = fixture.get("raw", json.dumps(fixture.get("counts")))
            before = run([sys.executable, str(baseline), "--counts", raw])
            after = run([sys.executable, str(LAB / "example.py"), "--counts", raw])
            records.append({"fixture": fixture, "baseline": before, "extracted": after})
            require(before["exit"] == after["exit"], "Exit contract changed")
            require(before["stdout"] == after["stdout"], "Output contract changed")
            if "expected" in fixture:
                require(after["exit"] == 0, fixture["case"] + ": wrong exit")
                require(json.loads(after["stdout"]) == fixture["expected"],
                        fixture["case"] + ": wrong result")
                require(before["stderr"] == after["stderr"] == "", "Unexpected stderr")
            else:
                require(after["exit"] == 2, fixture["case"] + ": wrong failure exit")
                require(after["stdout"] == "", "Invalid report emitted")
                # Usage names differ; the error message is the same contract.
                require("error: " in before["stderr"] and "error: " in after["stderr"],
                        "Missing CLI error")
                require(before["stderr"].split("error: ", 1)[1]
                        == after["stderr"].split("error: ", 1)[1], "Error contract changed")
                require(fixture["error"] in after["stderr"], "Wrong error")

        for document in [ROOT / LAB / "README.md", ROOT / LAB.parents[1] / "README.md"]:
            blocks = re.findall(r"```json\n(.*?)\n```", document.read_text(), re.S)
            require(bool(blocks), "No documented JSON")
            require(json.loads(blocks[0]) == fixtures[0]["expected"],
                    "Documented fixture output changed")
            if len(blocks) > 1:
                require(json.loads(blocks[1]) == fixtures[3]["expected"],
                        "Documented no-data output changed")
        records.append({"case": "documented JSON", "actual": "pass"})

        actual = run([sys.executable, "-m", "unittest", "discover", "-s",
                      str(LAB), "-p", "test_*.py"])
        records.append({"case": "required discovery after extraction",
                        "expected": "9 tests; exit 0", "actual": actual})
        check_suite(actual, True)

        with tempfile.TemporaryDirectory(prefix="r39-t016-") as directory:
            target = Path(directory)
            shutil.copy2(baseline, target / "example.py")
            shutil.copy2(ROOT / LAB / "test_example.py", target / "test_example.py")
            command = [sys.executable, "-m", "unittest", "discover", "-s",
                       ".", "-p", "test_*.py"]
            actual = run(command, cwd=target)
            records.append({"case": "suite against original baseline",
                            "expected": "9 tests; exit 0", "actual": actual})
            check_suite(actual, True)

            source = target / "example.py"
            text = (ROOT / LAB / "example.py").read_text()
            old = "counts[label] / count_total"
            require(text.count(old) == 1, "Mutation target changed")
            source.write_text(text.replace(old, "counts[label] / (count_total + 1)"))
            # Avoid reusing bytecode for the replaced module in the temp folder.
            shutil.rmtree(target / "__pycache__", ignore_errors=True)
            actual = run([sys.executable, "example.py"], cwd=target)
            records.append({"case": "deliberately wrong denominator",
                            "input": {"A": 2, "B": 3},
                            "expected_wrong_shares": {"A": 2 / 6, "B": 3 / 6},
                            "actual": actual})
            require(actual["exit"] == 0, "Wrong example did not run")
            require(json.loads(actual["stdout"])["proportions"] == {"A": 2 / 6, "B": 3 / 6},
                    "Wrong denominator demonstration failed")
            actual = run(command, cwd=target)
            records.append({"case": "suite rejects wrong denominator",
                            "expected": "9 tests; nonzero exit; AssertionError",
                            "actual": actual})
            check_suite(actual, False)
    finally:
        (OUT / "results.json").write_text(json.dumps(records, indent=2) + "\n")
    print("PASS: 10 before/after cases, both 9-test runs, and wrong-denominator failure")


if __name__ == "__main__":
    main()
