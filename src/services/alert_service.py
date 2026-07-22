from src.models.price_analysis import PriceAnalysis


class AlertService:

    @staticmethod
    def build_recommendation(
        analysis: PriceAnalysis,
        target_price: int | None,
    ) -> str:

        current_price = analysis.current.price
        average_price = analysis.average_price
        cheapest_price = analysis.cheapest.price

        if target_price is not None:

            if (
                current_price == cheapest_price
                and current_price <= target_price
            ):
                return "🟢 Excelente oportunidade"

            if current_price < average_price:
                return "🟡 Vale acompanhar"

            return "🔴 Acima do valor desejado"

        if current_price == cheapest_price:
            return "🟢 Excelente oportunidade"

        if current_price < average_price:
            return "🟡 Vale acompanhar"

        return "🔴 Acima do valor desejado"