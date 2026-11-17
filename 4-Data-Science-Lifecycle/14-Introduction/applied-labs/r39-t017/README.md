# Worked lifecycle scenario rubric

The [lifecycle introduction](../../README.md) treats maintenance as ongoing work
throughout capturing and processing. Its **Maintaining → Securing the Data**
section discusses removing departed users' access, limiting who can alter data
and encrypting stored data. This local exercise turns those topics into three
fictional scenarios and a small, explicit structural rubric.

## Local fixture

Prerequisites: Python 3.7+, its standard library and a local checkout. Run from
the repository root. No credentials, downloads, provider, GPU or device is needed.

```bash
python3 4-Data-Science-Lifecycle/14-Introduction/applied-labs/r39-t017/example.py
```

The three fictional records in `SCENARIOS` are evaluated in this order:

| ID | Asset | Threat | Control | Residual risk |
| --- | --- | --- | --- | --- |
| departed-analyst | Community survey dataset | `departed_account_access` | `revoke_departed_access` | Previously downloaded copies may still exist. |
| report-edit | Shared dataset for a monthly report | `unauthorized_changes` | `restrict_writers` | An authorized writer could still make an incorrect edit. |
| stored-survey | Stored survey export | `exposed_storage` | `encrypt_storage` | A user with decryption access could still disclose data. |

Expected default output, exit 0:

```json
{"results": [{"status": "pass", "issues": []}, {"status": "pass", "issues": []}, {"status": "pass", "issues": []}]}
```

## Worked input → output

Take the first scenario, without the optional `id` and `section` metadata.
The exact input is:

<!-- worked-input -->
```json
{
  "asset": "Fictional community survey dataset",
  "threat": "departed_account_access",
  "control": "revoke_departed_access",
  "residual_risk": "Previously downloaded copies may still exist."
}
```

Run this exact command from the repository root:

<!-- worked-command -->
```bash
python3 4-Data-Science-Lifecycle/14-Introduction/applied-labs/r39-t017/example.py --scenario '{"asset":"Fictional community survey dataset","threat":"departed_account_access","control":"revoke_departed_access","residual_risk":"Previously downloaded copies may still exist."}'
```

Expected exact stdout, exit 0, with no stderr:

<!-- worked-output -->
```json
{"results": [{"status": "pass", "issues": []}]}
```

Here is why that output follows from the input:

1. The input is an object, so individual fields can be checked.
2. `asset` identifies a dataset and is a nonblank string.
3. `threat` and `control` are nonblank strings, and their exact labels form a
   listed rubric pair: `departed_account_access` → `revoke_departed_access`.
4. `residual_risk` is also nonblank text, so no required field is missing.
5. The checker therefore returns `pass` with an empty issue list. It has checked
   only completeness and the listed pair, not the explanation's truth or quality.

A possible control rationale for human discussion is that revoking a departed
account's access addresses future use of that account, while not recalling
copies already obtained. A reviewer should ask for evidence about the actual
accounts, revocation process and retained copies. This example supplies none of
that operational evidence and does not claim an effective real-world control.

`test_exact_readme_worked_example_is_a_regression` reads these marked input,
command and output blocks directly from this README. It checks the literal
input, executes the published command in a fresh process without a shell, and
compares stdout byte-for-byte as text, stderr and the exit code. This keeps the
worked explanation and runnable example aligned.

## Rubric boundaries and human review

All four fields (`asset`, `threat`, `control`, `residual_risk`) must be nonblank
strings. Missing, blank or wrongly typed fields fail before pair matching.
Extra metadata is not graded. Labels match exactly, including case; the only
accepted pairs are the three in the fixture table. An unlisted or unknown pair
requests review rather than being declared substantively wrong.

The smallest structurally complete answer can use `"x"` for asset and residual
risk alongside a listed threat/control pair. It passes this rubric, but that
does not make it a useful explanation. An empty object fails all four fields.

```bash
python3 4-Data-Science-Lifecycle/14-Introduction/applied-labs/r39-t017/example.py --case missing-asset
python3 4-Data-Science-Lifecycle/14-Introduction/applied-labs/r39-t017/example.py --case unrelated-control
```

These copy the default fixture and change only its first record:

| Case | First result | Other results | Exit |
| --- | --- | --- | --- |
| `complete` / default | `pass`, no issues | `pass`, `pass` | 0 |
| `missing-asset` | `fail`, `missing or invalid: asset` | `pass`, `pass` | 1 |
| `unrelated-control` | `review`, `unlisted threat/control pair` | `pass`, `pass` | 3 |

The unrelated variant substitutes `encrypt_storage` for `revoke_departed_access`.
Encryption is not the listed response to continued access by a departed account;
the checker flags the explanation for human review. It does not decide whether
encryption might help with other risks in a larger scenario. Invalid JSON or
arguments exit 2 with an error on stderr and no report. For multiple records,
structural failure takes precedence over review in the exit code.

## Checks and scope

```bash
python3 -m unittest discover -s 4-Data-Science-Lifecycle/14-Introduction/applied-labs/r39-t017 -p "test_*.py"
```

Expected: 9 tests, `OK`, exit 0. To demonstrate failure, temporarily change the
final rubric result in `check_scenario` from `pass` to `fail`, rerun and restore
it. The exact documented example will then fail its regression test, and
unittest must exit nonzero.

The scenarios are fictional simulations of project discussions. The checker is
real deterministic local code, with no mocked remote service and no control
deployed. It does not assess legal compliance, security effectiveness, semantic
reasoning or trained-model performance. Human review judges the explanation,
supporting evidence and residual-risk rationale; a structural pass is no verdict
on those matters.

Practice: describe evidence you would request before accepting the residual-risk
explanation for one scenario, and explain why this checker cannot assess it.
