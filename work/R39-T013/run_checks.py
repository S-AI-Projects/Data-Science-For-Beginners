"""Run local fixtures, discovery and an isolated leakage mutation check."""

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
LAB = Path("2-Working-With-Data/08-data-preparation/applied-labs/r39-t013")
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
        require("AssertionError" in actual["stderr"], "Missing assertion failure")


def main():
    versions = {"python": sys.version, "platform": platform.platform()}
    for tool in ["git", "gh"]:
        versions[tool] = run([tool, "--version"])["stdout"].strip()
    (OUT / "versions.json").write_text(json.dumps(versions, indent=2) + "\n")
    fixtures = json.loads((OUT / "fixtures.json").read_text())
    try:
        for fixture in fixtures:
            command = [sys.executable, str(LAB / "example.py"),
                       "--training", json.dumps(fixture["training"]),
                       "--validation", json.dumps(fixture["validation"])]
            actual = run(command)
            records.append({"fixture": fixture, "actual": actual})
            if "expected" in fixture:
                require(actual["exit"] == 0, fixture["case"] + ": unexpected failure")
                require(json.loads(actual["stdout"]) == fixture["expected"],
                        fixture["case"] + ": result disagrees with explicit table")
                require(actual["stderr"] == "", "Unexpected stderr")
            else:
                require(actual["exit"] == 2, fixture["case"] + ": wrong exit")
                require(actual["stdout"] == "", "Invalid report emitted")
                require("error: " + fixture["error"] in actual["stderr"],
                        fixture["case"] + ": wrong error")

        actual = run([sys.executable, "-m", "unittest", "discover", "-s",
                      str(LAB), "-p", "test_*.py"])
        records.append({"case": "required discovery", "expected": "9 tests; exit 0",
                        "actual": actual})
        check_suite(actual, True)

        with tempfile.TemporaryDirectory(prefix="r39-t013-") as directory:
            target = Path(directory)
            for filename in ["example.py", "test_example.py"]:
                shutil.copy2(ROOT / LAB / filename, target / filename)
            source = target / "example.py"
            text = source.read_text()
            old = "    return [training_mean if value is None else value for value in values]"
            require(text.count(old) == 1, "Mutation target changed")
            wrong = ("    if any(value is not None for value in values):\n"
                     "        training_mean = fit_mean(values)\n" + old)
            source.write_text(text.replace(old, wrong))
            actual = run([sys.executable, "example.py"], cwd=target)
            expected_wrong = {"training_mean": 3, "validation": [100, 100]}
            records.append({"case": "deliberate validation refit",
                            "inputs": fixtures[0], "expected_wrong": expected_wrong,
                            "actual": actual})
            require(actual["exit"] == 0, "Mutation did not run")
            require(json.loads(actual["stdout"]) == expected_wrong,
                    "Mutation did not reproduce the leakage error")
            actual = run([sys.executable, "-m", "unittest", "discover", "-s",
                          ".", "-p", "test_*.py"], cwd=target)
            records.append({"case": "tests reject validation refit",
                            "expected": "9 tests; nonzero exit; AssertionError",
                            "actual": actual})
            check_suite(actual, False)
    finally:
        (OUT / "results.json").write_text(json.dumps(records, indent=2) + "\n")
    print("PASS: 14 fixtures, 9 tests, and validation-refit failure detected")


if __name__ == "__main__":
    main()
