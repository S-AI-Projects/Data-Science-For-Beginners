# R39-T045: Histogram Boundary Accounting (Offline Service Adapter)

## Overview
This local applied lab extends [Visualizing Distributions](../../README.md) by placing histogram boundary binning behind a callable service interface (`HistogramServiceInterface`) and supplying a deterministic offline adapter (`LocalOfflineHistogramAdapter`).

## Contract & Fixture
- **Input Bins:** `[0, 10, 20]`
- **Input Values:** `[0, 9, 10, 20]`
- **Result Counts:** `[2, 2]`
  - Bin $[0, 10)$: includes `0` and `9`
  - Bin $[10, 20]$ (final right-inclusive): includes `10` and `20`
- Values outside range recorded separately.

## Identified Mock Limitations
1. Does not simulate cloud network latency, packet loss, or HTTP connection timeouts.
2. Does not partition computation across distributed cluster nodes.
3. Does not replicate GPU acceleration or distributed cluster hardware variations.

## Invocation & Output
```bash
python3 3-Data-Visualization/10-visualization-distributions/applied-labs/r39-t045/example.py
```
Output:
```json
{"bins": [0, 10, 20], "counts": [2, 2], "below_range": [], "above_range": [], "total_in_range": 4, "total_out_of_range": 0, "service_mode": "local_offline_adapter"}
```

Run tests:
```bash
python3 -m unittest discover -s 3-Data-Visualization/10-visualization-distributions/applied-labs/r39-t045 -p "test_*.py"
```
