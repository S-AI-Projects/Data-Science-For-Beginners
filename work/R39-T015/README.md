# R39-T015 evidence

Branch `R39-T015` starts at organisation-fork main,
`4d2ac427ad6f022e73a75c4f46a28bbb7978ec3f`, matching the pinned source. It
contains no earlier task changes. The remote has neither assigned branch
spelling: `student/e26b07f0735` nor `R39-T015/student/e26b07f0735`.

Run from the repository root:

```bash
python3 -m unittest discover -s 6-Data-Science-In-Wild/20-Real-World-Examples/applied-labs/r39-t015 -p "test_*.py"
python3 work/R39-T015/run_checks.py
git diff --check
```

All 10 tests pass. The runner checks 9 CLI cases in fresh processes, compares
the three saved fictional scenarios with the code fixture, and verifies the
documented JSON in both the lesson and lab README.

- [Inputs, complete scenarios and expected results](fixtures.json)
- [Actual reports, commands, stderr and exits](results.json)
- [Tool versions](versions.json)
- [Reproducible checks](run_checks.py)
- [Rubric and mock limitations](../../6-Data-Science-In-Wild/20-Real-World-Examples/applied-labs/r39-t015/README.md)

The complete fixture passes (exit 0). Removing its first asset fails (exit 1).
Giving that scenario the unrelated `backups` control requests review (exit 3).
The fixture also includes the minimal complete object, unknown labels, an empty
object, an invalid container, a blank asset and malformed JSON (exit 2).

Unit tests inject a recording callable to verify the exact threat/control inputs
and that its response controls the result. A mock timeout requests review; no
network call is made. Unknown and malformed responses cannot produce a pass.
Incomplete scenarios fail without calling the adapter.

The failure check copies the code and tests to a temporary directory and makes
the adapter return True for every pair of known labels. The unrelated control
then incorrectly passes. The same 10-test suite rejects this change with
assertion failures and exit 1. The production files are never modified by this
check. Any unexpected check result raises `AssertionError`, giving the runner
a nonzero exit.

Repository AGENTS.md and the contribution guidance apply. There is no active
`.github/workflows/` at this pinned base. Quiz, notebook and translation code
is unchanged. New local Markdown links resolve and `git diff --check` passed.
Only Python's standard library is needed; no real service is contacted.

The lesson and evidence are separate commits. Omit this entire `work/R39-T015/`
directory from any later upstream branch, after a fit-to-curriculum review.
The current coursework PR targets S-AI-Projects.
