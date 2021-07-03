from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from models import Property_raw
from url_scrapers.property_scraper import PropertyScraper


class PrimeLocationScraper(PropertyScraper):
    def __init__(self, db_session) -> None:
        self.property_scraper = "PrimeLocation"
        super().__init__(db_session)

    def quit_popup_alert(self) -> None:
        """Removes the popup alert from the search browser."""
        try:
            self.driver.find_element_by_xpath(
                "//div[@class='alerts-popup-wrapper']//a[@href='#']"
            ).click()
        except Exception:
            pass

    def get_area_sqft(self) -> int:
        """
        Returns area as an integer in squared feet.
        """
        try:
            area_sqft = float(
                self.driver.find_element_by_xpath("//span[@class='num-icon num-sqft ']")
                .text.split()[0]
                .translate({ord(","): ""})
            )
        except:
            area_sqft = None

        return area_sqft

    def get_property_features(self) -> list:
        """
        Returns property features.
        """

        try:
            property_features = [
                feature.text
                for feature in self.driver.find_elements_by_xpath(
                    "//div[@id='tab-details']/div[@class='clearfix']//li"
                )
            ]

            assert len(property_features) > 0

        except AssertionError:
            property_features = [None]

        return property_features

    def get_property_info(self) -> list:
        """
        Gets all property info.
        """

        try:
            property_info = [
                info.text
                for info in self.driver.find_elements_by_xpath(
                    "//div[@id='tab-details']/ul/li"
                )
            ]

            assert len(property_info) > 0

        except AssertionError:
            property_info = [None]

        return property_info

    def get_property_description(self) -> str:
        """
        Gets property description.
        """
        
        try:
            property_description = self.driver.find_element_by_xpath(
            "//div[@class='bottom-plus-half']/div[@class='top']").text

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
                    "//span[@class='num-icon num-beds']"
                ).text.split()[0]
            )
        except:
            bedrooms = None

        try:
            bathrooms = int(
                self.driver.find_element_by_xpath(
                    "//span[@class='num-icon num-baths']"
                ).text.split()[0]
            )
        except:
            bathrooms = None

        try:
            receptions = int(
                self.driver.find_element_by_xpath(
                    "//span[@class='num-icon num-reception']"
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
            self.quit_popup_alert()
            self.driver.find_element_by_xpath("//li[@aria-controls='tab-map']").click()
            self.wait = WebDriverWait(self.driver, 10)
            gmaps_link = self.wait.until(
                EC.visibility_of_element_located(
                    (
                        By.XPATH,
                        "//div[@class='gm-style']//a[@title=\
    'Open this area in Google Maps (opens a new window)']",
                    )
                )
            ).get_attribute("href")
            latitude, longitude = [
                float(coord)
                for coord in gmaps_link.split("ll=")[1].split("&")[0].split(",")
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
                "//div[@id='listings-agent']//p//a"
            ).text
        except:
            agent = None

        try:
            agent_phone_number = self.driver.find_element_by_xpath(
                "//span[@class='agent_phone']/a"
            ).text.translate({ord(" "): ""})
        except:
            agent_phone_number = None

        return agent, agent_phone_number

    def find_pictures(self):
        num_pictures = int(
            self.driver.find_element_by_xpath("//div[@id='images-tally']")
            .text.rstrip()
            .split()[-1]
        )

        path = ""
        while True:
            downloaded_image = int(
                self.driver.find_element_by_xpath("//span[@id='images-num']").text
            )

            src = self.driver.find_element_by_xpath(
                "//div[@id='images-main']//img"
            ).get_attribute("src")

            # download the image
            path = path + self.download_image(src, downloaded_image) + ", "
            
            if downloaded_image >= num_pictures:
                break

            self.quit_popup_alert()
            self.driver.find_element_by_xpath("//a[@id='images-nav-next']").click()
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

        agent, agent_phone_number = self.get_agent()
        bedrooms, bathrooms, receptions = self.get_beds_baths_receps()
        area_sqft = self.get_area_sqft()
        property_features = self.get_property_features()
        property_info = self.get_property_info()
        property_description = self.get_property_description()
        
        property_details = self.driver.find_element_by_xpath(
            "//h1[@class='listing-details-h1']"
        ).text

        is_rent = "to rent" in property_details.lower()

        price_description = self.driver.find_element_by_xpath(
            "//span[@class='price']"
        ).text

        if is_rent:
            price_sale = None
            propert_type, address = property_details.split(" to rent in ")
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
            propert_type, address = property_details.split(" for sale in ")
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
            + property_info
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
            property_type=propert_type,
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