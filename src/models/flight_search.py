from dataclasses import dataclass


@dataclass
class FlightSearch:

    origin: str
    destination: str
    departure_date: str