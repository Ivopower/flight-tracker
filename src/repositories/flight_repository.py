from datetime import datetime

from src.database.database import Database
from src.mappers.flight_record_mapper import FlightRecordMapper
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
                searched_at,
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

    def get_latest_search(self):

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
            WHERE searched_at = (
                SELECT MAX(searched_at)
                FROM flights
            )
            ORDER BY price ASC
            """
        ).fetchall()

        return [
            FlightRecordMapper.from_row(row)
            for row in rows
        ]

    def get_flight_history(
        self,
        origin: str,
        destination: str,
        departure_date,
        airline: str,
        departure: str,
        arrival: str,
    ):

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
            WHERE origin = ?
              AND destination = ?
              AND departure_date = ?
              AND airline = ?
              AND departure = ?
              AND arrival = ?
            ORDER BY searched_at ASC
            """,
            (
                origin,
                destination,
                departure_date,
                airline,
                departure,
               arrival,
            ),
        ).fetchall()

        return [
            FlightRecordMapper.from_row(row)
            for row in rows
        ]

    def get_last_flight(
        self,
        origin: str,
        destination: str,
        departure_date,
        airline: str,
        departure: str,
        arrival: str,
    ):

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
            WHERE origin = ?
              AND destination = ?
              AND departure_date = ?
              AND airline = ?
              AND departure = ?
              AND arrival = ?
            ORDER BY searched_at DESC
            LIMIT 1
            """,
            (
                origin,
                destination,
                departure_date,
                airline,
                departure,
                arrival,
            ),
        ).fetchone()

        if row is None:
            return None

        return FlightRecordMapper.from_row(row)