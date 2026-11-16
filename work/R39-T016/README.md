# R39-T016 evidence

Branch `R39-T016` starts from organisation-fork main at pinned commit
`4d2ac427ad6f022e73a75c4f46a28bbb7978ec3f`. No previous task changes are
included. The assigned remote branch `student/e26b07f0735` was absent.

The baseline was implemented, tested and committed first as `6976372`. Its
inline count validation was then extracted into the named `validate_counts`
helper. The normalization, no-data policy and public error contract did not
change. The test module retains the original baseline for comparison.

Run from the repository root:

```bash
python3 -m unittest discover -s 3-Data-Visualization/11-visualization-proportions/applied-labs/r39-t016 -p "test_*.py"
python3 work/R39-T016/run_checks.py
git diff --check
```

All 9 tests passed before and after extraction. The runner checks 10 fixture
cases through both actual scripts in fresh processes, including normal,
smallest positive, mixed zero/positive, all-zero, empty and invalid inputs.
It requires identical output, exit status and error messages, as well as literal
expected results. Both versions pass the 9-test suite independently.

- [Inputs and expected results](fixtures.json)
- [Baseline versus extracted results, commands, stderr and exits](results.json)
- [Original baseline script](baseline_example.py)
- [Initial baseline fixture output](baseline_run.json)
- [Exact extraction diff](extraction.diff)
- [Tool versions](versions.json)
- [Reproducible checks](run_checks.py)
- [Lesson lab](../../3-Data-Visualization/11-visualization-proportions/applied-labs/r39-t016/README.md)

The runner verifies that the baseline snapshot matches its original Git commit
and that both README output blocks match saved expected results. The main
fixture is A=2, B=3: denominator 5, shares 0.4 and 0.6, total 1.0. Empty or
all-zero counts return `no-data`, empty shares and an undefined total (`null`).
Negative and missing counts are rejected.

The deliberate failure changes the extracted implementation's denominator to
`count_total + 1` in a temporary directory. The fixture then gives 2/6 and 3/6,
and the same suite fails with assertions and exit 1 after discovering 9 tests.
The real source stays unchanged. Any unexpected result raises `AssertionError`
and makes the evidence runner exit nonzero.

Repository AGENTS.md and contribution guidance apply. This pinned base has no
active `.github/workflows/`. No notebook, quiz, translation or external service
was changed. New relative Markdown links resolve; `git diff --check` passed.
Only Python's standard library is needed.

The two lesson commits (baseline, then extraction/documentation) are separate
from the coursework evidence commit. For a later upstream branch, first obtain
a fit-to-curriculum review, use only the lesson commits and omit the entire
`work/R39-T016/` directory. The coursework PR targets S-AI-Projects.
