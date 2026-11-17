# R39-T017 evidence

Branch `R39-T017` starts from organisation-fork main at pinned commit
`4d2ac427ad6f022e73a75c4f46a28bbb7978ec3f`. Earlier task changes are not
included. The remote has neither `student/e26b07f0735` nor
`R39-T017/student/e26b07f0735`, so this task uses its own branch from main.

Run from the repository root:

```bash
python3 -m unittest discover -s 4-Data-Science-Lifecycle/14-Introduction/applied-labs/r39-t017 -p "test_*.py"
python3 work/R39-T017/run_checks.py
git diff --check
```

All 9 tests pass. The runner checks 9 normal, boundary and invalid CLI cases in
fresh processes, then executes the exact published worked-example command as
an additional check. It also compares the saved scenario inputs and both README
default output blocks with the fixture.

- [Three scenarios, worked input and expected results](fixtures.json)
- [Actual output, stderr, commands and exits](results.json)
- [Tool versions](versions.json)
- [Reproducible checks](run_checks.py)
- [Published worked explanation](../../4-Data-Science-Lifecycle/14-Introduction/applied-labs/r39-t017/README.md)

The scenarios relate to **Maintaining / Securing the Data**: departed-account
access, unauthorized edits and exposed stored data. A complete record with a
listed threat/control pair passes the structural rubric. A missing asset fails;
an unrelated or unknown pair requests review. Thin but nonblank text can pass,
which demonstrates why a human must still judge explanations and evidence.

The regression test reads the marked input, command and expected output from
the lab README. It requires the input to match a literal expected object, runs
the documented argv directly from the repository root, and compares exact
stdout, empty stderr and exit 0. It does not generate its expected answer with
the checker.

The deliberate failure changes only a temporary copy of the checker so that a
complete record returns `fail`. The worked command then exits 1. The same suite
still discovers 9 tests, exits 1 with assertion failures, and specifically names
`test_exact_readme_worked_example_is_a_regression` as a failing test. Production
files are not changed. Any unexpected outcome raises `AssertionError` and gives
the evidence runner a nonzero exit.

Repository AGENTS.md and contribution guidance apply. The pinned base has no
active `.github/workflows/`; quiz, notebook and translation files are unchanged.
New local Markdown links resolve and `git diff --check` passed. Everything runs
with Python's standard library and fictional local inputs.

The lesson and evidence are separate commits. Omit the entire `work/R39-T017/`
directory from a later upstream branch after a fit-to-curriculum review. This
coursework PR targets S-AI-Projects.
