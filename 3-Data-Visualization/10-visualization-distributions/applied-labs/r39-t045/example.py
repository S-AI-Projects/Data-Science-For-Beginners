"""Histogram boundary accounting with offline service adapter (R39-T045).

Extends the Visualizing Distributions lesson. Puts distribution histogram
binning behind a callable service interface and provides a deterministic
offline adapter implementing explicit half-open bin accounting with a
right-inclusive final bin.
"""

from __future__ import annotations
from abc import ABC, abstractmethod
import json
from typing import Any, Dict, List, Sequence


class HistogramServiceInterface(ABC):
    """Abstract callable interface for distribution histogram services."""

    @abstractmethod
    def compute_histogram(
        self, values: Sequence[float], bins: Sequence[float]
    ) -> Dict[str, Any]:
        """Compute bin counts and out-of-range elements."""
        pass


class LocalOfflineHistogramAdapter(HistogramServiceInterface):
    """Deterministic local adapter implementing the histogram service contract offline.

    Behavioral limitations of this local mock:
    1. Does not simulate cloud network latency, packet loss, or HTTP connection timeouts.
    2. Does not partition computation across distributed worker nodes or cluster memory.
    3. Uses standard IEEE-754 64-bit float precision; does not simulate specialized hardware
       or GPU vectorization discrepancies.
    """

    def compute_histogram(
        self, values: Sequence[float], bins: Sequence[float]
    ) -> Dict[str, Any]:
        if len(bins) < 2:
            raise ValueError("Bins specification must contain at least two edges.")
        for i in range(len(bins) - 1):
            if bins[i] >= bins[i + 1]:
                raise ValueError("Bin edges must be strictly increasing.")

        num_bins = len(bins) - 1
        counts = [0] * num_bins
        below_range: List[float] = []
        above_range: List[float] = []

        for v in values:
            if v < bins[0]:
                below_range.append(v)
            elif v > bins[-1]:
                above_range.append(v)
            else:
                for i in range(num_bins):
                    is_last = (i == num_bins - 1)
                    lower = bins[i]
                    upper = bins[i + 1]
                    if is_last:
                        if lower <= v <= upper:
                            counts[i] += 1
                            break
                    else:
                        if lower <= v < upper:
                            counts[i] += 1
                            break

        return {
            "bins": list(bins),
            "counts": counts,
            "below_range": below_range,
            "above_range": above_range,
            "total_in_range": sum(counts),
            "total_out_of_range": len(below_range) + len(above_range),
            "service_mode": "local_offline_adapter",
        }


def main() -> None:
    adapter = LocalOfflineHistogramAdapter()
    bins = [0, 10, 20]
    values = [0, 9, 10, 20]
    res = adapter.compute_histogram(values, bins)
    print(json.dumps(res))


if __name__ == "__main__":
    main()
