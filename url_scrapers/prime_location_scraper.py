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

    def get_furnished_shared_student(self, description: str) -> tuple:
        """
        Returns tuple of bools as follows:
        INPUT: all_details: list of strings, All details of the property

        OUTPUT:
            is_furnish: bool
            is_shared: bool
            is_stud: bool
        """
        if "unfurnished" in description or "no furnished" in description:
            is_furnish = False
        elif "furnished" in description:
            is_furnish = True
        else:
            is_furnish = "NaN"
        
        is_shared = "shared" in description
        is_stud = not("no student" in description or "not for student" in description)
        
        return is_furnish, is_shared, is_stud

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

    def find_pictures(self):
        return None

    def scrape_url(self, url):
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

        is_rent = "to rent" in property_details.lower()

        price_description = self.driver.find_element_by_xpath(
            "//span[@class='price']").text
        
        if is_rent:
            price_for_sale = "NaN"
            price_for_sqft = "NaN"
            propert_type, addres = property_details.split(" to rent in ")
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
            propert_type, addres = property_details.split(" for sale in ")
            if price_description == "POA":
                price_for_sale = "NaN"
                price_for_sqft = "NaN"
            else:
                price_sale = int(price_description.split()[0].translate(
                    {ord(i): '' for i in '£,'}))
                price_per_sqft = int(price_description.split()[1].translate(
                    {ord(i): '' for i in '(£,/sq.'}))

        latitude, longitude, gmaps_link = self.get_maps()

        all_details = [property_details] + [
            property_description] + property_features + property_info
        
        complete_description = " | "
        for detail in all_details:
            complete_description += detail + " | "

        is_furnish, is_shared, is_stud = self.get_furnished_shared_student(complete_description)
        
        # Close tab
        self.driver.find_element_by_tag_name('body').send_keys(Keys.CONTROL + 'w')

        # Close browser
        self.driver.close()

        scraped_property = Property(
            country='GB',
            city= addres.split(", ")[-1].split()[0], # Not always get the city
            address=addres,
            post_code=addres.split(", ")[-1].split()[1],
            long_lat=str(longitude)+", "+str(latitude),

            area_m_2=0.092903*area_sqft,
            number_of_bedrooms=bedrooms,
            number_of_bathrooms=bathrooms,

            is_rental=is_rent,
            is_shared_accomodation=is_shared,
            is_student=is_stud,
            is_furnished=is_furnish,

            price_for_sale = price_sale,
            price_per_month_gbp=price_per_month,
            property_type=propert_type,
            
            url= url,
            description=complete_description,
            agency = agent,
            agency_phone_number = agent_phone_number,
            google_maps = gmaps_link
            pictures= self.find_pictures()
        )

        # Save to database
        self.save_property(scraped_property)