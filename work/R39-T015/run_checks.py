"""Reproduce local-adapter evidence; fail on any unexpected check result."""

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
LAB = Path("6-Data-Science-In-Wild/20-Real-World-Examples/applied-labs/r39-t015")
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
    require(match is not None and int(match.group(1)) == 10,
            "Expected 10 discovered tests")
    require((actual["exit"] == 0) == should_pass, "Unexpected test suite exit")
    if not should_pass:
        require("AssertionError" in actual["stderr"], "No assertion failure")


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
        records.append({"case": "fixture snapshot", "expected": fixture["scenarios"],
                        "actual": actual})
        require(actual["exit"] == 0, "Could not read fixture")
        require(json.loads(actual["stdout"]) == fixture["scenarios"],
                "Saved input fixture differs from example")
        for case in fixture["cases"]:
            actual = run([sys.executable, str(LAB / "example.py")] + case["args"])
            records.append({"fixture": case, "actual": actual})
            require(actual["exit"] == case["expected_exit"],
                    case["case"] + ": wrong exit")
            if "expected_results" in case:
                expected = {"adapter": "deterministic-local-mock",
                            "results": case["expected_results"]}
                require(json.loads(actual["stdout"]) == expected,
                        case["case"] + ": wrong rubric result")
                require(actual["stderr"] == "", "Unexpected stderr")
            else:
                require(actual["stdout"] == "", "Invalid report emitted")
                require(case["expected_error"] in actual["stderr"], "Wrong error")

        for readme in [ROOT / LAB / "README.md", ROOT / LAB.parents[1] / "README.md"]:
            documented = re.search(r"```json\n(.*?)\n```", readme.read_text(), re.S)
            require(documented is not None, "Missing documented output")
            require(json.loads(documented.group(1)) == {
                "adapter": "deterministic-local-mock",
                "results": fixture["cases"][0]["expected_results"],
            }, "README output differs from fixture")
        records.append({"case": "lesson and lab documented JSON", "actual": "pass"})

        actual = run([sys.executable, "-m", "unittest", "discover", "-s",
                      str(LAB), "-p", "test_*.py"])
        records.append({"case": "required discovery", "expected": "10 tests; exit 0",
                        "actual": actual})
        check_suite(actual, True)

        with tempfile.TemporaryDirectory(prefix="r39-t015-") as directory:
            target = Path(directory)
            for filename in ["example.py", "test_example.py"]:
                shutil.copy2(ROOT / LAB / filename, target / filename)
            source = target / "example.py"
            text = source.read_text()
            old = "    return PAIRS[threat] == control"
            require(text.count(old) == 1, "Mutation target changed")
            source.write_text(text.replace(old, "    return True"))
            actual = run([sys.executable, "example.py", "--case", "unrelated-control"],
                         cwd=target)
            records.append({"case": "deliberate wrong adapter result",
                            "input": "clinic threat unauthorized_access; control backups",
                            "expected_wrong_status": "pass", "actual": actual})
            require(actual["exit"] == 0, "Mutation did not incorrectly pass")
            require(json.loads(actual["stdout"])["results"][0]["status"] == "pass",
                    "Wrong-result demonstration failed")
            actual = run([sys.executable, "-m", "unittest", "discover", "-s",
                          ".", "-p", "test_*.py"], cwd=target)
            records.append({"case": "suite rejects always-true adapter",
                            "expected": "10 tests; nonzero exit; AssertionError",
                            "actual": actual})
            check_suite(actual, False)
    finally:
        (OUT / "results.json").write_text(json.dumps(records, indent=2) + "\n")
    print("PASS: 9 CLI cases, 10 tests, documentation and wrong-adapter failure")


if __name__ == "__main__":
    main()
