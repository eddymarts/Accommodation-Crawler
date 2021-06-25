from models import Property
from url_scrapers.property_scraper import PropertyScraper
from bs4 import BeautifulSoup
import requests

class ZooplaScraper(PropertyScraper):
    def __init__(self, db_session) -> None:
        self.property_scraper='Zoopla'
        super().__init__(db_session)


    def fetch_url(self, url):
        print(url)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        # print(soup.prettify()[:500])
        return soup

    def scrape_url(self, url):
        # web_page = self.fetch_url(url)
        scraped_property = Property(
            country='country',
            city='city',
            address='address',
            post_code='post_code',
            long_lat='long_lat',

            area_m_2=250.00,
            number_of_bedrooms=None,

            is_rental=None,
            is_shared_accomodation=None,
            is_student=None,
            is_furnished=None,

            price_per_month_gbp=None,
            property_type=None,
            
            url=url,
            description=None,
            pictures=None,

        )

        self.save_property(scraped_property)

        print(f"TODO {self.property_scraper}: scrape url {url}")

