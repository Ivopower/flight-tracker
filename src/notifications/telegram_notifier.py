import os

import requests
from dotenv import load_dotenv

from src.models.price_change import PriceChange
from src.analytics.price_analyzer import PriceAnalyzer
from src.repositories.flight_repository import FlightRepository
from src.services.alert_service import AlertService

load_dotenv()


class TelegramNotifier:

    def __init__(self):

        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")
        self.repository = FlightRepository()

    def send(
        self,
        changes: list[PriceChange],
        monitored_routes: int,
        best_flights: list,
    ):



        message = self.__build_message(
            changes=changes,
            monitored_routes=monitored_routes,
            best_flights=best_flights,
        )

        print(f"BOT TOKEN: {self.token[:10]}...")
        print(f"CHAT ID: {self.chat_id}")

        response = requests.post(
            f"https://api.telegram.org/bot{self.token}/sendMessage",
            json={
                "chat_id": self.chat_id,
                "text": message,
            },
            timeout=30,
        )

        print(f"Status Code: {response.status_code}")
        print(f"Resposta: {response.text}")

    def __build_message(
        self,
        changes: list[PriceChange],
        monitored_routes: int,
        best_flights: list,
    ) -> str:

        drops = sum(1 for c in changes if c.previous and c.decreased)
        increases = sum(1 for c in changes if c.previous and c.increased)

        groups: dict[str, list[PriceChange]] = {}

        for change in changes:

            groups.setdefault(
                change.search_name,
                []
            ).append(change)

        lines = []

        lines.append("✈️ Flight Tracker")
        lines.append("")
        lines.append("📊 RESUMO")
        lines.append(f"🏷️ Rotas monitoradas: {monitored_routes}")
        lines.append(f"🔄 Rotas alteradas: {len(groups)}")
        lines.append(f"✈️ Alterações: {len(changes)}")
        lines.append(f"📉 Quedas: {drops}")
        lines.append(f"📈 Altas: {increases}")

        # ==========================================
        # NÃO HOUVE ALTERAÇÕES
        # ==========================================
        if not changes:

            lines.append("")
            lines.append("ℹ️ Nenhuma alteração encontrada.")
            lines.append("")
            lines.append("🏆 Melhor preço por rota")

            for search, flight in best_flights:

                lines.append("")
                lines.append("━━━━━━━━━━━━━━━━━━━━")
                lines.append("")
                lines.append(f"📍 {search.name}")
                lines.append("")
                lines.append(f"💰 R$ {flight.price:.2f}")

                if search.target_price is not None:

                    lines.append(f"🎯 Meta: R$ {search.target_price:.2f}")

                    delta = flight.price - search.target_price

                    if delta <= 0:

                        lines.append(
                            f"✅ R$ {abs(delta):.2f} abaixo da meta"
                        )

                    else:

                        lines.append(
                            f"⚠️ R$ {delta:.2f} acima da meta"
                        )

                lines.append("")
                lines.append(
                    f"{self.__airline_emoji(flight.airline)} {flight.airline}"
                )
                lines.append(
                    f"🕒 {flight.departure} → {flight.arrival}"
                )
                lines.append(
                    f"⏱️ {flight.duration}"
                )
                lines.append(
                    f"🛫 {flight.stops}"
                )
                lines.extend(
                    self.__build_history(
                        search.id,
                        flight,
                        search.target_price,
                    )
                )

            return "\n".join(lines)

        # ==========================================
        # HOUVE ALTERAÇÕES
        # ==========================================

        for flights in groups.values():

            flights.sort(
                key=lambda change: (
                    change.current.price,
                    change.current.departure,
                )
            )

        ordered_groups = sorted(
            groups.items(),
            key=lambda item: item[1][0].current.price,
        )

        for search_name, flights in ordered_groups:

            lines.append("")
            lines.append("━━━━━━━━━━━━━━━━━━━━")
            lines.append("")
            lines.append(f"📍 {search_name}")
            lines.append("")
            lines.append("🏆 MELHOR OFERTA")
            lines.append("")

            lines.extend(
                self.__build_card(
                    flights[0]
                )
            )

            if len(flights) > 1:

                lines.append("✈️ OUTRAS OPÇÕES")
                lines.append("")

                for flight in flights[1:]:

                    lines.extend(
                        self.__build_card(change)
                    )

        return "\n".join(lines)

    def __build_card(
        self,
        change: PriceChange,
    ) -> list[str]:

        flight = change.current

        lines = []

        lines.append("━━━━━━━━━━━━━━━━━━━━")
        lines.append("")
        lines.append(f"📍 {change.search_name}")
        lines.append("")
        lines.append(f"💰 R$ {flight.price:.2f}")

        if change.target_price is not None:

            lines.append(f"🎯 Meta: R$ {change.target_price:.2f}")

            delta = flight.price - change.target_price

            if delta <= 0:

                lines.append(
                    f"✅ R$ {abs(delta):.2f} abaixo da meta"
                )

            else:

                lines.append(
                    f"⚠️ R$ {delta:.2f} acima da meta"
                )

        lines.append("")

        lines.append(
            f"{self.__airline_emoji(flight.airline)} {flight.airline}"
        )

        lines.append(
            f"🕒 {flight.departure} → {flight.arrival}"
        )

        lines.append(
            f"⏱️ {flight.duration}"
        )

        lines.append(
            f"🛫 {flight.stops}"
        )

        lines.append("")

        if change.previous is None:

            lines.append("🆕 Primeiro monitoramento")

        else:

            if change.decreased:

                lines.append(
                    f"📉 -R$ {abs(change.difference):.2f} ({change.percentage:.2f}%)"
                )

            elif change.increased:

                lines.append(
                    f"📈 +R$ {change.difference:.2f} (+{change.percentage:.2f}%)"
                )

            else:

                lines.append("⚪ Sem alteração")

        lines.extend(
            self.__build_history(
                change.search_id,
                flight,
                change.target_price,
            )
        )

        return lines

    def __build_history(
        self,
        search_id: str,
        flight,
        target_price: int | None,
    ) -> list[str]:

        lines = []

        history = self.repository.get_price_history(
            search_id=search_id,
            airline=flight.airline,
            departure=flight.departure,
            arrival=flight.arrival,
        )

        analysis = PriceAnalyzer.analyze(history)

        if analysis is None:
            return lines

        recommendation = AlertService.build_recommendation(
            analysis,
            target_price,
        )

        lines.append("")
        lines.append(recommendation)
        lines.append("")
        lines.append("📊 Histórico")
        lines.append(f"📉 Menor: R$ {analysis.cheapest.price:.2f}")
        lines.append(f"📊 Média: R$ {analysis.average_price:.2f}")
        lines.append(f"📈 Maior: R$ {analysis.most_expensive.price:.2f}")

        return lines

    def __airline_emoji(
        self,
        airline: str,
    ) -> str:

        airline = airline.upper()

        if "LATAM" in airline:
            return "🔴"

        if "GOL" in airline:
            return "🟠"

        if "AZUL" in airline:
            return "🔵"

        return "⚪"