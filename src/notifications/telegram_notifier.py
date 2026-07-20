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

        lines = []

        lines.append("✈️ Flight Tracker")
        lines.append("")

        lines.append(f"Foram encontradas {len(changes)} alteração(ões).")
        lines.append("")

        for change in changes:

            lines.append(change.emoji)

            lines.append(change.current.airline)

            lines.append(
                f"{change.current.departure} → {change.current.arrival}"
            )

            if change.previous is None:

                lines.append(
                    f"Primeiro monitoramento: R$ {change.current.price:.2f}"
                )

            else:

                lines.append(
                    f"Antes : R$ {change.previous.price:.2f}"
                )

                lines.append(
                    f"Agora : R$ {change.current.price:.2f}"
                )

                lines.append(
                    f"Variação : R$ {change.difference:.2f}"
                )

                lines.append(
                    f"({change.percentage:.2f}%)"
                )

            lines.append("")
            lines.append("-------------------------")
            lines.append("")

        return "\n".join(lines)