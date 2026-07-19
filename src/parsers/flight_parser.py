import re

from playwright.sync_api import Page

from src.models.flight import Flight


class FlightParser:

    def parse(self, page: Page):

        cards = page.locator("li.pIav2d")

        print(f"Cards encontrados: {cards.count()}")

        flights = []

        for i in range(cards.count()):

            texto = cards.nth(i).inner_text()

            # Ignora os cards detalhados (duplicados)
            if "Selecionar voo" in texto:
                continue

            linhas = [
                l.strip()
                for l in texto.splitlines()
                if l.strip()
            ]

            try:

                departure = linhas[0]
                arrival = linhas[2]

                airline = next(
                    l for l in linhas
                    if "LATAM" in l or "Gol" in l or "Azul" in l
                )
                airline = airline.split("Operado por")[0].strip()

                duration = next(
                    l for l in linhas
                    if re.match(r"\d+h", l)
                )

                route = next(
                    l for l in linhas
                    if "–" in l and "GRU" in l
                )

                stops = next(
                    l for l in linhas
                    if "escala" in l.lower()
                )

                price_text = next(
                    l for l in linhas
                    if "R$" in l
                )

                price = int(
                    re.sub(r"[^\d]", "", price_text)
                )

                flights.append(
                    Flight(
                        airline=airline,
                        departure=departure,
                        arrival=arrival,
                        duration=duration,
                        route=route,
                        stops=stops,
                        price=price,
                    )
                )

            except Exception as e:
                print(f"Erro no voo {i}: {e}")

        return flights