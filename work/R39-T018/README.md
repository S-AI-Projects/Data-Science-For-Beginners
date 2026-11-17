# R39-T018 evidence

Branch `R39-T018` starts at organisation-fork main, pinned commit
`4d2ac427ad6f022e73a75c4f46a28bbb7978ec3f`. Earlier task changes are not
included. The assigned remote branch `student/e26b07f0735` was absent.

From the repository root, run:

```bash
python3 -m unittest discover -s 1-Introduction/03-defining-data/applied-labs/r39-t018 -p "test_*.py"
python3 work/R39-T018/run_checks.py
git diff --check
```

All 10 tests pass. The runner checks 9 cases in fresh processes, compares the
saved scenario input with the code fixture, and executes the exact documented
failure-and-recovery command. The invalid first record omits `asset`; it reports
`fail` with `missing or invalid: asset`. The next complete record reports `pass`.
The command exits 1 overall because at least one input failed, while preserving
both outputs and continuing to process the next input.

- [Scenario inputs and expected results](fixtures.json)
- [Expected versus actual output, stderr and exits](results.json)
- [Tool versions](versions.json)
- [Reproducible check script](run_checks.py)
- [Worked example and recovery explanation](../../1-Introduction/03-defining-data/applied-labs/r39-t018/README.md)

The default scenarios cover structured customer and sensor data, plus email as
a data source. One complete scenario passes, the missing-asset scenario fails,
and an unrelated threat/control pair requests review. Human review judges
explanations and evidence; a structural pass does not establish a sound control
or security effectiveness.

The regression test reads its input, command and expected output from the lab
README, executes that command in a fresh process and compares stdout exactly,
along with stderr and exit code. The test does not ask the implementation to
generate its own expected answer.

The failure check changes the valid result to `fail` in a temporary copy. The
next valid input then fails too. The exact documented regression test is required
to fail in a 10-test run with a nonzero exit and an `AssertionError`. The source
checkout remains unchanged. Any unexpected check result raises `AssertionError`
and makes the evidence runner exit nonzero.

Repository AGENTS.md and contribution guidance apply. There is no active
`.github/workflows/` at this pinned base. No quiz, notebook or translation files
were changed. New local links resolve, the lesson default output matches the
fixture, and `git diff --check` passes. Only Python's standard library is used;
there is no mock or real service call.

The lesson change and coursework evidence are separate commits. Omit the entire
`work/R39-T018/` directory from any later upstream branch after a curriculum-fit
review. The coursework PR targets S-AI-Projects.
