"""Reproduce coursework evidence; raise on any unexpected result."""

import json
from pathlib import Path
import platform
import re
import shutil
import subprocess
import sys
import tempfile


ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).resolve().parent
LAB = Path("4-Data-Science-Lifecycle/16-communication/applied-labs/r39-t012")
records = []


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def run(command, cwd=ROOT):
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True)
    return {"command": command, "exit": result.returncode,
            "stdout": result.stdout, "stderr": result.stderr}


def check_cli(name, args, expected, exit_code=0):
    actual = run([sys.executable, str(LAB / "example.py")] + args)
    records.append({"case": name, "inputs": args,
                    "expected": {"report": expected, "exit": exit_code},
                    "actual": actual})
    require(actual["exit"] == exit_code, name + ": wrong exit")
    if exit_code == 0:
        require(json.loads(actual["stdout"]) == expected, name + ": wrong report")
        require(actual["stderr"] == "", name + ": unexpected error")
    else:
        require(actual["stdout"] == "", name + ": invalid report emitted")
        require("error:" in actual["stderr"], name + ": missing error")


def check_suite(result, should_pass):
    match = re.search(r"Ran (\d+) tests?", result["stderr"])
    require(match is not None and int(match.group(1)) > 0, "No tests executed")
    require((result["exit"] == 0) == should_pass, "Unexpected suite exit")
    if not should_pass:
        require("AssertionError" in result["stderr"], "No assertion failure")


def main():
    versions = {"python": sys.version, "platform": platform.platform()}
    for tool in ["git", "gh"]:
        versions[tool] = run([tool, "--version"])["stdout"].strip()
    (OUT / "versions.json").write_text(json.dumps(versions, indent=2) + "\n")
    try:
        check_cli("normal", [],
                  {"counts": {"A": 2, "B": 1, "C": 3}, "total": 6})
        check_cli("filtered", ["--include", '["A","B"]'],
                  {"counts": {"A": 2, "B": 1}, "total": 3})
        check_cli("smallest nonempty", ["--rows", '["A"]'],
                  {"counts": {"A": 1}, "total": 1})
        for name, args in [
            ("empty data", ["--rows", "[]"]),
            ("empty filter", ["--include", "[]"]),
            ("no matches", ["--include", '["Z"]']),
        ]:
            check_cli(name, args, {"counts": {}, "total": 0})
        for name, args in [
            ("blank label", ["--rows", '[""]']),
            ("whitespace label", ["--rows", '[" "]']),
            ("non-string label", ["--rows", "[1]"]),
            ("null label", ["--rows", "[null]"]),
            ("invalid container", ["--rows", "null"]),
            ("invalid filter", ["--include", "null"]),
            ("malformed JSON", ["--rows", "["]),
            ("hidden invalid", ["--rows", '["A",""]',
                                "--include", '["A"]']),
        ]:
            check_cli(name, args, None, 2)
        command = [sys.executable, "-m", "unittest", "discover", "-s",
                   str(LAB), "-p", "test_*.py"]
        actual = run(command)
        records.append({"case": "required discovery", "expected": "9 tests; exit 0",
                        "actual": actual})
        check_suite(actual, True)
        require("Ran 9 tests" in actual["stderr"], "Unexpected test count")

        # Mutate only a disposable copy: prove the tests catch a wrong total.
        with tempfile.TemporaryDirectory(prefix="r39-t012-") as directory:
            target = Path(directory)
            for filename in ["example.py", "test_example.py"]:
                shutil.copy2(ROOT / LAB / filename, target / filename)
            source = target / "example.py"
            text = source.read_text()
            old = '"total": sum(counts.values())'
            require(text.count(old) == 1, "Mutation target changed")
            source.write_text(text.replace(old, '"total": sum(counts.values()) + 1'))
            actual = run([sys.executable, "-m", "unittest", "discover", "-s",
                          ".", "-p", "test_*.py"], cwd=target)
            records.append({"case": "deliberate wrong result",
                            "inputs": "temporary copy: total = correct total + 1",
                            "expected": "nonzero exit; AssertionError; nonzero tests",
                            "actual": actual})
            check_suite(actual, False)
    finally:
        (OUT / "results.json").write_text(json.dumps(records, indent=2) + "\n")
    print("PASS: fresh-process fixtures, 9 tests, and deliberate failure detected")


if __name__ == "__main__":
    main()
