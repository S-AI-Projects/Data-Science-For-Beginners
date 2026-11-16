# Scenario rubric with an offline service adapter

This exercise extends the [real-world examples lesson](../../README.md). Its
industry, humanities and sustainability sections show how data science projects
depend on their context. The research section also asks us to investigate harms
and deployment challenges. Here we practice naming an asset, threat, proposed
control and remaining risk before making claims about a project.

## Local fixture and invocation

You need Python 3.7+, its standard library and a local checkout. Run from the
repository root; no credentials, network, model download, GPU or device is needed.

```bash
python3 6-Data-Science-In-Wild/20-Real-World-Examples/applied-labs/r39-t015/example.py
```

Three fictional scenarios are stored in `SCENARIOS` in `example.py`, in this order:

| ID / lesson section | Asset | Threat | Control | Residual risk |
| --- | --- | --- | --- | --- |
| clinic-access / Data Science + Industry | Clinic appointment dataset for demand analysis | `unauthorized_access` | `access_review` | An approved account could still misuse its access. |
| poetry-archive / Data Science + Humanities | Transcribed poems and annotation history | `data_loss` | `backups` | Edits since the last backup could still be lost. |
| habitat-feed / Data Science + Sustainability | Habitat sensor readings for a dashboard | `tampered_readings` | `integrity_checks` | A faulty sensor may send authentic but inaccurate data. |

Possible rationales for human discussion: reviewing access can help identify
inappropriate permissions; backup copies can support recovery of lost files;
integrity checks can help detect alterations. The checker does not evaluate
these explanations or establish that the proposed controls work in a real system.

Expected output (one line), exit 0:

```json
{"adapter": "deterministic-local-mock", "results": [{"status": "pass", "issues": []}, {"status": "pass", "issues": []}, {"status": "pass", "issues": []}]}
```

## The stated structural rubric

1. Input must be an object. `asset`, `threat`, `control` and `residual_risk` must
   each be a nonblank string. A missing, blank or non-string field fails before
   the adapter is called. Extra fields such as fixture `id` and `section` are
   informational and not graded.
2. The checker calls `relation_check(threat, control)`. The deterministic local
   adapter returns `True` for the three exact pairs in the table, `False` when
   both labels are known but paired differently, and `None` for unknown labels.
   Matching is case-sensitive, with no synonym matching or text interpretation.
3. `True` passes the rubric. `False` requests review of the unlisted pair;
   unknown labels, invalid responses and adapter `OSError` (including a timeout)
   also request review. An unlisted pair is not an automatic substantive failure.

For example, `backups` is deliberately unrelated to `unauthorized_access` in
this narrow lookup. The checker flags that pair for review; it does not claim
that backups can never be relevant to some broader incident. Likewise, a field
containing just `"x"` passes the nonblank-text rule. A human must judge whether
it identifies a meaningful asset or explains residual risk.

## Callable boundary and mock limits

The core is `check_scenario(scenario, relation_check=local_relation)`. A replacement
adapter accepts two strings and returns **exactly** `True`, `False` or `None`.
For an unavailable service it can raise `OSError`; other programming errors are
not silently converted into rubric results. Tests inject a recording callable
and a fictional timeout to verify this boundary without making a request.

`local_relation` is a **deterministic mock relation service**, not a language model
or remote client. It establishes only the specified lookup and local callable
contract. It does not establish a real service's authentication, API compatibility,
latency, availability, retries, rate limits, semantic accuracy, scoring consistency
or handling of sensitive data. Any real integration needs its own implementation,
credentials and separate evaluation; it is outside this task. No control is
deployed, and no trained-model performance or actual security outcome is measured.

## Boundary and failure cases

```bash
python3 6-Data-Science-In-Wild/20-Real-World-Examples/applied-labs/r39-t015/example.py --case missing-asset
python3 6-Data-Science-In-Wild/20-Real-World-Examples/applied-labs/r39-t015/example.py --case unrelated-control
```

These copy the same fixture and change only its first scenario:

| Invocation | First result | Other results | Exit |
| --- | --- | --- | --- |
| default / `--case complete` | `pass`, no issues | `pass`, `pass` | 0 |
| `--case missing-asset` | `fail`, `missing or invalid: asset` | `pass`, `pass` | 1 |
| `--case unrelated-control` | `review`, `threat/control pair not listed` | `pass`, `pass` | 3 |

Every JSON report identifies the mock adapter. CLI exit 1 means a structural
failure, 3 means human review is needed, and malformed JSON or arguments exit 2
with no report. For multiple scenarios a structural failure takes precedence
over review. The smallest complete object has the four required fields; an empty
object fails all four. Unknown but nonblank threat/control labels request review.

To check a custom object locally:

```bash
python3 6-Data-Science-In-Wild/20-Real-World-Examples/applied-labs/r39-t015/example.py --scenario '{"asset":"x","threat":"data_loss","control":"backups","residual_risk":"x"}'
```

This deliberately thin explanation gets one rubric `pass`, exit 0. It is a useful
boundary example of why human review remains necessary, even for a passing result.

## Checks

```bash
python3 -m unittest discover -s 6-Data-Science-In-Wild/20-Real-World-Examples/applied-labs/r39-t015 -p "test_*.py"
```

Expected: 10 tests, `OK`, exit 0. To prove a wrong result fails, temporarily change
`return PAIRS[threat] == control` to `return True`, rerun and restore it. The
unrelated control would incorrectly pass, and unittest must exit nonzero.

Practice: give a human reviewer evidence that would support or challenge one
control rationale, and explain what this lookup cannot decide about that evidence.
