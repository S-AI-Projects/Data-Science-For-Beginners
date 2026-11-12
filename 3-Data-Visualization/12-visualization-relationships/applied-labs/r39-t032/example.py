"""Build chart-ready yearly honey production totals from a local fixture."""

import json
from typing import Dict, Iterable, List, Mapping


def local_fixture() -> List[Dict[str, object]]:
    """Return a minimal mock showing grouping two states across two years."""
    return [
        {"state": "AL", "year": 1998, "totalprod": 10},
        {"state": "AZ", "year": 1998, "totalprod": 20},
        {"state": "AL", "year": 1999, "totalprod": 5},
    ]


def minimal_valid_fixture() -> List[Dict[str, object]]:
    """Return the smallest valid input: one record with the required fields."""
    return [{"state": "AL", "year": 1998, "totalprod": 10}]


def boundary_fixture() -> List[Dict[str, object]]:
    """Return a boundary record: zero production is a valid numeric total."""
    return [{"state": "AL", "year": 1998, "totalprod": 0}]


def invalid_fixture() -> List[Dict[str, object]]:
    """Return an invalid record missing the required totalprod field."""
    return [{"state": "AL", "year": 1998}]


def aggregate_yearly_production(
    observations: Iterable[Mapping[str, object]],
) -> Dict[str, List[int]]:
    """Group records by year and return aligned labels and total production.

    The label at each index is the year for the production total at that same
    index, mirroring x-axis labels and y-values in a chart. Empty input is
    valid and produces empty series; required fields and integer values are
    checked for each supplied record.
    """
    totals_by_year: Dict[int, int] = {}

    for row_number, observation in enumerate(observations, start=1):
        try:
            year = observation["year"]
            production = observation["totalprod"]
        except KeyError as error:
            raise ValueError(
                "observation {} is missing required field {!r}".format(
                    row_number, error.args[0]
                )
            ) from error

        if isinstance(year, bool) or not isinstance(year, int):
            raise ValueError("observation {} has a non-integer year".format(row_number))
        if isinstance(production, bool) or not isinstance(production, int):
            raise ValueError(
                "observation {} has non-integer totalprod".format(row_number)
            )

        totals_by_year[year] = totals_by_year.get(year, 0) + production

    labels = sorted(totals_by_year)
    return {
        "labels": labels,
        "values": [totals_by_year[year] for year in labels],
    }


def main() -> None:
    """Print the local fixture's chart data as JSON."""
    print(json.dumps(aggregate_yearly_production(local_fixture())))


if __name__ == "__main__":
    main()
