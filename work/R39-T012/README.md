# R39-T012 coursework evidence

Base: `S-AI-Projects/Data-Science-For-Beginners`, `main`, commit
`4d2ac427ad6f022e73a75c4f46a28bbb7978ec3f` (also the task's pinned source).
The assigned remote branch `student/e26b07f0735` was absent; the task branch is
`R39-T012`. This branch targets the organisation fork, not Microsoft upstream.

Reproduce from the repository root:

```bash
python3 -m unittest discover -s 4-Data-Science-Lifecycle/16-communication/applied-labs/r39-t012 -p "test_*.py"
python3 work/R39-T012/run_checks.py
git diff --check
```

The required discovery ran **9 tests**, passed and exited 0. The evidence runner
checks 14 fresh-process CLI scenarios and runs discovery again. Its final check
copies the code and tests to a temporary directory, deliberately adds one to the
reported total, and requires a nonzero unittest exit with `AssertionError` and
a nonzero test count. The original files are never mutated. The runner itself
raises `AssertionError` (nonzero exit) for any unexpected outcome.

- [Inputs, expected versus actual reports, stderr and exits](results.json)
- [Python, platform, Git and GitHub CLI versions](versions.json)
- [Reproducible checks](run_checks.py)
- [Fixture contract and exact boundary decision](../../4-Data-Science-Lifecycle/16-communication/applied-labs/r39-t012/README.md)

The normal input is `["A","A","B","C","C","C"]`: counts A=2, B=1,
C=3, total=6. Filtering to A/B yields A=2, B=1, total=3. The smallest
nonempty dataset `["A"]` totals 1; empty data, an empty filter and no matches
total 0. Blank and non-string labels are invalid even when filtered out.

Repository guidance and the pinned CONTRIBUTING.md were read. No quiz app,
notebook, translation or external service was modified. The repository has no
active `.github/workflows/` at this base; a translation workflow is stored under
`.github/PULL_REQUEST_TEMPLATE/`, not an active workflow. New local Markdown
links were checked against their targets. `git diff --check` passed.

Only the lesson README and its three lab files belong in a later upstream
proposal, after a fit-to-curriculum review. **Omit this entire `work/R39-T012/`
directory from any later upstream branch** (for example, cherry-pick only the
lesson commit). Upstream acceptance is not a requirement for this coursework.
