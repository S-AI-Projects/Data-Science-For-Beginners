This adds a small count-to-proportion example to the proportions lesson. Counts
A=2, B=3 use denominator 5 and produce A=0.4, B=0.6, total=1.0. Labels stay
paired with their values.

The zero-total policy is explicit: empty or all-zero counts return `no-data`,
empty proportions and an undefined total (`null`). Negative counts are rejected,
as are missing and non-integer counts. A zero category is a defined share of zero
only when the overall denominator is positive.

The first commit adds a correct, tested baseline. The next extracts one named
responsibility, `validate_counts`, keeping the normalization and public contract
unchanged. Tests preserve the inline baseline and compare both versions with
literal expectations. This is a small behavior-preserving refactor, with no
performance claim.

Checks run from the repository root:

```bash
python3 -m unittest discover -s 3-Data-Visualization/11-visualization-proportions/applied-labs/r39-t016 -p "test_*.py"
python3 work/R39-T016/run_checks.py
git diff --check
```

All 9 tests pass before and after extraction. Ten normal, boundary and invalid
fixtures run through both scripts in fresh processes, checking expected outputs,
errors and exit codes. Both README output examples agree with the fixture.
New local links resolve.

The failure check changes the denominator to `count_total + 1` in a temporary
copy, confirms the wrong shares of 2/6 and 3/6, and verifies that the same 9-test
suite fails with assertions and exit 1. The production source is untouched.

Evidence:

- [Inputs and expected results](https://github.com/shashank-injeti/Data-Science-For-Beginners/blob/R39-T016/work/R39-T016/fixtures.json)
- [Before/after results and deliberate failure](https://github.com/shashank-injeti/Data-Science-For-Beginners/blob/R39-T016/work/R39-T016/results.json)
- [Baseline snapshot](https://github.com/shashank-injeti/Data-Science-For-Beginners/blob/R39-T016/work/R39-T016/baseline_example.py)
- [Extraction diff](https://github.com/shashank-injeti/Data-Science-For-Beginners/blob/R39-T016/work/R39-T016/extraction.diff)
- [Tool versions](https://github.com/shashank-injeti/Data-Science-For-Beginners/blob/R39-T016/work/R39-T016/versions.json)
- [Check script](https://github.com/shashank-injeti/Data-Science-For-Beginners/blob/R39-T016/work/R39-T016/run_checks.py)

The lab needs Python 3.7+, its standard library and a checkout. It uses real
arithmetic on synthetic counts, with no charting dependency, mocked service,
model, provider or device. It does not establish the completeness of a real
dataset or population proportions.

This PR targets the **S-AI-Projects fork** on independent branch `R39-T016`.
The assigned student branch was absent, so it starts at pinned main. Earlier
tasks are not included. The two lesson commits are separate from coursework
evidence; omit `work/R39-T016/` from any later upstream proposal after a
curriculum-fit review. No active CI workflow exists at this base, and notebook,
quiz and translation files are unchanged.
