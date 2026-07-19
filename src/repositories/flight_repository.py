from datetime import datetime

from src.database.database import Database
from src.mappers.flight_record_mapper import FlightRecordMapper
from src.models.flight import Flight
from src.models.flight_search import FlightSearch


class FlightRepository:

    def __init__(self):

        self.database = Database()

    def save(self, search: FlightSearch, flight: Flight):

        self.database.execute(
            """
            INSERT INTO flights (
                searched_at,
                origin,
                destination,
                departure_date,
                airline,
                departure,
                arrival,
                duration,
                route,
                stops,
                price
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                datetime.now(),
                search.origin,
                search.destination,
                search.departure_date,
                flight.airline,
                flight.departure,
                flight.arrival,
                flight.duration,
                flight.route,
                flight.stops,
                flight.price,
            ),
        )

    def get_all(self):

        rows = self.database.execute(
            """
            SELECT
                searched_at,
                origin,
                destination,
                departure_date,
                airline,
                departure,
                arrival,
                duration,
                route,
                stops,
                price
            FROM flights
            ORDER BY searched_at DESC
            """
        ).fetchall()

        return [
            FlightRecordMapper.from_row(row)
            for row in rows
        ]

    def get_cheapest(self):

        row = self.database.execute(
            """
            SELECT
                searched_at,
                origin,
                destination,
                departure_date,
                airline,
                departure,
                arrival,
                duration,
                route,
                stops,
                price
            FROM flights
            ORDER BY price ASC
            LIMIT 1
            """
        ).fetchone()

        if row is None:
            return None

        return FlightRecordMapper.from_row(row)