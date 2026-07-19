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

            page.goto(
                url,
                wait_until="domcontentloaded"
            )

            # Primeira tentativa
            if not self.__wait_for_results(page):

                print("Resultados não carregaram.")

                # Procura o botão Atualizar
                try:

                    update_button = page.get_by_role(
                        "button",
                        name="Atualizar"
                    )

                    if update_button.is_visible():

                        print("Botão 'Atualizar' encontrado. Tentando novamente...")

                        update_button.click()

                        if self.__wait_for_results(page):

                            print("Resultados carregados após clicar em Atualizar.")

                        else:

                            print("Ainda sem resultados após Atualizar.")

                    else:

                        print("Botão Atualizar não encontrado.")

                except Exception:

                    print("Não foi possível clicar em Atualizar.")

                # Última tentativa
                if not self.__wait_for_results(page):

                    print("Recarregando a página...")

                    page.reload(
                        wait_until="domcontentloaded"
                    )

                    if not self.__wait_for_results(page):

                        page.screenshot(
                            path="data/search_result_error.png",
                            full_page=True
                        )

                        with open(
                            "data/search_result_error.html",
                            "w",
                            encoding="utf-8"
                        ) as f:

                            f.write(page.content())

                        browser.close()

                        raise RuntimeError(
                            "Não foi possível carregar os resultados do Google Flights."
                        )

            parser = FlightParser()

            flights = parser.parse(page)

            page.screenshot(
                path="data/search_result.png",
                full_page=True
            )

            browser.close()

            return flights

    def __wait_for_results(self, page):

        try:

            page.wait_for_selector(
                "li.pIav2d",
                timeout=10000
            )

            return True

        except TimeoutError:

            return False