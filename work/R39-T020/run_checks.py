"""Save scenario and question checks; demonstrate a deliberately wrong answer."""

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
LAB = Path("1-Introduction/01-defining-data-science/applied-labs/r39-t020")
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
    require(match is not None and int(match.group(1)) == 12,
            "Expected 12 discovered tests")
    require((actual["exit"] == 0) == should_pass, "Unexpected unittest exit")
    if not should_pass:
        require("AssertionError" in actual["stderr"], "Missing assertion failure")


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
        records.append({"case": "scenario fixture", "expected": fixture["scenarios"],
                        "actual": actual})
        require(actual["exit"] == 0, "Could not load scenario fixture")
        require(json.loads(actual["stdout"]) == fixture["scenarios"], "Fixture mismatch")

        for case in fixture["cases"]:
            actual = run([sys.executable, str(LAB / "example.py")] + case["args"])
            records.append({"fixture": case, "actual": actual})
            require(actual["exit"] == case["exit"], case["case"] + ": wrong exit")
            if "first_status" in case:
                require(json.loads(actual["stdout"])["results"][0]["status"]
                        == case["first_status"], case["case"] + ": wrong result")
                require(actual["stderr"] == "", "Unexpected stderr")
            else:
                require(actual["stdout"] == "", "Invalid argument emitted a report")
                require(case["error"] in actual["stderr"], "Wrong CLI error")

        for question, expectation in fixture["questions"].items():
            actual = run([sys.executable, str(LAB / "example.py"),
                          "--question", question])
            expected = {"results": [expectation["expected"]]}
            records.append({"question": question, "input": expectation["input"],
                            "expected": expected, "rationale": expectation["rationale"],
                            "actual": actual})
            expected_exit = {"pass": 0, "fail": 1, "review": 3}[
                expectation["expected"]["status"]]
            require(actual["exit"] == expected_exit, question + ": wrong exit")
            require(json.loads(actual["stdout"]) == expected, question + ": wrong answer")
            require(actual["stderr"] == "", "Unexpected question stderr")

        for document in [ROOT / LAB / "README.md", ROOT / LAB.parents[1] / "README.md"]:
            match = re.search(r"```json\n(.*?)\n```", document.read_text(), re.S)
            require(match is not None, "README missing default JSON output")
            expected = {"results": [{"status": "pass", "issues": []} for _ in range(3)]}
            require(json.loads(match.group(1)) == expected, "Documented output mismatch")

        actual = run([sys.executable, "-m", "unittest", "discover", "-s",
                      str(LAB), "-p", "test_*.py"])
        records.append({"case": "required unittest discovery", "expected": "12 tests; exit 0",
                        "actual": actual})
        check_suite(actual, True)

        with tempfile.TemporaryDirectory(prefix="r39-t020-") as directory:
            target = Path(directory)
            for filename in ["example.py", "test_example.py"]:
                shutil.copy2(ROOT / LAB / filename, target / filename)
            source = target / "example.py"
            text = source.read_text()
            old = '    return {"status": "pass", "issues": []}'
            require(text.count(old) == 1, "Mutation target changed")
            source.write_text(text.replace(old,
                '    return {"status": "review", "issues": []}'))
            shutil.rmtree(target / "__pycache__", ignore_errors=True)
            actual = run([sys.executable, "-m", "unittest", "discover", "-s",
                          ".", "-p", "test_*.py"], cwd=target)
            records.append({"case": "deliberate wrong prediction",
                            "expected": "12 tests; nonzero exit; assertion failures",
                            "actual": actual})
            check_suite(actual, False)
    finally:
        (OUT / "results.json").write_text(json.dumps(records, indent=2) + "\n")
    print("PASS: four CLI cases, three applied answers, 12 tests and deliberate failure")


if __name__ == "__main__":
    main()
