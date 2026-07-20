import os

import requests
from dotenv import load_dotenv

from src.models.price_change import PriceChange

load_dotenv()


class TelegramNotifier:

    def __init__(self):

        self.token = os.getenv("TELEGRAM_BOT_TOKEN")
        self.chat_id = os.getenv("TELEGRAM_CHAT_ID")

    def send(
        self,
        changes: list[PriceChange],
    ):

        if not changes:
            return

        message = self.__build_message(changes)

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
    ) -> str:

        changes = sorted(
            changes,
            key=lambda change: (
                change.current.price,
                change.current.departure,
            ),
        )

        best = changes[0]

        drops = sum(1 for c in changes if c.previous and c.decreased)
        increases = sum(1 for c in changes if c.previous and c.increased)

        lines = []

        lines.append("✈️ Flight Tracker")
        lines.append("")
        lines.append("📊 RESUMO")
        lines.append(f"🔎 Alterações: {len(changes)}")
        lines.append(f"📉 Quedas: {drops}")
        lines.append(f"📈 Altas: {increases}")
        lines.append("")

        lines.append("🏆 MELHOR OFERTA DO DIA")
        lines.append("")

        lines.extend(self.__build_card(best))

        if len(changes) > 1:

            lines.append("")
            lines.append("━━━━━━━━━━━━━━━━━━━━")
            lines.append("")
            lines.append("✈️ OUTRAS OPÇÕES")
            lines.append("")

            for change in changes[1:]:

                lines.extend(self.__build_card(change))

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

        lines.append("")

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