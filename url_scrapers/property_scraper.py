from models import Property, UrlToScrape
from datetime import datetime

class PropertyScraper():
    def __init__(self, db_session) -> None:
        self.db_session = db_session
        pass

    def _mark_url_obj_status(self, url_obj, status):
        print(f"{url_obj.url} = {status}")
        url_obj.scraped_yet = status
        self.db_session.add(url_obj)
        self.db_session.commit()

    def mark_as_currently_scraping(self, url_obj):
        self._mark_url_obj_status(url_obj, 'CURRENTLY_SCRAPING')

    def mark_as_finished_scraping(self, url_obj):
        self._mark_url_obj_status(url_obj, 'FINISHED')

    def mark_as_failed_scraping(self, url_obj):
        self._mark_url_obj_status(url_obj, 'FAILED')


    def get_urls_from_db(self, number_to_scrape):
        query = self.db_session.query(UrlToScrape).filter_by(
            parser_to_use=self.property_scraper
        ).filter_by(
            scraped_yet=False #default value is false
        )

        urls = query[:number_to_scrape] # Limit it to just the ones to scrape
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
        print(f"{self.property_scraper} -- Need to scrape {len(urls_to_scrape)} URLs")
        # print(urls_to_scrape)

        for url_obj in urls_to_scrape:
            url = url_obj.url
            print(f"\n{self.property_scraper} scraping url {url}")
            try:
                self.mark_as_currently_scraping(url_obj)
                self.scrape_url(url)
                self.mark_as_finished_scraping(url_obj)

            except Exception as error:
                print(f"Got error:{error}")
                print(f"Failed to scrape URL: {url}")
                self.mark_as_failed_scraping(url_obj)
