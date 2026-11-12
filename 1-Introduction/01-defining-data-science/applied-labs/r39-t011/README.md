# Applied lab R39-T011: scenario rubric checker

> **Simulation notice:** all scenarios are fictional. There is no real student
> data, hardware, cloud service or trained model. Standard-library Python 3 only.

## How this illustrates the lesson
"Defining Data Science" says data science turns data into **actionable
insights** and walks through the data journey (acquisition, storage,
processing, ...). Its "Digitalization and Digital Transformation" section
digitises an online course (completion times, quiz scores, age categories).
Each of those digitised items is an **asset**. This lab asks, for each asset:
what could go wrong (**threat**), what reduces it (**control**), and what is
still left (**residual risk**).

## Inputs and outputs
| Public item | Meaning | Lesson concept |
|---|---|---|
| input `scenario` (dict) | `lesson_section`, `asset`, `threat`, `threat_type`, `control`, `control_type`, `residual_risk` | a digitised data source from the lesson |
| output `Result.status` | `PASS`, `FAIL` or `REVIEW` | structural verdict only |
| output `Result.reasons` | list such as `missing:asset` | which rule fired |

## Run
From the repository root:

    python3 1-Introduction/01-defining-data-science/applied-labs/r39-t011/example.py
    python3 -m unittest discover -s 1-Introduction/01-defining-data-science/applied-labs/r39-t011 -p "test_*.py"

Expected output of `example.py`:

    S1-course-timings      PASS    -
    S2-web-logs            PASS    -
    S3-quiz-table          PASS    -
    N1-no-asset            FAIL    missing:asset
    N2-unrelated-control   REVIEW  control_unrelated_to_threat

Expected test result: `Ran 12 tests ... OK` (exit code 0).

## Where the simplifications stop
- The checker verifies structure only. A scenario with every field filled in
  with nonsense still passes (see `test_structurally_complete_nonsense_still_passes`).
  A human reviewer judges the explanation.
- The threat-to-control table is a small hand-made mapping, not security
  knowledge. Unrelated pairs are flagged `REVIEW`, not decided.
- Nothing here measures real privacy, real system behaviour or model quality.