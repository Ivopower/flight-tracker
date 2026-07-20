from datetime import datetime

from src.models.flight import Flight
from src.models.flight_search import FlightSearch
from src.models.price_change import PriceChange
from src.repositories.flight_repository import FlightRepository


class PriceMonitorService:

    def __init__(self):

        self.repository = FlightRepository()

    def process(
        self,
        search: FlightSearch,
        flights: list[Flight],
        searched_at: datetime,
    ) -> list[PriceChange]:

        changes = []

        for flight in flights:

            last = self.repository.get_last_flight(
                search_id=search.id,
                airline=flight.airline,
                departure=flight.departure,
                arrival=flight.arrival,
            )

            if last is None:

                self.repository.save(
                    search=search,
                    flight=flight,
                    searched_at=searched_at,
                )

                changes.append(
                    PriceChange(
                        previous=None,
                        current=flight,
                        search_name=search.name,
                        target_price=search.target_price,
                        difference=0,
                        percentage=0,
                    )
                )

                continue

            if last.price == flight.price:
                continue

            difference = flight.price - last.price

            percentage = (
                difference / last.price
            ) * 100

            self.repository.save(
                search=search,
                flight=flight,
                searched_at=searched_at,
            )

            changes.append(
                PriceChange(
                    previous=last,
                    current=flight,
                    search_name=search.name,
                    difference=difference,
                    target_price=search.target_price,
                    percentage=percentage,
                )
            )

        return changes