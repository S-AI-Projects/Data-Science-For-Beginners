This adds a local outcome-rate exercise to the ethics lesson. It keeps the
sample count beside the rate and records how each observation changes the
calculation, so the final report can be checked against its inputs.

For fictional A `[1,0]` and B `[1,1,0,0]`, both rates are 0.5, but n is 2
for A and 4 for B. An empty group reports an undefined rate (`null`), whereas
`[0]` reports an observed rate of 0.0. The text explains that these descriptive
rates do not establish causation, fairness or population-level conclusions.

The trace starts at zero observations and stores a snapshot after each outcome.
Tests independently reconstruct every prefix and check that its count, positive
count and rate agree. They also check that the final report equals the last
state. All 31 binary sequences of lengths zero through four are covered.

The lesson links to the lab with its command, fixture, expected output and scope.
This is real local arithmetic on synthetic data, using Python 3.7+ and the
standard library. No service is mocked and no model or hardware is involved.

Checks run from the repository root:

```bash
python3 -m unittest discover -s 1-Introduction/02-ethics/applied-labs/r39-t014 -p "test_*.py"
python3 work/R39-T014/run_checks.py
git diff --check
```

All 9 tests pass, along with 10 fresh-process fixture checks. The runner checks
the README's JSON too. It then increments the final count in a temporary copy
without changing the trace, confirms the wrong counts of 3 and 5, and verifies
that the same 9-test suite fails with assertion errors and exit 1. Local links
and anchors resolve.

Evidence:

- [Inputs and expected states](https://github.com/shashank-injeti/Data-Science-For-Beginners/blob/R39-T014/work/R39-T014/fixtures.json)
- [Actual results and deliberate failure](https://github.com/shashank-injeti/Data-Science-For-Beginners/blob/R39-T014/work/R39-T014/results.json)
- [Tool versions](https://github.com/shashank-injeti/Data-Science-For-Beginners/blob/R39-T014/work/R39-T014/versions.json)
- [Check script](https://github.com/shashank-injeti/Data-Science-For-Beginners/blob/R39-T014/work/R39-T014/run_checks.py)

This PR is for the **S-AI-Projects fork**. `R39-T014` starts from pinned main
independently of T012 and T013; the assigned student branch was absent remotely.
The lesson and coursework evidence are separate commits, allowing a later
upstream branch to omit `work/R39-T014/` after a curriculum-fit review. There is
no active CI workflow at this base, and no quiz, notebook or translation change.
