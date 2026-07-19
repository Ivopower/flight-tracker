from datetime import datetime

from src.database.database import Database
from src.models.flight_search import FlightSearch
from src.services.price_monitor_service import PriceMonitorService
from src.services.search_service import SearchService


def main():

    database = Database()
    database.create_tables()

    search = FlightSearch(
        origin="GRU",
        destination="GYN",
        departure_date="2026-11-14",
    )

    flights = SearchService().search(search)

    changes = PriceMonitorService().process(
        search=search,
        flights=flights,
        searched_at=datetime.now(),
    )

    print()

    print("==========================")
    print("ALTERAÇÕES")
    print("==========================")

    print()

    if not changes:

        print("Nenhuma alteração encontrada.")
        return

    for change in changes:

        print(change.current)

        if change.previous is None:

            print("Primeiro registro.")

        else:

            print(
                f"Anterior : R$ {change.previous.price:.2f}"
            )

            print(
                f"Atual    : R$ {change.current.price:.2f}"
            )

            print(
                f"Variação : R$ {change.difference:.2f}"
            )

            print(
                f"Percentual: {change.percentage:.2f}%"
            )

        print()