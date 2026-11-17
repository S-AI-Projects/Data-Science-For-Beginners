# R39-T020 evidence

Branch `R39-T020` starts from organisation-fork main at pinned commit
`4d2ac427ad6f022e73a75c4f46a28bbb7978ec3f`. Earlier tasks are not included.
The assigned remote branch `student/e26b07f0735` was absent.

Run from the repository root:

```bash
python3 -m unittest discover -s 1-Introduction/01-defining-data-science/applied-labs/r39-t020 -p "test_*.py"
python3 work/R39-T020/run_checks.py
git diff --check
```

All 12 tests pass. The runner checks four fixture cases in fresh processes,
three applied questions, exact default output in both lesson and lab READMEs,
and a deliberate wrong answer. Each question has a saved input, expected result
and rationale.

- [Scenario fixtures, question answers and expected results](fixtures.json)
- [Actual output, stderr and exit codes](results.json)
- [Tool versions](versions.json)
- [Reproducible checks](run_checks.py)
- [Lab explanation and applied questions](../../1-Introduction/01-defining-data-science/applied-labs/r39-t020/README.md)

The scenarios use the lesson's digital transformation, data processing and IoT
topics. A complete scenario passes; omitting its asset fails; an unlisted
threat/control pair requests review. Applied answers are: predict `pass`,
diagnose missing asset as `fail`, and send an unlisted pair to `review`. Each
answer is checked by calling the actual local rubric and by running the matching
CLI question in a fresh process.

The failure demonstration changes the successful result to `review` in a
temporary copy. Tests then reject the prediction and complete scenarios; the
same 12-test suite exits nonzero with assertion failures. The source checkout
stays unchanged. Any unexpected check raises `AssertionError` and makes the
runner exit nonzero.

Repository AGENTS.md and contribution guidance apply. The pinned base has no
active `.github/workflows/`. No notebooks, quizzes or translations changed.
New local links resolve and `git diff --check` passes. Python's standard library
is sufficient. The cases are fictional and do not simulate or contact a service.

The lesson and evidence are separate commits. Omit all of `work/R39-T020/` from
a later upstream proposal after fit-to-curriculum review. This coursework PR
targets S-AI-Projects.
