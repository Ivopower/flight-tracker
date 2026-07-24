from datetime import datetime

from src.config.search_loader import SearchLoader
from src.database.database import Database
from src.notifications.telegram_notifier import TelegramNotifier
from src.services.price_monitor_service import PriceMonitorService
from src.services.search_service import SearchService
from src.analytics.price_analyzer import PriceAnalyzer
from src.repositories.flight_repository import FlightRepository
from src.services.alert_service import AlertService

def main():

    database = Database()
    database.create_tables()

    searches = SearchLoader.load()

    repository = FlightRepository()

    repository.cleanup_expired_history(searches)

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

    print()
    print("==========================")
    print("ANÁLISE HISTÓRICA")
    print("==========================")

    for change in all_changes:

        history = repository.get_price_history(
            search_id=change.search_id,
            airline=change.current.airline,
            departure=change.current.departure,
            arrival=change.current.arrival,
        )

        analysis = PriceAnalyzer.analyze(history)

        if analysis is None:
            continue

        recommendation = AlertService.build_recommendation(
            analysis,
            change.target_price,
        )

        print()
        print(change.search_name)
        print(f"Atual : R$ {analysis.current.price:.2f}")
        print(f"Menor: R$ {analysis.cheapest.price:.2f}")
        print(f"Média : R$ {analysis.average_price:.2f}")
        print(f"Maior: R$ {analysis.most_expensive.price:.2f}")
        print(f"Histórico: {analysis.total_searches}")
        print(recommendation)

    TelegramNotifier().send(
        changes=all_changes,
        monitored_routes=len(searches),
        best_flights=best_flights,
    )

    print("✅ Telegram enviado.")


if __name__ == "__main__":
    main()