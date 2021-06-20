from models import Property


class UrlScraper():
    def __init__(self, db_session) -> None:
        self.db_session = db_session
        pass

    def save_property(self, property: Property):
        print(f"Saving property: {property}")

    def scrape(self, number_to_scrape):
        for i in range(number_to_scrape):
            print(f"Scraping {i}");
            # Pick them from the DB and scrape them one by one



    def scrape_url(self, url):
        new_prop = Property()
        return new_prop
