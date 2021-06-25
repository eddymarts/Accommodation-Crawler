from models import Property


class UrlScraper():
    def __init__(self, db_session) -> None:
        self.db_session = db_session
        pass

    def save_property(self, property: Property):
        print(f"Saving property: {property}")

    def get_urls_from_db(self, number_to_scrape):
        number_to_scrape
        print("Work in progress")
        return []

    def scrape(self, number_to_scrape):
        urls_to_scrape = self.get_urls_from_db(number_to_scrape)
        for url_obj in urls_to_scrape:
            url = url_obj.url
            print(f"Scraping {url}");



    def scrape_url(self, url):
        new_prop = Property()
        return new_prop
