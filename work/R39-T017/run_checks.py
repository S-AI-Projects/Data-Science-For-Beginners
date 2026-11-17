"""Record fresh-process fixtures and execute the published worked example."""

import json
from pathlib import Path
import platform
import re
import shlex
import shutil
import subprocess
import sys
import tempfile


OUT = Path(__file__).resolve().parent
ROOT = OUT.parents[1]
LAB = Path("4-Data-Science-Lifecycle/14-Introduction/applied-labs/r39-t017")
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
        require("FAIL: test_exact_readme_worked_example_is_a_regression" in actual["stderr"],
                "The exact worked-example regression did not fail")


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
        records.append({"case": "saved scenario inputs", "expected": fixture["scenarios"],
                        "actual": actual})
        require(actual["exit"] == 0, "Could not read scenarios")
        require(json.loads(actual["stdout"]) == fixture["scenarios"], "Fixture changed")
        for case in fixture["cases"]:
            actual = run([sys.executable, str(LAB / "example.py")] + case["args"])
            records.append({"fixture": case, "actual": actual})
            require(actual["exit"] == case["expected_exit"], case["case"] + ": wrong exit")
            if "expected_results" in case:
                require(json.loads(actual["stdout"]) == {"results": case["expected_results"]},
                        case["case"] + ": wrong rubric result")
                require(actual["stderr"] == "", "Unexpected stderr")
            else:
                require(actual["stdout"] == "", "Invalid report emitted")
                require(case["expected_error"] in actual["stderr"], "Wrong error")

        readme = (ROOT / LAB / "README.md").read_text()

        def block(name, language):
            match = re.search(r"<!-- " + name + r" -->\s*```" + language
                              + r"\n(.*?)\n```", readme, re.S)
            require(match is not None, "Missing worked-example block")
            return match.group(1)

        require(json.loads(block("worked-input", "json")) == fixture["worked_input"],
                "Worked input changed")
        command = shlex.split(block("worked-command", "bash"))
        require(command[:3] == ["python3", str(LAB / "example.py"), "--scenario"]
                and len(command) == 4, "Worked command changed")
        require(json.loads(command[3]) == fixture["worked_input"], "Command input changed")
        expected_stdout = block("worked-output", "json") + "\n"
        require(json.loads(expected_stdout) == fixture["worked_expected"],
                "Worked output changed")
        actual = run(command)
        records.append({"case": "exact published worked example",
                        "input": fixture["worked_input"],
                        "expected_stdout": expected_stdout, "expected_exit": 0,
                        "actual": actual})
        require(actual["exit"] == 0 and actual["stdout"] == expected_stdout
                and actual["stderr"] == "", "Worked example regression failed")

        for document in [ROOT / LAB / "README.md", ROOT / LAB.parents[1] / "README.md"]:
            match = re.search(r"```json\n(.*?)\n```", document.read_text(), re.S)
            require(match is not None, "No documented default output")
            require(json.loads(match.group(1)) == {
                "results": fixture["cases"][0]["expected_results"]
            }, "Default output in README changed")

        actual = run([sys.executable, "-m", "unittest", "discover", "-s",
                      str(LAB), "-p", "test_*.py"])
        records.append({"case": "required discovery", "expected": "9 tests; exit 0",
                        "actual": actual})
        check_suite(actual, True)

        with tempfile.TemporaryDirectory(prefix="r39-t017-") as directory:
            temp_root = Path(directory)
            target = temp_root / LAB
            target.mkdir(parents=True)
            for filename in ["example.py", "test_example.py", "README.md"]:
                shutil.copy2(ROOT / LAB / filename, target / filename)
            source = target / "example.py"
            text = source.read_text()
            old = '    return {"status": "pass", "issues": []}'
            require(text.count(old) == 1, "Mutation target changed")
            source.write_text(text.replace(old, '    return {"status": "fail", "issues": []}'))
            actual = run(command, cwd=temp_root)
            records.append({"case": "deliberately wrong worked result",
                            "expected_wrong_exit": 1, "actual": actual})
            require(actual["exit"] == 1, "Wrong-result example did not fail")
            require(json.loads(actual["stdout"])["results"][0]["status"] == "fail",
                    "Wrong result was not produced")
            actual = run([sys.executable, "-m", "unittest", "discover", "-s",
                          str(LAB), "-p", "test_*.py"], cwd=temp_root)
            records.append({"case": "exact regression rejects wrong worked result",
                            "expected": "9 tests; nonzero exit; specific regression failure",
                            "actual": actual})
            check_suite(actual, False)
    finally:
        (OUT / "results.json").write_text(json.dumps(records, indent=2) + "\n")
    print("PASS: 9 CLI cases, exact worked example, 9 tests, and regression failure")


if __name__ == "__main__":
    main()
