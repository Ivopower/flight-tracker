from playwright.sync_api import sync_playwright

from src.config import HEADLESS, VIEWPORT
from src.models.flight_search import FlightSearch
from src.providers.google_flights_provider import GoogleFlightsProvider
from src.parsers.flight_parser import FlightParser


class GoogleFlightsScraper:

    def search(self, search: FlightSearch):

        provider = GoogleFlightsProvider()
        url = provider.get_url(search)

        print()
        print("Abrindo:")
        print(url)

        with sync_playwright() as p:

            browser = p.chromium.launch(
                headless=HEADLESS,
                args=[
                    "--no-sandbox",
                    "--disable-dev-shm-usage"
                ]
            )

            page = browser.new_page(
                viewport=VIEWPORT
            )

            page.goto(url)

            page.wait_for_load_state("domcontentloaded")

            page.wait_for_timeout(8000)

            parser = FlightParser()
            flights = parser.parse(page)

            page.screenshot(
                path="data/search_result.png",
                full_page=True
            )

            browser.close()

            return flights
