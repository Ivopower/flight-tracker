from datetime import datetime

from src.database.database import Database
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

        return self.database.execute(
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