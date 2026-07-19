from dataclasses import dataclass
from datetime import date, datetime


@dataclass
class FlightRecord:

    searched_at: datetime
    origin: str
    destination: str
    departure_date: date

    airline: str
    departure: str
    arrival: str

    duration: str
    route: str
    stops: str

    price: float

    def __str__(self):

        return (
            f"{self.airline:<7} | "
            f"{self.departure} → {self.arrival} | "
            f"{self.duration} | "
            f"{self.stops} | "
            f"R$ {self.price:.0f}"
        )