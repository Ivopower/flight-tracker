from dataclasses import dataclass

from src.models.flight_record import FlightRecord


@dataclass
class PriceAnalysis:

    current: FlightRecord
    cheapest: FlightRecord
    most_expensive: FlightRecord

    average_price: float

    variation: float

    total_searches: int