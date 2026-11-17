This adds three fictional rubric scenarios tied to Capturing, Processing and
Maintaining in the lifecycle lesson. Each includes an asset, threat, control and
residual risk. Complete scenarios pass, a missing asset fails, and an unrelated
threat/control pair requests review for a person.

The lab compares input sizes of one, two and three scenarios. All statuses match
the expected rubric result. The deterministic work count is 4, 8 and 12 required
fields checked, respectively. This is a contract-level measure of checks, not a
timing benchmark or claim about model accuracy.

Validation from the repository root:

```bash
python3 -m unittest discover -s 4-Data-Science-Lifecycle/14-Introduction/applied-labs/r39-t019 -p "test_*.py"
python3 work/R39-T019/run_checks.py
git diff --check
```

All 9 tests pass. The evidence runner checks four CLI cases in fresh processes,
the exact JSON in both README files, and a temporary wrong-result mutation. The
mutation changes a complete result to `review`; the same suite fails with
assertion errors and exit 1. Saved inputs, expected/actual outputs and tool
versions are linked below.

- [Fixture scenarios and size comparison](https://github.com/shashank-injeti/Data-Science-For-Beginners/blob/R39-T019/work/R39-T019/fixtures.json)
- [Actual checks and mutation failure](https://github.com/shashank-injeti/Data-Science-For-Beginners/blob/R39-T019/work/R39-T019/results.json)
- [Tool versions](https://github.com/shashank-injeti/Data-Science-For-Beginners/blob/R39-T019/work/R39-T019/versions.json)
- [Evidence runner](https://github.com/shashank-injeti/Data-Science-For-Beginners/blob/R39-T019/work/R39-T019/run_checks.py)

Human review still judges the explanation and evidence. The checker only checks
nonblank fields and exact listed pairs. These are fictional cases processed by
local Python code; no service, model or hardware is involved. Python 3.7+ and its
standard library are sufficient.

This PR targets the **S-AI-Projects fork** on independent branch `R39-T019`.
It starts at pinned main because the assigned student branch was absent. Earlier
tasks are not included. Lesson and evidence are separate commits, so a later
upstream proposal can omit `work/R39-T019/` after a curriculum-fit review. There
is no active CI workflow at this base; notebooks, quizzes and translations are
unchanged.
