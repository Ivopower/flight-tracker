from datetime import datetime

from src.database.database import Database
from src.models.flight import Flight
from src.models.flight_search import FlightSearch


class FlightRepository:

    def __init__(self):

        self.database = Database()

    def save(
        self,
        search: FlightSearch,
        flight: Flight,
        searched_at: datetime,
    ):

        self.database.execute(
            """
            INSERT INTO flights (
                searched_at,
                search_id,
                airline,
                departure,
                arrival,
                duration,
                route,
                stops,
                price
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                searched_at,
                search.id,
                flight.airline,
                flight.departure,
                flight.arrival,
                flight.duration,
                flight.route,
                flight.stops,
                flight.price,
            ),
        )

    def get_last_flight(
        self,
        search_id: str,
        airline: str,
        departure: str,
        arrival: str,
    ):

        row = self.database.execute(
            """
            SELECT
                airline,
                departure,
                arrival,
                duration,
                route,
                stops,
                price
            FROM flights
            WHERE search_id = ?
              AND airline = ?
              AND departure = ?
              AND arrival = ?
            ORDER BY searched_at DESC
            LIMIT 1
            """,
            (
                search_id,
                airline,
                departure,
                arrival,
            ),
        ).fetchone()

        if row is None:
            return None

        return Flight(
            airline=row[0],
            departure=row[1],
            arrival=row[2],
            duration=row[3],
            route=row[4],
            stops=row[5],
            price=row[6],
        )

    def get_price_history(
        self,
        search_id: str,
        airline: str,
        departure: str,
        arrival: str,
    ) -> list[Flight]:

        rows = self.database.execute(
            """
            SELECT
                airline,
                departure,
                arrival,
                duration,
                route,
                stops,
                price
            FROM flights
            WHERE search_id = ?
              AND airline = ?
              AND departure = ?
              AND arrival = ?
            ORDER BY searched_at
            """,
            (
                search_id,
                airline,
                departure,
                arrival,
            ),
        ).fetchall()

        return [
            Flight(
                airline=row[0],
                departure=row[1],
                arrival=row[2],
                duration=row[3],
                route=row[4],
                stops=row[5],
                price=row[6],
            )
            for row in rows
        ]