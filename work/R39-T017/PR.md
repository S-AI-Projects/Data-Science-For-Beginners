This adds a worked scenario-rubric exercise to the lifecycle introduction, tied
to **Maintaining → Securing the Data**. The three fictional scenarios cover a
departed analyst's access, unauthorized dataset edits and exposed stored survey
data. Each names an asset, threat, control and residual risk.

The main teaching example walks from one exact JSON input to its result. It
explains the nonblank-field checks and the listed threat/control pair that lead
to a structural pass. A regression test reads the documented input, command and
expected output from the README, executes that exact command, and checks stdout,
stderr and exit status. Expected results are literal, not computed by the checker.

A missing asset fails; an unrelated control requests review. Human review still
judges the explanation, evidence and residual-risk rationale. The fictional
scenarios simulate project discussions; the checker is real local structural
code, with no mocked service, deployed control or trained-model claim. Python
3.7+, its standard library and a checkout are sufficient.

Checks run from the repository root:

```bash
python3 -m unittest discover -s 4-Data-Science-Lifecycle/14-Introduction/applied-labs/r39-t017 -p "test_*.py"
python3 work/R39-T017/run_checks.py
git diff --check
```

All 9 tests pass. Nine CLI cases plus the exact worked command run in fresh
processes. They cover normal, minimal, empty, missing-field, unknown-pair and
malformed-input cases. Saved scenarios and documented outputs agree with the
code, and new local links resolve.

The failure check changes the complete result to `fail` in a temporary copy.
The documented example then exits 1, and the same suite fails with assertions
and specifically reports the worked-example regression test as failing.

Evidence:

- [Inputs, scenarios and expected results](https://github.com/shashank-injeti/Data-Science-For-Beginners/blob/R39-T017/work/R39-T017/fixtures.json)
- [Exact command results and deliberate failure](https://github.com/shashank-injeti/Data-Science-For-Beginners/blob/R39-T017/work/R39-T017/results.json)
- [Tool versions](https://github.com/shashank-injeti/Data-Science-For-Beginners/blob/R39-T017/work/R39-T017/versions.json)
- [Check script](https://github.com/shashank-injeti/Data-Science-For-Beginners/blob/R39-T017/work/R39-T017/run_checks.py)

This PR targets the **S-AI-Projects fork** on independent branch `R39-T017`.
The assigned student branch was absent remotely, so it starts at pinned main.
No earlier task changes are included. Lesson files and coursework evidence are
separate commits; omit `work/R39-T017/` from any later upstream proposal after
a curriculum-fit review. No active CI workflow exists at this base; quiz,
notebook and translation code is unchanged.
