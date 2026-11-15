import sqlite3
from typing import List, Tuple


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


def rainfall_for_year(
    connection: sqlite3.Connection, year: int
) -> List[Tuple[str, int]]:
    """Return (city, rainfall amount) rows for a year, ordered by city.

    `year` is the value for the SQL WHERE filter. The returned fields are the
    columns selected from the joined cities and rainfall tables.
    """
    rows = connection.execute(
        """
        SELECT cities.city, rainfall.amount
        FROM cities
        INNER JOIN rainfall ON cities.city_id = rainfall.city_id
        WHERE rainfall.year = ?
        ORDER BY cities.city ASC
        """,
        (year,),
    )
    return rows.fetchall()


def main() -> None:
    """Run the local sample and print the ordered query results."""
    with sqlite3.connect(":memory:") as connection:
        create_schema(connection)
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
        for city, amount in rainfall_for_year(connection, 2019):
            print("{}: {} mm".format(city, amount))


if __name__ == "__main__":
    main()
