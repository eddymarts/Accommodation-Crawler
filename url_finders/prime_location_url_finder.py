import time
from typing import List
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from pprint import pprint
# from cities import get_cities

from url_finders.url_finder import UrlFinder

class PrimeLocationUrlFinder(UrlFinder):
    def __init__(self, db_session) -> None:
        self.parser_to_use = "PrimeLocation"
        super().__init__(db_session)

    # Return all the URLs we want to scrape
    def find(self):
        # PrimeLocation driver
        pl_driver = webdriver.Chrome()
        url_to_scrape="https://www.primelocation.com/"
        print(f"\nFetching url{url_to_scrape}\n")
        pl_driver.get(url_to_scrape)
        wait = WebDriverWait(pl_driver, 10)
        element = wait.until(EC.visibility_of_element_located((By.NAME, "search-form")))


        # Selecting the "To rent" option
        to_rent = pl_driver.find_element_by_xpath("//option[@value='to-rent']")
        to_rent.click()


        # Entering the city
        search_text = pl_driver.find_element_by_xpath("//input[@id='search-input-location']")
        search_text.send_keys("London")
        print("Searching for city London")

        # Clicking the search button
        search_button = pl_driver.find_element_by_xpath("//button[@value='Search']")
        search_button.click()


        # Selecting the 50 entries per page (maximum)
        entries_50 = Select(pl_driver.find_element_by_xpath("//select[@name='page_size']"))
        entries_50.select_by_value(value='50')


        to_rent_links = []
        featured_links = pl_driver.find_elements_by_xpath("//ul[@id='featured_listings']/li//div[@class='status-wrapper']/a")
        for link in featured_links:
            to_rent_links.append(link.get_attribute("href"))
        print("Scraped first 50 links")

        links = pl_driver.find_elements_by_xpath("//div[@class='listing-results-wrapper']//a[@class='photo-hover']")
        for link in links:
            to_rent_links.append(link.get_attribute("href"))

        # Going to next search page
        next_page = str(int(pl_driver.find_element_by_xpath("//div[@class='paginate bg-muted']/span[@class='current']").text) + 1)
        pages = pl_driver.find_elements_by_xpath("//div[@class='paginate bg-muted']/a")
        if next_page in [page.text for page in pages]:
            pl_driver.find_element_by_xpath(f"//div[@class='paginate bg-muted']/a[contains(text(),'{next_page}')]").click()
        else:
            #Go to next search
            print("go to next search")

        self.save_urls_to_db(to_rent_links)


        # Creating the next search
        # search_next = pl_driver.find_element_by_xpath("//input[@id='location']")
        # search_next.clear()
        # search_next.send_keys("liverpool")
