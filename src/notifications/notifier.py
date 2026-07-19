from abc import ABC, abstractmethod

from src.models.price_change import PriceChange


class Notifier(ABC):

    @abstractmethod
    def send(
        self,
        changes: list[PriceChange],
    ):
        pass