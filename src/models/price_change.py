from dataclasses import dataclass

from src.models.flight import Flight
from src.models.flight_record import FlightRecord


@dataclass
class PriceChange:

    previous: FlightRecord | None

    current: Flight

    difference: float

    percentage: float