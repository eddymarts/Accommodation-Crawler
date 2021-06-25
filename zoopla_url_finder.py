from models import UrlToScrape
from datetime import datetime
from bs4 import BeautifulSoup
import requests

# How do you know what you want to scrape
# https://www.zoopla.co.uk/to-rent/property/london/?page_size=25&price_frequency=per_month&q=london&radius=0&results_sort=newest_listings&pn=2
areas_of_UK = ["London", "South East England", "East Midlands", "East of England", "North East England", "North West England", "South West England", "West Midlands", "Yorkshire and The Humber", "Isle of Man", "Channel Isles", "Scotland", "Wales", "Northern Ireland"]

class UrlFinder():
    def __init__(self, db_session) -> None:
        self.db_session = db_session
        pass

    def current_date(self):
        # datetime object containing current date and time
        now = datetime.now()
        # dd/mm/YY H:M:S
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        dt_string = now.strftime("%d/%m/%Y--%H:%M:%S")
        return dt_string

    def fetch_url(self, url):
        print(url)
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        # print(soup.prettify()[:500])
        # print(soup)
        return soup

    def scrape_urls_from_page(self, web_page):
        urls = [f"https://www.zoopla.co.uk{item['href']}" for item in web_page.find_all('a', attrs={'data-testid' : True}) if item['data-testid']=='listing-details-link']
        return urls;


    def create_db_object_from_url(self, new_url):
        new_url_obj = UrlToScrape(
            url=new_url,
            parser_to_use='Zoopla',
            scraped_yet=False
        )

        self.db_session.add(new_url_obj)
        self.db_session.commit()


    def scrape_URLs_for_region(self, region):
        print(f"\n\nBEGINNING SCRAPING FOR {region}\n")

        page_number = 0
        end_of_search = False

        while not end_of_search:
            page_number = page_number+1
            url = f"https://www.zoopla.co.uk/to-rent/property/{region}/?page_size=50&price_frequency=per_month&q={region}&radius=0&results_sort=newest_listings&pn={page_number}"
            
            web_page = self.fetch_url(url)

            sub_pages = self.scrape_urls_from_page(web_page)
            if len(sub_pages) == 0:
                end_of_search = True

            for page in sub_pages:
                self.create_db_object_from_url(page)
        print(f"Finished scraping for {region}")

    def find(self):
        
        # finds URLs and saves them to the DB.
        for region in areas_of_UK:
            urls_for_region = self.scrape_URLs_for_region(region)

        # self.db_session.commit()
