from src.models.flight_search import FlightSearch
from src.services.search_service import SearchService


def main():

    search = FlightSearch(
        origin="GRU",
        destination="GYN",
        departure_date="2026-11-14",
    )

    service = SearchService()

    flights = service.search(search)

    print(f"\nVoos encontrados: {len(flights)}\n")

    for flight in flights:
        print(flight)


if __name__ == "__main__":
    main()