from statistics import mean

from src.models.price_analysis import PriceAnalysis


class PriceAnalyzer:

    @staticmethod
    def analyze(history):

        if not history:
            return None

        prices = [flight.price for flight in history]

        current = history[-1]

        cheapest = min(
            history,
            key=lambda x: x.price
        )

        most_expensive = max(
            history,
            key=lambda x: x.price
        )

        return PriceAnalysis(
            current=current,
            cheapest=cheapest,
            most_expensive=most_expensive,
            average_price=mean(prices),
            total_searches=len(history),
        )