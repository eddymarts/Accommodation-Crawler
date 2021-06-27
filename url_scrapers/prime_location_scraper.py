from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from models import Property
from url_scrapers.property_scraper import PropertyScraper

class PrimeLocationScraper(PropertyScraper):
    def __init__(self, db_session) -> None:
        self.property_scraper='PrimeLocation'
        super().__init__(db_session)
    
    def get_area_sqft(self) -> int:
        """
        Returns area as an integer in squared feet.
        """
        try:
            area_sqft = int(self.driver.find_element_by_xpath(
            "//span[@class='num-icon num-sqft ']").text.split()[0].translate(
                    {ord(','): ''}))
        except:
            area_sqft = "NaN"

        return area_sqft
    def get_property_features(self) -> list:
        """
        Returns property features.
        """
        
        try:
            property_features = [feature.text for feature in
                self.driver.find_elements_by_xpath(
                "//div[@id='tab-details']/div[@class='clearfix']//li")]

            assert len(property_features) > 0

        except AssertionError:
            property_features = ["NaN"]
        
        return property_features
    
    def get_property_info(self) -> list:
        """
        Gets all property info.
        """
        
        try:
            property_info = [info.text for info in
                self.driver.find_elements_by_xpath(
                "//div[@id='tab-details']/ul/li")]

            assert len(property_info) > 0

        except AssertionError:
            property_info = ["NaN"]
        
        return property_info
    
    def get_beds_baths_receps(self) -> tuple:
        """
        Returns number of bedrooms, number of bathrooms and number of receptions.
        """
        try:
            bedrooms = int(self.driver.find_element_by_xpath(
            "//span[@class='num-icon num-beds']").text.split()[0])
        except:
            bedrooms = "NaN"
        
        try:
            bathrooms = int(self.driver.find_element_by_xpath(
            "//span[@class='num-icon num-baths']").text.split()[0])
        except:
            bathrooms = "NaN"
        
        try:
            receptions = int(self.driver.find_element_by_xpath(
            "//span[@class='num-icon num-reception']").text.split()[0])
        except:
            receptions = "NaN"

        return bedrooms, bathrooms, receptions

    def get_furnished_shared_student(self, all_details: list) -> tuple:
        """
        Returns tuple of bools as follows:
        INPUT: all_details: list of strings, All details of the property

        OUTPUT:
            is_furnished: bool
            is_shared: bool
            is_student: bool
        """

        furnished = 0
        unfurnished = 0
        shared = 0
        no_student = 0

        for detail in all_details:
            if "unfurnished" in detail.lower() or "no furnished" in detail.lower():
                unfurnished += 1
            elif "furnished" in detail.lower():
                furnished += 1
            
            if "shared" in detail.lower():
                shared += 1
            
            if "no student" in detail.lower() or "not for student" in detail.lower():
                no_student += 1
        
        if unfurnished:
            is_furnished = False
        elif furnished:
            is_furnished = True
        else:
            is_furnished = "NaN"
        
        is_shared = shared > 0
        is_student = no_student == 0
            
        return is_furnished, is_shared, is_student

    def get_maps(self) -> tuple:
        """
        Searches for the Google Maps link of the property.

        INPUT: None
        OUTPUT:
            latitude: float
            longitude: float
            Google Maps link: string
        """

        self.driver.find_element_by_xpath("//li[@aria-controls='tab-map']").click()
        self.wait = WebDriverWait(self.driver, 10)
        gmaps_link = self.wait.until(EC.visibility_of_element_located((By.XPATH, "//div[@class='gm-style']//a[@title=\
'Open this area in Google Maps (opens a new window)']"))).get_attribute("href")
        latitude, longitude = [float(coord) for coord in
            gmaps_link.split("ll=")[1].split("&")[0].split(",")]
        
        return latitude, longitude, gmaps_link

    def get_agent(self) -> tuple:
        """
        Returns agency name and phone number.
        """
        agent = self.driver.find_element_by_xpath(
            "//div[@id='listings-agent']//p//a").text
        agent_phone_number = self.driver.find_element_by_xpath(
            "//span[@class='agent_phone']/a").text.translate({ord(' '): ''})
        
        return agent, agent_phone_number

    def scrape_url(self, url):
        ##print(f"TODO {self.property_scraper}: scrape url {url}")
        
        # Open browser
        self.driver = webdriver.Chrome()

        # Open new tab
        self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 't')
        self.driver.get(url)

        agent, agent_phone_number = self.get_agent()
        bedrooms, bathrooms, receptions = self.get_beds_baths_receps()
        area_sqft = self.get_area_sqft()
        property_features = self.get_property_features()
        property_info = self.get_property_info()
        property_description = self.driver.find_element_by_xpath(
            "//div[@class='bottom-plus-half']/div[@class='top']").text
        
        property_details = self.driver.find_element_by_xpath(
        "//h1[@class='listing-details-h1']").text

        is_rental = "to rent" in property_details.lower()

        price_description = self.driver.find_element_by_xpath(
            "//span[@class='price']").text
        
        if is_rental:
            price_for_sale = "NaN"
            price_for_sqft = "NaN"
            property_type, address = property_details.split(" to rent in ")
            if price_description == "POA":
                price_per_month = "NaN"
                price_per_week = "NaN"
            else:
                price_per_month = int(price_description.split()[0].translate(
                        {ord(i): '' for i in '£,'}))
                price_per_week = int(price_description.split()[2].translate(
                        {ord(i): '' for i in '(£,'}))
        else:
            price_per_month = "NaN"
            price_per_week = "NaN"
            property_type, address = property_details.split(" for sale in ")
            if price_description == "POA":
                price_for_sale = "NaN"
                price_for_sqft = "NaN"
            else:
                price_for_sale = int(price_description.split()[0].translate(
                    {ord(i): '' for i in '£,'}))
                price_per_sqft = int(price_description.split()[1].translate(
                    {ord(i): '' for i in '(£,/sq.'}))

        all_details = [property_details] + [
            property_description] + property_features + property_info
        is_furnished, is_shared, is_student = self.get_furnished_shared_student(all_details)
        
        # Not always gets the city
        city, post_code = address.split(", ")[-1].split()
        latitude, longitude, gmaps_link = self.get_maps()
        country = 'GB'
        
        # Close tab
        self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')

        # Close browser
        self.driver.close()

    # id = Column(Integer, primary_key=True)
    # country = Column(String, index=True) DONE
    # city = Column(String, index=True) DONE
    # address = Column(String) Done
    # post_code = Column(String) Done
    # long_lat = Column(String) DONE

    # # area_sqft - Square-footage = Column(String) DONE
    # area_m_2 = Column(Float)
    # number_of_bedrooms = Column(Integer) DONE
    # number_of_bathrooms = Column(Integer) DONE

    # is_rental = Column(Boolean) DONE
    # is_shared_accomodation = Column(Boolean) DONE
    # is_student = Column(Boolean) DONE
    # is_furnished = Column(Boolean) DONE

    # price_per_month_gbp = Column(Float, index=True) DONE
    # property_details = Column(String) # Flat/house/detached/semi-detached DONE
    
    # url = Column(String) DONE
    # description = Column(String) DONE
    # pictures = Column(String)

    # updated_date = Column(DateTime)