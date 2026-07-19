from dataclasses import dataclass


@dataclass
class Flight:
    airline: str
    departure: str
    arrival: str
    duration: str
    route: str
    stops: str
    price: float

    def __str__(self):
        return (
            f"{self.airline:6} | "
            f"{self.departure} → {self.arrival} | "
            f"{self.duration} | "
            f"{self.stops} | "
            f"R$ {self.price}"
        )