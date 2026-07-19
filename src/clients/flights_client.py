from src.models.flight import Flight


class FlightsClient:

    def search(self):

        print("Buscando voos...")

        return [
            Flight(
                airline="LATAM",
                departure="08:20",
                arrival="10:00",
                duration="1h40",
                stops="Direto",
                price=529.90
            ),
            Flight(
                airline="GOL",
                departure="12:35",
                arrival="14:15",
                duration="1h40",
                stops="Direto",
                price=612.00
            )
        ]