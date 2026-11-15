"""Group honey production by year and visualize the annual totals."""

from collections import defaultdict
from typing import DefaultDict, Iterable, List, Tuple


ProductionRecord = Tuple[str, int, int]
AnnualTotal = Tuple[int, int]

PRODUCTION_RECORDS: List[ProductionRecord] = [
    ("CA", 2019, 12),
    ("ND", 2019, 8),
    ("CA", 2018, 10),
    ("SD", 2019, 5),
    ("ND", 2018, 4),
]


def annual_production_totals(
    records: Iterable[ProductionRecord],
) -> List[AnnualTotal]:
    """Return every observed year and its total in chronological order.

    There is no year-range filter; an empty input produces no groups.
    """
    totals: DefaultDict[int, int] = defaultdict(int)
    for record in records:
        if not isinstance(record, tuple) or len(record) != 3:
            raise ValueError("Each record must be a (state, year, production) tuple.")

        state, year, production = record
        if not isinstance(state, str) or not state.strip():
            raise ValueError("State must be a non-empty string.")
        if isinstance(year, bool) or not isinstance(year, int):
            raise ValueError("Year must be an integer.")
        if (
            isinstance(production, bool)
            or not isinstance(production, int)
            or production < 0
        ):
            raise ValueError("Production must be a non-negative integer.")

        totals[year] += production
    return sorted(totals.items())


def main() -> None:
    import matplotlib.pyplot as plt

    annual_totals = annual_production_totals(PRODUCTION_RECORDS)
    print("Year | Total honey production (pounds)")
    for year, total in annual_totals:
        print(f"{year} | {total}")

    years, totals = zip(*annual_totals)
    _, axis = plt.subplots()
    axis.plot(years, totals, marker="o")
    axis.set(
        title="Annual Honey Production",
        xlabel="Year",
        ylabel="Total production (pounds)",
    )
    axis.grid(True, alpha=0.3)
    plt.show()


if __name__ == "__main__":
    main()
