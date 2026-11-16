Rows A,A,B,C,C,C must be communicated as A=2, B=1, C=3, total=6. When the
audience sees only A/B, the displayed total must be 3. This lesson extension
demonstrates that labels, counts and aggregate totals describe the same data.

- Adds a Python standard-library local summary and synthetic fixture, with
  labels paired directly to counts and the total computed after filtering.
- Explains the exact boundary: empty data is valid (total 0), one label is the
  smallest nonempty case, and blank/non-string labels are invalid even when
  excluded by the filter. Empty filters and unknown categories retain no rows.
- Links the lab from the communication lesson with exact commands, output,
  prerequisites and limitations. No service or hardware simulation, credentials,
  model download, or trained-model performance claim is involved.

Validation:

```bash
python3 -m unittest discover -s 4-Data-Science-Lifecycle/16-communication/applied-labs/r39-t012 -p "test_*.py"
python3 work/R39-T012/run_checks.py
git diff --check
```

All 9 tests pass. Fourteen CLI scenarios run in fresh processes, including
normal, smallest nonempty, empty and invalid inputs. A disposable copy with a
deliberately incorrect total fails the same 9-test suite with assertion failures
and exit 1. New relative documentation links resolve.

Evidence: [expected versus actual results](https://github.com/shashank-injeti/Data-Science-For-Beginners/blob/R39-T012/work/R39-T012/results.json),
[tool versions](https://github.com/shashank-injeti/Data-Science-For-Beginners/blob/R39-T012/work/R39-T012/versions.json),
[reproducible checks](https://github.com/shashank-injeti/Data-Science-For-Beginners/blob/R39-T012/work/R39-T012/run_checks.py).

Submission is for **S-AI-Projects/Data-Science-For-Beginners**, based on pinned
commit 4d2ac427ad6f022e73a75c4f46a28bbb7978ec3f. The assigned remote branch
`student/e26b07f0735` was absent, so task branch `R39-T012` starts at fork main.
The lesson change and coursework evidence are separate commits: omit the
`work/R39-T012/` evidence commit from any later upstream proposal, which first
needs a fit-to-curriculum review. No active repository CI workflow exists at this
base; quiz, notebook and translation code is unchanged.

Instructor review is welcome.
