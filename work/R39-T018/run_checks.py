"""Record rubric and recovery cases; prove the documented test catches a bug."""

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
LAB = Path("1-Introduction/03-defining-data/applied-labs/r39-t018")
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
    require((actual["exit"] == 0) == should_pass, "Unexpected unittest exit")
    if not should_pass:
        require("AssertionError" in actual["stderr"], "Missing assertion failure")
        require("FAIL: test_documented_invalid_then_valid_sequence_recovers"
                in actual["stderr"], "Recovery regression was not the failing test")


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
        records.append({"case": "fixture inputs", "expected": fixture["scenarios"],
                        "actual": actual})
        require(actual["exit"] == 0, "Could not load scenario fixture")
        require(json.loads(actual["stdout"]) == fixture["scenarios"], "Fixture differs")

        for case in fixture["cases"]:
            actual = run([sys.executable, str(LAB / "example.py")] + case["args"])
            records.append({"fixture": case, "actual": actual})
            require(actual["exit"] == case["expected_exit"], case["case"] + ": wrong exit")
            if "expected" in case:
                require(json.loads(actual["stdout"]) == case["expected"],
                        case["case"] + ": unexpected report")
                require(actual["stderr"] == "", "Unexpected stderr")
            else:
                require(actual["stdout"] == "", "Invalid command produced a report")
                require(case["error"] in actual["stderr"], "Wrong error")

        readme = (ROOT / LAB / "README.md").read_text()

        def block(name, language):
            match = re.search(r"<!-- " + name + r" -->\s*```" + language
                              + r"\n(.*?)\n```", readme, re.S)
            require(match is not None, "Missing documented recovery block")
            return match.group(1)

        command = shlex.split(block("recovery-command", "bash"))
        require(command[:3] == ["python3", str(LAB / "example.py"), "--sequence"]
                and len(command) == 4, "Recovery command changed")
        require(json.loads(command[3]) == fixture["recovery_input"],
                "Recovery input changed")
        expected_stdout = block("recovery-output", "json") + "\n"
        require(json.loads(expected_stdout) == fixture["recovery_expected"],
                "Recovery expected output changed")
        actual = run(command)
        records.append({"case": "exact documented recovery command",
                        "input": fixture["recovery_input"],
                        "expected": {"stdout": expected_stdout, "exit": 1, "stderr": ""},
                        "actual": actual})
        require(actual["stdout"] == expected_stdout and actual["exit"] == 1
                and actual["stderr"] == "", "Recovery example mismatch")

        for document in [ROOT / LAB / "README.md", ROOT / LAB.parents[1] / "README.md"]:
            match = re.search(r"```json\n(.*?)\n```", document.read_text(), re.S)
            require(match is not None, "Missing documented default output")
            require(json.loads(match.group(1)) == fixture["cases"][0]["expected"],
                    "README default output differs from fixture")

        actual = run([sys.executable, "-m", "unittest", "discover", "-s",
                      str(LAB), "-p", "test_*.py"])
        records.append({"case": "required discovery", "expected": "10 tests; exit 0",
                        "actual": actual})
        check_suite(actual, True)

        with tempfile.TemporaryDirectory(prefix="r39-t018-") as directory:
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
            command = shlex.split(block("recovery-command", "bash"))
            actual = run(command, cwd=temp_root)
            records.append({"case": "deliberately wrong result in next valid input",
                            "expected_exit": 1, "actual": actual})
            require(actual["exit"] == 1, "Mutated recovery example did not fail")
            require([item["status"] for item in json.loads(actual["stdout"])["results"]]
                    == ["fail", "fail"], "Mutation did not alter valid recovery result")
            actual = run([sys.executable, "-m", "unittest", "discover", "-s",
                          str(LAB), "-p", "test_*.py"], cwd=temp_root)
            records.append({"case": "suite rejects incorrect recovery result",
                            "expected": "10 tests; nonzero; named recovery regression failure",
                            "actual": actual})
            check_suite(actual, False)
    finally:
        (OUT / "results.json").write_text(json.dumps(records, indent=2) + "\n")
    print("PASS: 9 fresh-process cases, exact recovery command, 10 tests, deliberate failure")


if __name__ == "__main__":
    main()
