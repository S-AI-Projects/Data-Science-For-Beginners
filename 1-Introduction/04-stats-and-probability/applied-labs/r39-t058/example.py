"""Histogram boundary accounting evaluation experiment.
Task R39-T058.
"""

from typing import List, Dict, Any, Sequence


def count_histogram_bins(
    values: Sequence[float], bins: Sequence[float]
) -> Dict[str, Any]:
    """Count values into bins where bins are [start, end) and final bin is [start, end]."""
    if len(bins) < 2:
        raise ValueError("At least two bin edges required")

    for i in range(len(bins) - 1):
        if bins[i] >= bins[i + 1]:
            raise ValueError("Bins must be strictly increasing")

    num_bins = len(bins) - 1
    counts = [0] * num_bins
    below_range: List[float] = []
    above_range: List[float] = []

    for val in values:
        if val < bins[0]:
            below_range.append(val)
        elif val > bins[-1]:
            above_range.append(val)
        else:
            placed = False
            for i in range(num_bins):
                is_last_bin = i == num_bins - 1
                if is_last_bin:
                    if bins[i] <= val <= bins[i + 1]:
                        counts[i] += 1
                        placed = True
                        break
                else:
                    if bins[i] <= val < bins[i + 1]:
                        counts[i] += 1
                        placed = True
                        break
            if not placed:
                above_range.append(val)

    return {
        "bins": list(bins),
        "counts": counts,
        "below_range": below_range,
        "above_range": above_range,
        "total_in_range": sum(counts),
        "total_out_of_range": len(below_range) + len(above_range),
    }


def run_evaluation_experiment() -> Dict[str, Any]:
    """Compare three small controlled configurations and observe trade offs."""
    configs = {
        "config_small": {
            "bins": [0, 10, 20],
            "values": [0, 9, 10, 20],
            "expected_counts": [2, 2],
        },
        "config_medium": {
            "bins": [0, 10, 20],
            "values": [-5, 0, 5, 9, 10, 15, 20, 25],
            "expected_counts": [3, 3],
        },
        "config_multibin": {
            "bins": [0, 5, 10, 20],
            "values": [0, 2, 5, 8, 10, 20],
            "expected_counts": [2, 2, 2],
        },
    }

    report: Dict[str, Any] = {}
    for cfg_name, cfg_data in configs.items():
        res = count_histogram_bins(cfg_data["values"], cfg_data["bins"])
        is_correct = res["counts"] == cfg_data["expected_counts"]
        total_items = len(cfg_data["values"])
        in_range_ratio = (
            res["total_in_range"] / total_items if total_items > 0 else 0.0
        )

        report[cfg_name] = {
            "input_size": total_items,
            "bins": cfg_data["bins"],
            "counts": res["counts"],
            "correctness_pct": 100.0 if is_correct else 0.0,
            "in_range_ratio": round(in_range_ratio, 2),
            "out_of_range_count": res["total_out_of_range"],
        }

    return report


def main() -> None:
    bins = [0, 10, 20]
    values = [0, 9, 10, 20]
    contract_res = count_histogram_bins(values, bins)
    print("Contract result counts:", contract_res["counts"])

    exp_report = run_evaluation_experiment()
    print("\nEvaluation experiment across configurations:")
    for cfg, data in exp_report.items():
        print(f"{cfg}: size={data['input_size']}, counts={data['counts']}, correctness={data['correctness_pct']}%")


if __name__ == "__main__":
    main()
