from datetime import datetime

from src.config.search_loader import SearchLoader
from src.database.database import Database
from src.notifications.telegram_notifier import TelegramNotifier
from src.services.price_monitor_service import PriceMonitorService
from src.services.search_service import SearchService


def main():

    database = Database()
    database.create_tables()

    searches = SearchLoader.load()

    all_changes = []
    best_flights = []

    for search in searches:

        print()
        print("=" * 60)
        print(f"Pesquisando: {search.name}")
        print("=" * 60)

        flights = SearchService().search(search)

        if flights:

            best_flights.append(
                (
                    search,
                    min(
                        flights,
                        key=lambda flight: flight.price,
                    ),
                )
            )

        changes = PriceMonitorService().process(
            search=search,
            flights=flights,
            searched_at=datetime.now(),
        )

        all_changes.extend(changes)

    print()

    if all_changes:

        print("==========================")
        print("ALTERAÇÕES")
        print("==========================")
        print()

        for change in all_changes:

            print(change.current)

            if change.previous is None:

                print("Primeiro registro.")

            else:

                print(
                    f"Antes : R$ {change.previous.price:.2f}"
                )

                print(
                    f"Agora : R$ {change.current.price:.2f}"
                )

                print(
                    f"Variação : R$ {change.difference:.2f}"
                )

                print(
                    f"Percentual : {change.percentage:.2f}%"
                )

            print()

    else:

        print("Nenhuma alteração encontrada.")

    TelegramNotifier().send(
        changes=all_changes,
        monitored_routes=len(searches),
        best_flights=best_flights,
    )

    print("✅ Telegram enviado.")


if __name__ == "__main__":
    main()