This adds three fictional scenarios to the defining data science lesson. They
connect digital transformation, processing web logs and IoT readings to four
fields: asset, threat, control and residual risk. A small rubric checks field
completeness and listed threat/control pairs.

The lab includes three applied questions: predict the result for a complete
scenario, diagnose a missing asset, and choose the review policy for an unlisted
pair. Each answer has a rationale and an executable check against the local
rubric. A complete scenario passes, a missing asset fails, and an unlisted pair
requests human review. The checker does not judge explanation quality or
control effectiveness.

Checks run from the repository root:

```bash
python3 -m unittest discover -s 1-Introduction/01-defining-data-science/applied-labs/r39-t020 -p "test_*.py"
python3 work/R39-T020/run_checks.py
git diff --check
```

All 12 tests pass. Four scenario CLI cases and all three applied questions run
in fresh processes. The runner checks both README outputs against the fixture.
A temporary wrong-result mutation makes the same suite fail with assertions and
a nonzero exit.

Evidence:

- [Fixtures and expected question answers](https://github.com/shashank-injeti/Data-Science-For-Beginners/blob/R39-T020/work/R39-T020/fixtures.json)
- [Actual results and deliberate failure](https://github.com/shashank-injeti/Data-Science-For-Beginners/blob/R39-T020/work/R39-T020/results.json)
- [Tool versions](https://github.com/shashank-injeti/Data-Science-For-Beginners/blob/R39-T020/work/R39-T020/versions.json)
- [Check runner](https://github.com/shashank-injeti/Data-Science-For-Beginners/blob/R39-T020/work/R39-T020/run_checks.py)

Inputs are fictional and use Python 3.7+ standard-library code. There is no
service simulation, model, paid provider or hardware. The rubric only checks
structure and listed labels; human review evaluates the explanations and
supporting evidence.

This PR targets the **S-AI-Projects fork** on independent branch `R39-T020`.
The assigned student branch was absent, so the task branch starts at pinned main.
No earlier task changes are included. Lesson and evidence are separate commits;
omit `work/R39-T020/` from a later upstream branch after a curriculum-fit review.
No active CI workflow exists at this base; notebooks, quizzes and translations
are unchanged.
