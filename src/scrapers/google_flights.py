from playwright.sync_api import TimeoutError, sync_playwright

from src.config import HEADLESS, VIEWPORT
from src.models.flight_search import FlightSearch
from src.parsers.flight_parser import FlightParser
from src.providers.google_flights_provider import GoogleFlightsProvider


class GoogleFlightsScraper:

    def search(self, search: FlightSearch):

        provider = GoogleFlightsProvider()
        url = provider.get_url(search)

        print()
        print("Abrindo:")
        print(url)

        with sync_playwright() as p:

            browser = self.__open_browser(p)

            page = self.__open_page(browser, url)

            self.__ensure_results(page)

            flights = self.__parse(page)

            self.__save_success(page)

            browser.close()

            return flights

    def __open_browser(self, playwright):

        return playwright.chromium.launch(
            headless=HEADLESS,
            args=[
                "--no-sandbox",
                "--disable-dev-shm-usage"
            ]
        )

    def __open_page(self, browser, url):

        page = browser.new_page(
            viewport=VIEWPORT
        )

        page.goto(
            url,
            wait_until="domcontentloaded"
        )

        return page

    def __ensure_results(self, page):

        if self.__wait_for_results(page):
            return

        print("Resultados não carregaram.")

        if self.__click_update(page):

            print("Resultados carregados após clicar em Atualizar.")

            return

        print("Recarregando página...")

        page.reload(
            wait_until="domcontentloaded"
        )

        if self.__wait_for_results(page):
            return

        self.__save_error(page)

        raise RuntimeError(
            "Não foi possível carregar os resultados do Google Flights."
        )

    def __wait_for_results(self, page):

        try:

            page.wait_for_selector(
                "li.pIav2d",
                timeout=10000
            )

            return True

        except TimeoutError:

            return False

    def __click_update(self, page):

        try:

            button = page.get_by_role(
                "button",
                name="Atualizar"
            )

            if not button.is_visible():
                return False

            print("Botão 'Atualizar' encontrado.")

            button.click()

            return self.__wait_for_results(page)

        except Exception:

            return False

    def __parse(self, page):

        parser = FlightParser()

        return parser.parse(page)

    def __save_success(self, page):

        page.screenshot(
            path="data/search_result.png",
            full_page=True
        )

    def __save_error(self, page):

        page.screenshot(
            path="data/search_result_error.png",
            full_page=True
        )

        with open(
            "data/search_result_error.html",
            "w",
            encoding="utf-8"
        ) as file:

            file.write(page.content())