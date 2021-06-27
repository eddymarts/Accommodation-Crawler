from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from url_finders.url_finder import UrlFinder

class PrimeLocationUrlFinder(UrlFinder):
    def __init__(self, db_session) -> None:
        self.parser_to_use = "PrimeLocation"
        super().__init__(db_session)
        self.url_to_scrape = "https://www.primelocation.com/"
    
    def get_links(self, option, region) -> None:
        """ Gets all property links within a region. """
        page = 1

        while True:
            # Open new tab
            self.driver.find_element_by_tag_name(
                'body').send_keys(Keys.CONTROL + 't') 
            self.driver.get(
        self.url_to_scrape + f"{option}/property/{region}/?\
page_size=50&search_source=refine&radius=0&view_type=grid&pn={page}")

            links = self.driver.find_elements_by_xpath(
"//div[@class='listing-results-wrapper']//a[@class='photo-hover']")
            if links:
                # Save to database
                self.save_urls_to_db([link.get_attribute("href") for link in links])
                self.link_number += len(links)
                print(f"Page {page}: Scraped first {self.link_number} links.")
                page += 1
            else: # End of search
                # Close tab
                self.driver.find_element_by_tag_name(
                    'body').send_keys(Keys.CONTROL + 'w')
                break


    def find(self) -> None:
        """
        Finds all property links in PrimeLocation.com and saves it to local database.
        """
        self.link_number = 0

        # Open browser
        self.driver = webdriver.Chrome()
        areas_of_UK = ["London", "South East England", "East Midlands", "East of England", "North East England", "North West England", "South West England", "West Midlands", "Yorkshire and The Humber", "Isle of Man", "Channel Isles", "Scotland", "Wales", "Northern Ireland"]
        regions = [region.replace(" ", "-") for region in areas_of_UK]

        for option in ["for-sale", "to-rent"]:
            print(f"\nFetching {option} properties in {self.url_to_scrape}\n")

            for region in regions:
                page = 1
                print(f"\nFetching properties in {region}\n")
                self.get_links(option, region)

        # Close browser
        self.driver.close()