from src.scrapers.google_flights import GoogleFlightsScraper


class SearchService:

    def search(self, search):

        scraper = GoogleFlightsScraper()

        return scraper.search(search)