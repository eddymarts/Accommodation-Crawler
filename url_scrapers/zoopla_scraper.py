from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from models import Property_raw
from url_scrapers.property_scraper import PropertyScraper


class ZooplaScraper(PropertyScraper):
    def __init__(self, db_session) -> None:
        self.property_scraper = "Zoopla"
        super().__init__(db_session)

    def quit_popup_alert(self) -> None:
        """Removes the popup alert and cookies banner from the search browser."""
        try:
            self.driver.find_element_by_xpath(
                "//button[@aria-label='Close']"
            ).click()
        except Exception:
            pass

        
        try:
            self.driver.find_element_by_xpath(
                "//div[@class='ui-cookie-consent-choose__buttons']/\
button[@class='ui-button-secondary']").click()
        except Exception:
            pass
    
    def get_address(self) -> str:
        """ Returns address as a string. """
        try:
            address = self.driver.find_element_by_xpath(
                "//span[@data-testid='address-label']").text
        except:
            address = None
        
        return address

    def get_area_sqft(self) -> int:
        """
        Returns area as an integer in squared feet.
        """
        try:
            area_sqft = float(
                self.driver.find_element_by_xpath("//span[@data-testid='floorarea-label']")
                .text.split()[0]
                .translate({ord(","): ""})
            )
        except:
            area_sqft = None

        return area_sqft
    
    def get_details(self) -> tuple:
        """ Returns property details as a string. """
        try:
            property_details = self.driver.find_element_by_xpath(
                "//span[@data-testid='title-label']").text
        except:
            property_details = None

        try:
            property_type = property_details.rsplit(' ', 3)[0]
            if "bed" in property_type:
                property_type = property_type.split("bed ")[1]
        except:
            property_type = None          
        
        return property_details, property_type

    def get_property_features(self) -> list:
        """
        Returns property features.
        """

        try:
            property_features = [
                feature.text
                for feature in self.driver.find_elements_by_xpath(
                    "//div[@data-testid='listing_features']//li"
                )
            ]

            assert len(property_features) > 0

        except AssertionError:
            property_features = [None]

        return property_features

    def get_property_description(self) -> str:
        """
        Gets property description.
        """
        
        try:
            property_description = self.driver.find_element_by_xpath(
            "//div[@data-testid='listing_description']//span").text

        except:
            property_description = None
        
        return property_description
    
    def get_beds_baths_receps(self) -> tuple:
        """
        Returns number of bedrooms, number of bathrooms and number of receptions.
        """
        try:
            bedrooms = int(
                self.driver.find_element_by_xpath(
                    "//span[@data-testid='beds-label']"
                ).text.split()[0]
            )
        except:
            bedrooms = None

        try:
            bathrooms = int(
                self.driver.find_element_by_xpath(
                    "//span[@data-testid='baths-label']"
                ).text.split()[0]
            )
        except:
            bathrooms = None

        try:
            receptions = int(
                self.driver.find_element_by_xpath(
                    "//span[@data-testid='receptions-label']"
                ).text.split()[0]
            )
        except:
            receptions = None

        return bedrooms, bathrooms, receptions

    def get_maps(self) -> tuple:
        """
        Searches for the Google Maps link of the property.

        INPUT: None
        OUTPUT:
            latitude: float
            longitude: float
            Google Maps link: string
        """
        try:
            gmaps_link = self.driver.find_element_by_xpath(
                "//img[@data-testid='static-google-map']").get_attribute("src")

            latitude, longitude = [
                float(coord)
                for coord in gmaps_link.split("png%7C")[1].split("&")[0].split(",")
            ]
        except:
            latitude, longitude, gmaps_link = None, None, None

        return latitude, longitude, gmaps_link

    def get_agent(self) -> tuple:
        """
        Returns agency name and phone number.
        """
        try:
            agent = self.driver.find_element_by_xpath(
                "//div[@data-testid='agent-details']//h3").text.split(
                    "\nView agent properties")[0]
        except:
            agent = None

        try:
            agent_phone_number = self.driver.find_element_by_xpath(
                "//a[@data-testid='agent-phone-cta-link']"
            ).text.translate({ord(" "): ""})
        except:
            agent_phone_number = None

        return agent, agent_phone_number

    def find_pictures(self):
        try:
            images = self.driver.find_elements_by_xpath(
                "//li[@data-testid='gallery-image']")
            
            path = ""
            for index, image in enumerate(images):
                src = image.find_element_by_xpath("//img").get_attribute("src")

                # download the image
                path = path + self.download_image(src, index) + ", "
            path = path.rstrip(", ")
        except:
            path = "No pictures uploaded."
    
        return path

    def scrape_url(self, url):
        # Open browser
        options = Options()
        options.headless = True
        self.driver = webdriver.Chrome(options=options)

        # Unique identifier used for identifying buckets
        self.property_id = url.split("details/")[1].split("/")[0]

        # Open new tab
        self.driver.find_element_by_tag_name("body").send_keys(Keys.CONTROL + "t")
        self.driver.get(url)
        self.quit_popup_alert()

        address = self.get_address()
        agent, agent_phone_number = self.get_agent()
        bedrooms, bathrooms, receptions = self.get_beds_baths_receps()
        area_sqft = self.get_area_sqft()
        property_features = self.get_property_features()
        property_description = self.get_property_description()
        property_details, property_type = self.get_details()
        price_description = self.driver.find_element_by_xpath(
            "//span[@data-testid='price']").text
        is_rent = "to rent" in property_details.lower() or "to-rent" in url

        if is_rent:
            price_sale = None
            if "POA" in price_description.upper():
                price_per_month = None
            else:
                if len(price_description.split()) > 1:
                    price_per_month = int(
                        price_description.split()[0].translate(
                            {ord(i): "" for i in "£,"}
                        )
                    )
                else:
                    price_per_month = int(
                        price_description.translate({ord(i): "" for i in "£,"})
                    )
        else:
            price_per_month = None
            if "POA" in price_description.upper():
                price_sale = None
            else:
                if len(price_description.split()) > 1:
                    price_sale = int(
                        price_description.split()[0].translate(
                            {ord(i): "" for i in "£,"}
                        )
                    )
                else:
                    price_sale = int(
                        price_description.translate({ord(i): "" for i in "£,"})
                    )

        picture = self.find_pictures()
        la, lo, gmaps_link = self.get_maps()

        all_details = (
            [property_details]
            + [property_description]
            + property_features
        )

        complete_description = " | "
        for detail in all_details:
            complete_description += str(detail) + " | "

        # Close tab
        self.driver.find_element_by_tag_name("body").send_keys(Keys.CONTROL + "w")

        # Close browser
        self.driver.close()

        scraped_property = Property_raw(
            address=address,
            longitude=lo,
            latitude=la,
            area_sqft=area_sqft,
            number_of_bedrooms=bedrooms,
            number_of_bathrooms=bathrooms,
            number_of_receptions=receptions,
            is_rental=is_rent,
            price_for_sale=price_sale,
            price_per_month_gbp=price_per_month,
            property_type=property_type,
            url=url,
            description=complete_description,
            agency=agent,
            agency_phone_number=agent_phone_number,
            google_maps=gmaps_link,
            pictures=picture,
            is_clean=False
        )
        
        # Save to database
        self.save_property(scraped_property)