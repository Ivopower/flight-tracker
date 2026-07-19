import base64

from src.models.flight_search import FlightSearch


class GoogleFlightsUrlBuilder:

    BASE_URL = (
        "https://www.google.com/travel/flights/search"
    )

    def build(self, search: FlightSearch) -> str:

        date = self.__encode(search.departure_date)

        origin = self.__encode(search.origin)

        destination = self.__encode(search.destination)

        tfs = (
            f"CBwQAhoeEg{date}"
            f"agcIARID{origin}"
            f"cgcIARID{destination}"
            f"QAFIAXABggELCP___________wGYAQI"
        )

        return (
            f"{self.BASE_URL}"
            f"?tfs={tfs}"
            f"&tfu=EgYIABAAGAA"
            f"&hl=pt-BR"
            f"&gl=BR"
        )

    def __encode(self, value: str) -> str:

        return (
            base64
            .b64encode(value.encode())
            .decode()
        )