from dataclasses import dataclass

from src.models.flight import Flight


@dataclass
class PriceChange:

    previous: Flight | None
    current: Flight

    difference: float
    percentage: float

    @property
    def decreased(self) -> bool:

        return self.difference < 0

    @property
    def increased(self) -> bool:

        return self.difference > 0

    @property
    def emoji(self) -> str:

        if self.decreased:
            return "🟢⬇️"

        if self.increased:
            return "🔴⬆️"

        return "⚪"