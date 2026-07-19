from urllib.parse import urlencode


class GoogleFlightsURLBuilder:

    @staticmethod
    def build(
        origin: str,
        destination: str,
        departure_date: str,
    ) -> str:

        params = {
            "hl": "pt-BR"
        }

        return (
            "https://www.google.com/travel/flights?"
            + urlencode(params)
        )