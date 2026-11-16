This adds a small local example to the data preparation lesson showing why a
missing-value mean should be fitted on training observations and reused for
validation.

For training `[2,None,4]`, the stored mean is 3. Validation `[100,None]` then
becomes `[100,3]`. Refitting on validation would give `[100,100]`, which the
checks reject.

The lab has separate fit and transform functions and compares their output with
a hand-calculated table using identical inputs. It covers a single observed
training value, zero, fractional and negative values, empty validation, and
all-missing validation. Empty or all-missing training is rejected because there
is no observed value to average.

The lesson links to the lab with the command, fixture and expected output.
It needs only Python 3.7+ and a checkout. These are synthetic local observations,
with no mocked service, model training or claims about model performance. The
scope is one numeric feature with `None` as the missing-value marker.

Validation run from the repository root:

```bash
python3 -m unittest discover -s 2-Working-With-Data/08-data-preparation/applied-labs/r39-t013 -p "test_*.py"
python3 work/R39-T013/run_checks.py
git diff --check
```

All 9 tests pass. The evidence runner checks 14 fixtures in fresh processes.
It also introduces validation refitting in a temporary copy, confirms the wrong
`[100,100]` result, and verifies that the same suite fails with assertion errors
and exit 1. New relative documentation links resolve.

Evidence:

- [Inputs and independent expected results](https://github.com/shashank-injeti/Data-Science-For-Beginners/blob/R39-T013/work/R39-T013/fixtures.json)
- [Actual results and failure check](https://github.com/shashank-injeti/Data-Science-For-Beginners/blob/R39-T013/work/R39-T013/results.json)
- [Tool versions](https://github.com/shashank-injeti/Data-Science-For-Beginners/blob/R39-T013/work/R39-T013/versions.json)
- [Check script](https://github.com/shashank-injeti/Data-Science-For-Beginners/blob/R39-T013/work/R39-T013/run_checks.py)

This PR targets the **S-AI-Projects fork**. Branch `R39-T013` starts at the pinned
main commit, independently of T012. The assigned student branch was absent on
the remote. Lesson files and coursework evidence are separate commits, so a
later upstream proposal can omit `work/R39-T013/` after a curriculum-fit review.
No active repository CI workflow exists at this base; quiz, notebook and
translation files are unchanged.
