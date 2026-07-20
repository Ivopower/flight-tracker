from dataclasses import dataclass


@dataclass
class FlightSearch:

    id: str
    name: str
    enabled: bool

    origin: str
    destination: str
    departure_date: str

    target_price: int | None

    url: str