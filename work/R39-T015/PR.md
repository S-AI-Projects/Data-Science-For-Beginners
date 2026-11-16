This adds three fictional scenarios to the real-world examples lesson: a clinic
dataset, a poetry archive and a habitat sensor feed. Each names an asset, threat,
control and residual risk, and is tied to the lesson's Industry, Humanities or
Sustainability section.

The checker verifies nonblank required fields and delegates the threat/control
relation to a callable. A deterministic offline adapter uses three exact label
pairs. Complete scenarios pass; a missing asset fails before the adapter is
called; an unrelated control or unknown label requests human review.

A rubric pass is deliberately narrow. Human review still judges the explanation,
evidence and proposed control. The mock does not establish real-service semantic
accuracy, authentication, compatibility, availability, latency or control
effectiveness. There is no model training, paid provider, network call or device.
Python 3.7+ and the standard library are sufficient.

Checks run from the repository root:

```bash
python3 -m unittest discover -s 6-Data-Science-In-Wild/20-Real-World-Examples/applied-labs/r39-t015 -p "test_*.py"
python3 work/R39-T015/run_checks.py
git diff --check
```

All 10 tests pass, including injected callables, invalid responses and a fictional
timeout. Nine CLI scenarios run in fresh processes. The saved fixture and both
README output blocks agree with the code. Local documentation links resolve.

The failure check changes the adapter in a temporary copy to accept every known
pair. It confirms that the unrelated control wrongly passes, then verifies that
the same suite fails with assertion errors and exit 1.

Evidence:

- [Scenarios, inputs and expected results](https://github.com/shashank-injeti/Data-Science-For-Beginners/blob/R39-T015/work/R39-T015/fixtures.json)
- [Actual results and wrong-adapter failure](https://github.com/shashank-injeti/Data-Science-For-Beginners/blob/R39-T015/work/R39-T015/results.json)
- [Tool versions](https://github.com/shashank-injeti/Data-Science-For-Beginners/blob/R39-T015/work/R39-T015/versions.json)
- [Check script](https://github.com/shashank-injeti/Data-Science-For-Beginners/blob/R39-T015/work/R39-T015/run_checks.py)

This PR targets the **S-AI-Projects fork**. `R39-T015` starts from pinned main
and contains no previous task changes. The assigned student branch was absent
remotely. Lesson and coursework evidence are separate commits so that a later
upstream proposal can omit `work/R39-T015/` after a curriculum-fit review. There
is no active CI workflow at this base; quiz, notebook and translations are unchanged.
