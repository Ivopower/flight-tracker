from src.database.database import Database
from src.models.flight_search import FlightSearch
from src.repositories.flight_repository import FlightRepository
from src.services.search_service import SearchService


def main():

    database = Database()
    database.create_tables()

    search = FlightSearch(
        origin="GRU",
        destination="GYN",
        departure_date="2026-11-14",
    )

    service = SearchService()

    flights = service.search(search)

    repository = FlightRepository()

    for flight in flights:
        repository.save(search, flight)

    print(f"\nVoos encontrados: {len(flights)}\n")

    for flight in flights:
        print(flight)

    print("\n==========================")
    print("VOO MAIS BARATO")
    print("==========================\n")

    cheapest = repository.get_cheapest()

    print(cheapest)

    print()
    print(f"Companhia : {cheapest.airline}")
    print(f"Preço     : R$ {cheapest.price:.2f}")
    print(f"Saída     : {cheapest.departure}")
    print(f"Chegada   : {cheapest.arrival}")
    print(f"Duração   : {cheapest.duration}")


if __name__ == "__main__":
    main()