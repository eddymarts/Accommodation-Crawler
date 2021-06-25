from models import Property, UrlToScrape
from url_scrapers.property_scraper import PropertyScraper
from datetime import datetime
from bs4 import BeautifulSoup
import requests
from url_finders.url_finder import UrlFinder

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
        print(f"TODO {self.property_scraper}: scrape url {url}")

