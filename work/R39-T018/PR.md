This adds three fictional data-description scenarios tied to the lesson's
**Structured Data** and **Sources of Data** sections. Each record describes an
asset, threat, control and residual risk. A small local rubric checks that the
four fields are present and that the threat/control pair is listed.

The lab shows a missing-data case followed by recovery in the same ordered
input sequence. The first record has no `asset` field and returns
`missing or invalid: asset`. The next valid record passes. Both results are
reported, while the command exits 1 overall to preserve the earlier failure.
An unrelated pair requests review. Human review still evaluates the reasoning
and evidence; a structural pass is not a judgment of security effectiveness.

The README publishes the exact input, command and expected output. The regression
test reads those blocks and executes the command in a fresh process. The checker
uses deterministic local code and fictional inputs, with no mocked service,
credentials, model or device. Python 3.7+ and its standard library are sufficient.

Checks run from the repository root:

```bash
python3 -m unittest discover -s 1-Introduction/03-defining-data/applied-labs/r39-t018 -p "test_*.py"
python3 work/R39-T018/run_checks.py
git diff --check
```

All 10 tests pass, including the exact recovery regression. Nine CLI cases run
in fresh processes. The failure check changes the valid result in a temporary
copy, verifies that the next valid record now fails, and confirms that the named
regression test fails with a nonzero suite exit. Saved inputs, expected/actual
results and tool versions are linked below.

- [Inputs and expected outputs](https://github.com/shashank-injeti/Data-Science-For-Beginners/blob/R39-T018/work/R39-T018/fixtures.json)
- [Results and failure demonstration](https://github.com/shashank-injeti/Data-Science-For-Beginners/blob/R39-T018/work/R39-T018/results.json)
- [Tool versions](https://github.com/shashank-injeti/Data-Science-For-Beginners/blob/R39-T018/work/R39-T018/versions.json)
- [Evidence runner](https://github.com/shashank-injeti/Data-Science-For-Beginners/blob/R39-T018/work/R39-T018/run_checks.py)

This PR targets the **S-AI-Projects fork** on independent branch `R39-T018`.
The assigned student branch was absent remotely, so this starts at pinned main.
Earlier tasks are not included. Lesson and coursework evidence are separate
commits; omit `work/R39-T018/` from a later upstream proposal after a
curriculum-fit review. No active CI workflow exists at this base; quiz,
notebook and translation files are unchanged.
