"""Save fresh-process results and prove a broken trace invariant fails tests."""

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
LAB = Path("1-Introduction/02-ethics/applied-labs/r39-t014")
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
    require((actual["exit"] == 0) == should_pass, "Unexpected test suite exit")
    if not should_pass:
        require("AssertionError" in actual["stderr"], "No assertion failure")


def main():
    versions = {"python": sys.version, "platform": platform.platform()}
    for tool in ["git", "gh"]:
        versions[tool] = run([tool, "--version"])["stdout"].strip()
    (OUT / "versions.json").write_text(json.dumps(versions, indent=2) + "\n")
    fixtures = json.loads((OUT / "fixtures.json").read_text())
    try:
        for fixture in fixtures:
            args = fixture.get("raw_args")
            if args is None:
                args = ["--a", json.dumps(fixture["a"]),
                        "--b", json.dumps(fixture["b"])]
            actual = run([sys.executable, str(LAB / "example.py")] + args)
            records.append({"fixture": fixture, "actual": actual})
            if "expected" in fixture:
                require(actual["exit"] == 0, fixture["case"] + ": wrong exit")
                require(json.loads(actual["stdout"]) == fixture["expected"],
                        fixture["case"] + ": wrong state or final report")
                require(actual["stderr"] == "", "Unexpected stderr")
            else:
                require(actual["exit"] == 2, fixture["case"] + ": wrong exit")
                require(actual["stdout"] == "", "Invalid report emitted")
                require(fixture["error"] in actual["stderr"], "Wrong error")

        readme = (ROOT / LAB / "README.md").read_text()
        documented = re.search(r"```json\n(.*?)\n```", readme, re.S)
        require(documented is not None, "Missing documented output")
        require(json.loads(documented.group(1)) == fixtures[0]["expected"],
                "README output disagrees with fixture")
        records.append({"case": "documented JSON matches normal fixture",
                        "actual": "pass"})

        actual = run([sys.executable, "-m", "unittest", "discover", "-s",
                      str(LAB), "-p", "test_*.py"])
        records.append({"case": "required discovery", "expected": "9 tests; exit 0",
                        "actual": actual})
        check_suite(actual, True)

        with tempfile.TemporaryDirectory(prefix="r39-t014-") as directory:
            target = Path(directory)
            for filename in ["example.py", "test_example.py"]:
                shutil.copy2(ROOT / LAB / filename, target / filename)
            source = target / "example.py"
            text = source.read_text()
            old = "    final = dict(trace[-1])"
            require(text.count(old) == 1, "Mutation target changed")
            source.write_text(text.replace(old, old + '\n    final["n"] += 1'))
            actual = run([sys.executable, "example.py"], cwd=target)
            records.append({"case": "deliberate wrong final counts",
                            "inputs": {"a": fixtures[0]["a"], "b": fixtures[0]["b"]},
                            "expected_wrong_counts": {"A": 3, "B": 5},
                            "actual": actual})
            require(actual["exit"] == 0, "Mutated example did not run")
            report = json.loads(actual["stdout"])
            require(report["A"]["n"] == 3 and report["B"]["n"] == 5,
                    "Mutation did not produce the wrong counts")
            actual = run([sys.executable, "-m", "unittest", "discover", "-s",
                          ".", "-p", "test_*.py"], cwd=target)
            records.append({"case": "suite rejects broken final-state invariant",
                            "expected": "9 tests; nonzero exit; AssertionError",
                            "actual": actual})
            check_suite(actual, False)
    finally:
        (OUT / "results.json").write_text(json.dumps(records, indent=2) + "\n")
    print("PASS: 10 fixtures, documented JSON, 9 tests, and broken invariant detected")


if __name__ == "__main__":
    main()
