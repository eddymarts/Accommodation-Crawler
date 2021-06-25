from datetime import datetime
from bs4 import BeautifulSoup
import requests
from url_finders.url_finder import UrlFinder

# How do you know what you want to scrape
# https://www.zoopla.co.uk/to-rent/property/london/?page_size=25&price_frequency=per_month&q=london&radius=0&results_sort=newest_listings&pn=2
areas_of_UK = ["London", "South East England", "East Midlands", "East of England", "North East England", "North West England", "South West England", "West Midlands", "Yorkshire and The Humber", "Isle of Man", "Channel Isles", "Scotland", "Wales", "Northern Ireland"]

class ZooplaUrlFinder(UrlFinder):
    def __init__(self, db_session) -> None:
        self.parser_to_use = "Zoopla"
        super().__init__(db_session)


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

            self.save_urls_to_db(sub_pages)
        print(f"Finished scraping for {region}")

    def find(self):
        # finds URLs and saves them to the DB.
        for region in areas_of_UK:
            self.scrape_URLs_for_region(region)

