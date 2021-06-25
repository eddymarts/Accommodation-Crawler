from models import Property, UrlToScrape
from datetime import datetime

class PropertyScraper():
    def __init__(self, db_session) -> None:
        self.db_session = db_session
        pass

    def mark_as_currently_scraping(self, url_objects):
        pass
        # url_objects.

    def get_urls_from_db(self, number_to_scrape):
        query = self.db_session.query(UrlToScrape).filter_by(
            parser_to_use=self.property_scraper
        )

        urls = query[:number_to_scrape] # Limit it to just the ones to scrape
        self.mark_as_currently_scraping(urls)
        return urls

    def current_date(self):
        # datetime object containing current date and time
        now = datetime.now()
        return now;

    def save_property(self, property_object):
        property_object.updated_date=self.current_date();
        
        self.db_session.add(property_object)
        self.db_session.commit()

    def scrape(self, number_to_scrape):
        urls_to_scrape = self.get_urls_from_db(number_to_scrape)
        # print(f"{self.property_scraper} -- Need to scrape these URLS:")
        # print(urls_to_scrape)

        for url_obj in urls_to_scrape:
            url = url_obj.url
            print(f"Scraping {url}");
            try:
                self.scrape_url(url)

            except Exception as error:
                print(f"Got error:{error}")
                print(f"Failed to scrape URL: {url}")
