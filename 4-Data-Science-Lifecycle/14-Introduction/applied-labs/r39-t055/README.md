# Security Scenario Rubric with Offline Service Adapter (R39 T055)

## Overview
This lab extends the Introduction to the Data Science Lifecycle lesson. It shows how to check security scenarios across lifecycle stages while decoupling policy checks using a callable local adapter.

## The Contract and Scenarios
* Complete scenario passes: Training pipeline dataset protected by role based access controls passes rubric checks.
* Missing asset fails: When asset is None, the checker marks it as FAIL.
* Unrelated control needs review: A denial of service threat paired with changing a dashboard theme gets marked as REVIEW.
* Human review judges the explanation while the checker verifies structural fields.

## The Callable Service Adapter
The rubric checker accepts any callable adapter that receives the threat and control strings. This allows running entirely offline without talking to external cloud services.

## Unestablished Behaviors
The local adapter does not establish:
1. Live cloud identity and access management calls
2. Network latency, retries, and timeout handling
3. Automatic synchronization with real enterprise policy databases

## How to Run the Example
Run with Python 3:
```bash
python3 4-Data-Science-Lifecycle/14-Introduction/applied-labs/r39-t055/example.py
```

## How to Run Tests
Run the unit test runner:
```bash
python3 -m unittest discover -s 4-Data-Science-Lifecycle/14-Introduction/applied-labs/r39-t055 -p "test_*.py"
```

## Scope and Limitations
This lab is a local simulation using Python 3 standard library. No live cloud endpoints or paid services are used.
