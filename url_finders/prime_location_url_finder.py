from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
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
        print(f"\nFetching url {url_to_scrape}\n")
        pl_driver.get(url_to_scrape)
        wait = WebDriverWait(pl_driver, 10)
        element = wait.until(EC.visibility_of_element_located((By.NAME, "search-form")))

        def more_pages() -> bool:
            """
            Checks if there are more pages to scrape.

            INPUT: None
            OUTPUT: Dictionary with
                    0: Next page to scrape.
                    1: True if there are more pages, False otherwise.
            """
            next_page = str(int(pl_driver.find_element_by_xpath(
                "//div[@class='paginate bg-muted']/span[@class='current']").text) + 1)
            pages = pl_driver.find_elements_by_xpath("//div[@class='paginate bg-muted']/a")

            return {
                0: next_page,
                1: next_page in [page.text for page in pages]}

        def click_search():
            """ Clicks the search button """
            pl_driver.find_element_by_xpath("//button[@value='Search']").click()

        areas_of_UK = ["London", "South East England", "East Midlands", "East of England", "North East England", "North West England", "South West England", "West Midlands", "Yorkshire and The Humber", "Isle of Man", "Channel Isles", "Scotland", "Wales", "Northern Ireland"]

        # Quitting the cookies banner
        pl_driver.find_element_by_xpath(
            "//button[@title='Agree to our use of cookies']").click()

        # Selecting the "To rent" option
        pl_driver.find_element_by_xpath("//option[@value='to-rent']").click()

        # Entering the city
        pl_driver.find_element_by_xpath(
            "//input[@id='search-input-location']").send_keys(f"{areas_of_UK[-1]}")
        click_search()

        # Selecting the 50 entries per page (maximum)
        Select(pl_driver.find_element_by_xpath(
            "//select[@name='page_size']")).select_by_value(value='50')

        to_rent_links = []
        for area in areas_of_UK: # Search each area
            search_next = pl_driver.find_element_by_xpath("//input[@id='location']")
            search_next.clear()
            search_next.send_keys(f"{area}")
            click_search()
            print(f"Searching for region of {area}")

            # While there are pages left
            while True:
                # Getting all the links
                links = pl_driver.find_elements_by_xpath("//div[@class='listing-results-wrapper']//a[@class='photo-hover']")
                for link in links:
                    to_rent_links.append(link.get_attribute("href"))
                    #print(link.get_attribute("href"))
                print(f"Scraped first {len(to_rent_links)} links")

                # Going to next search page
                search_pages = more_pages()
                if search_pages[1]:
                    pl_driver.find_element_by_xpath(
                f"//div[@class='paginate bg-muted']\
/a[contains(text(),'{search_pages[0]}')]").click()
                else:
                    break

                # Quitting alerts popup
                try:
                    pl_driver.find_element_by_xpath(
                        "//div[@class='alerts-popup-wrapper']//a[@href='#']").click()
                except Exception:
                    pass
                print(f"Scraping page: {search_pages[0]}")

        self.save_urls_to_db(to_rent_links)