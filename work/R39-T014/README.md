# R39-T014 evidence

Branch `R39-T014` starts from organisation-fork main at
`4d2ac427ad6f022e73a75c4f46a28bbb7978ec3f`, matching the pinned lesson source.
It contains no changes from T012 or T013. Neither assigned branch spelling,
`student/e26b07f0735` or `R39-T014/student/e26b07f0735`, exists on the remote.

Reproduce from the repository root:

```bash
python3 -m unittest discover -s 1-Introduction/02-ethics/applied-labs/r39-t014 -p "test_*.py"
python3 work/R39-T014/run_checks.py
git diff --check
```

All 9 tests pass. The runner checks 10 normal, boundary and invalid fixtures in
fresh processes. The normal fixture gives A: n=2, successes=1, rate=0.5;
B: n=4, successes=2, rate=0.5. Empty groups keep an undefined rate (`null`);
`[0]` has an observed rate of 0.0. Missing, boolean, float and out-of-range
outcomes are rejected, as are invalid containers and malformed JSON.

- [Inputs and explicit expected reports, including every state](fixtures.json)
- [Expected versus actual results, commands, stderr and exits](results.json)
- [Tool versions](versions.json)
- [Reproducible check script](run_checks.py)
- [Lab explanation](../../1-Introduction/02-ethics/applied-labs/r39-t014/README.md)

Each trace records the initial state and the state after every observation.
Tests reconstruct each prefix from the original input, check its count, positive
count and rate, then compare the final report with the last snapshot. They cover
all 31 binary sequences of lengths zero through four, as subtests within the
9-test suite. The documented JSON is also checked against the saved normal
fixture.

The failure check inserts `final["n"] += 1` in a disposable copy. The mutated
example reports A n=3 and B n=5 while the trace still ends at 2 and 4. Running
the same suite discovers 9 tests and fails with `AssertionError` and exit 1.
The real lesson files are unchanged by this check. The evidence runner itself
raises `AssertionError` and exits nonzero on an unexpected result.

Repository AGENTS.md and contribution guidance were followed. There are no
active `.github/workflows/` at this pinned base; notebooks, the quiz app and
translations are unchanged. New relative Markdown links and their local anchors
were checked; `git diff --check` passed. Only Python's standard library is needed.

The lesson and evidence are separate commits. A later upstream proposal needs
a fit-to-curriculum review and should use only the lesson commit: omit the entire
`work/R39-T014/` directory. This coursework PR targets S-AI-Projects.
