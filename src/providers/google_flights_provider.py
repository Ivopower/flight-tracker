from src.models.flight_search import FlightSearch


class GoogleFlightsProvider:

    def get_url(self, search: FlightSearch) -> str:

        return (
            "https://www.google.com/travel/flights/search?"
            "tfs=CBwQAhoeEgoyMDI2LTExLTE0agcIARIDR1JV"
            "cgcIARIDR1lOQAFIAXABggELCP___________wGYAQI"
            "&tfu=EgYIABAAGAA"
            "&hl=pt-BR"
            "&gl=BR"
        )