import json

from src.models.flight_search import FlightSearch


class SearchLoader:

    @staticmethod
    def load() -> list[FlightSearch]:

        with open(
            "config/searches.json",
            encoding="utf-8"
        ) as file:

            searches = json.load(file)

        loaded_searches = []

        for search_data in searches:

            if not search_data["enabled"]:
                continue

            loaded_searches.append(
                FlightSearch(
                    id=search_data["id"],
                    name=search_data["name"],
                    enabled=search_data["enabled"],
                    origin=search_data["origin"],
                    destination=search_data["destination"],
                    departure_date=search_data["departure_date"],
                    target_price=search_data.get("target_price"),
                    url=search_data["url"],
                )
            )

        return loaded_searches