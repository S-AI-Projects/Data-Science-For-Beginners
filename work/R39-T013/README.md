# R39-T013 check results

This task starts at organisation-fork main, commit
`4d2ac427ad6f022e73a75c4f46a28bbb7978ec3f`, which matches the pinned source.
Branch `R39-T013` is independent of `R39-T012`; none of T012's changes are
included. Neither `student/e26b07f0735` nor `R39-T013/student/e26b07f0735`
exists on the organisation remote.

From the repository root:

```bash
python3 -m unittest discover -s 2-Working-With-Data/08-data-preparation/applied-labs/r39-t013 -p "test_*.py"
python3 work/R39-T013/run_checks.py
git diff --check
```

Results: 9 tests passed; the fixture runner checked 14 cases in fresh processes.
The expected answers are literal values calculated independently of the
implementation. The same training and validation lists are passed to the code
and shown alongside those expectations.

- [Saved inputs and expected results](fixtures.json)
- [Expected versus actual results, stdout, stderr and exit codes](results.json)
- [Tool versions](versions.json)
- [Reproducible check script](run_checks.py)
- [Lab explanation and calculation table](../../2-Working-With-Data/08-data-preparation/applied-labs/r39-t013/README.md)

The normal case fits `(2+4)/2 = 3` on training `[2,null,4]`. Validation
`[100,null]` becomes `[100,3]`. A single observed training value is valid;
empty/all-missing training is rejected. Empty and all-missing validation work
with the already fitted mean. Tests also cover zero, negative and fractional
values, repeated transformation, unchanged inputs and invalid types.

The runner changes **only a temporary copy** so transformation wrongly refits
on validation. It first confirms that this produces `[100,100]`, then runs the
same suite and requires 9 discovered tests, assertion failures and a nonzero
exit. That suite exits 1, as expected. The runner raises `AssertionError` and
exits nonzero if any check fails; production files stay unchanged.

The repository AGENTS.md and contribution guidance apply. No active workflow is
present under `.github/workflows/` at the pinned base. No quiz app, notebook or
translation code changed. New relative Markdown links resolve and
`git diff --check` passed. Tests use Python's standard library; no external data
or service is involved.

The lesson change and this coursework evidence are separate commits. For a later
upstream proposal, first obtain a fit-to-curriculum review, then use only the
lesson commit. Omit the entire `work/R39-T013/` directory from that branch.
