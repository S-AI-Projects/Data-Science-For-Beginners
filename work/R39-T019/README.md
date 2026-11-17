# R39-T019 evidence

Branch `R39-T019` starts from the organisation fork's pinned `main` commit
`4d2ac427ad6f022e73a75c4f46a28bbb7978ec3f`. Earlier tasks are not included.
The assigned remote branch `student/e26b07f0735` was absent.

Run from the repository root:

```bash
python3 -m unittest discover -s 4-Data-Science-Lifecycle/14-Introduction/applied-labs/r39-t019 -p "test_*.py"
python3 work/R39-T019/run_checks.py
git diff --check
```

All 9 tests pass. The runner checks four CLI cases in fresh processes and saves
expected versus actual output, stderr and exit codes. The three valid fixture
scenarios cover Capturing, Processing and Maintaining. A missing asset fails;
an unrelated control requests review.

- [Inputs and expected comparison](fixtures.json)
- [Actual reports and deliberate failure](results.json)
- [Tool versions](versions.json)
- [Reproducible evidence runner](run_checks.py)
- [Lab explanation and limits](../../4-Data-Science-Lifecycle/14-Introduction/applied-labs/r39-t019/README.md)

The comparison takes prefixes of sizes 1, 2 and 3. Each included record has
expected status `pass`, and all actual statuses match. The deterministic metric
is required-field checks: 4, 8 and 12. It counts the four required fields
inspected per complete scenario; it is a work proxy, not elapsed time, cost or
model accuracy. Correctness here means agreement with the rubric's expected
statuses, not real-world accuracy.

The runner also compares the exact default JSON in both README files with the
expected fixture. The deliberate mutation changes a complete result from `pass`
to `review` in a temporary copy. The 9-test suite then fails with assertion
errors and a nonzero exit. The checkout remains unchanged. Any unexpected runner
result raises `AssertionError` and exits nonzero.

Repository AGENTS.md and contribution guidance apply. There is no active
`.github/workflows/` at this base. No notebook, quiz or translation files
changed. New local links resolve, and `git diff --check` passes. Python's
standard library is sufficient; the scenarios are fictional and no service is
mocked or contacted.

The lesson and evidence are separate commits. Omit the entire `work/R39-T019/`
directory from a later upstream proposal after a fit-to-curriculum review. This
coursework PR targets S-AI-Projects.
