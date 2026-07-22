from dataclasses import dataclass

from src.models.flight import Flight


@dataclass
class PriceAnalysis:

    current: Flight

    cheapest: Flight

    most_expensive: Flight

    average_price: float

    total_searches: int

    recommendation: str | None = None