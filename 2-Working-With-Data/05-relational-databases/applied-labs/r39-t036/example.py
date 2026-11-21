import sqlite3
from typing import List, Optional, Tuple


def create_schema(connection: sqlite3.Connection) -> None:
    """Create the lesson's cities and rainfall tables in a SQLite connection.

    The table IDs illustrate primary keys; rainfall.city_id references
    cities.city_id as a foreign key.
    """
    connection.execute("PRAGMA foreign_keys = ON")
    connection.executescript(
        """
        CREATE TABLE cities (
            city_id INTEGER PRIMARY KEY,
            city TEXT NOT NULL,
            country TEXT NOT NULL
        );

        CREATE TABLE rainfall (
            rainfall_id INTEGER PRIMARY KEY,
            city_id INTEGER NOT NULL REFERENCES cities(city_id),
            year INTEGER NOT NULL,
            amount INTEGER NOT NULL
        );
        """
    )


class QueryBuilder:
    """Named responsibility: Query construction and validation.

    Handles parameter validation and building the parameterized SQL statement.
    """

    @staticmethod
    def validate_parameters(year: int, order_desc: bool) -> None:
        """Validate input parameters for rainfall queries."""
        if not isinstance(year, int) or isinstance(year, bool):
            raise TypeError("Year must be an integer, got {}".format(type(year).__name__))
        if year < 0:
            raise ValueError("Year must be non-negative, got {}".format(year))
        if not isinstance(order_desc, bool):
            raise TypeError("order_desc must be a boolean, got {}".format(type(order_desc).__name__))

    @staticmethod
    def build_rainfall_query(order_desc: bool = False) -> str:
        """Construct the SQL query string for rainfall joined with cities."""
        order_direction = "DESC" if order_desc else "ASC"
        return (
            "SELECT cities.city, rainfall.amount\n"
            "FROM cities\n"
            "INNER JOIN rainfall ON cities.city_id = rainfall.city_id\n"
            "WHERE rainfall.year = ?\n"
            "ORDER BY cities.city {}"
        ).format(order_direction)


def rainfall_for_year_baseline(
    connection: sqlite3.Connection, year: int, order_desc: bool = False
) -> List[Tuple[str, int]]:
    """Baseline implementation before extracting QueryBuilder responsibility.

    Directly validates parameters, builds SQL, and executes against connection.
    """
    if not isinstance(year, int) or isinstance(year, bool):
        raise TypeError("Year must be an integer, got {}".format(type(year).__name__))
    if year < 0:
        raise ValueError("Year must be non-negative, got {}".format(year))
    if not isinstance(order_desc, bool):
        raise TypeError("order_desc must be a boolean, got {}".format(type(order_desc).__name__))

    order_direction = "DESC" if order_desc else "ASC"
    sql = (
        "SELECT cities.city, rainfall.amount\n"
        "FROM cities\n"
        "INNER JOIN rainfall ON cities.city_id = rainfall.city_id\n"
        "WHERE rainfall.year = ?\n"
        "ORDER BY cities.city {}"
    ).format(order_direction)

    cursor = connection.execute(sql, (year,))
    return cursor.fetchall()


def rainfall_for_year(
    connection: sqlite3.Connection,
    year: int,
    order_desc: bool = False,
    query_builder: Optional[QueryBuilder] = None,
) -> List[Tuple[str, int]]:
    """Return (city, rainfall amount) rows for a year, ordered by city name.

    `year` is the value for the SQL WHERE filter.
    `order_desc` determines sorting order (ascending by default, descending if True).
    The returned fields are the columns selected from the joined cities and rainfall tables.
    Delegates query construction and validation to QueryBuilder (extracted responsibility).
    """
    builder = query_builder or QueryBuilder()
    builder.validate_parameters(year, order_desc)
    sql = builder.build_rainfall_query(order_desc=order_desc)
    cursor = connection.execute(sql, (year,))
    return cursor.fetchall()


def populate_fixture(connection: sqlite3.Connection) -> None:
    """Populate database connection with sample fixture data."""
    connection.executemany(
        "INSERT INTO cities (city_id, city, country) VALUES (?, ?, ?)",
        [
            (1, "Tokyo", "Japan"),
            (2, "Atlanta", "United States"),
            (3, "Auckland", "New Zealand"),
        ],
    )
    connection.executemany(
        "INSERT INTO rainfall (rainfall_id, city_id, year, amount) "
        "VALUES (?, ?, ?, ?)",
        [
            (1, 1, 2019, 1874),
            (2, 2, 2019, 1111),
            (3, 3, 2019, 942),
            (4, 1, 2020, 1690),
        ],
    )


def main() -> None:
    """Run the local sample and print the ordered query results."""
    with sqlite3.connect(":memory:") as connection:
        create_schema(connection)
        populate_fixture(connection)
        for city, amount in rainfall_for_year(connection, 2019):
            print("{}: {} mm".format(city, amount))


if __name__ == "__main__":
    main()
