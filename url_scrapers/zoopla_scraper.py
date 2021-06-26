from models import Property
from url_scrapers.property_scraper import PropertyScraper
from bs4 import BeautifulSoup
import requests

class ZooplaScraper(PropertyScraper):
    def __init__(self, db_factory) -> None:
        super().__init__(db_factory)
        self.property_scraper= 'Zoopla' 


    def fetch_url(self, url):
        page = requests.get(url)
        soup = BeautifulSoup(page.content, "html.parser")
        # print(soup.prettify()[:500])
        return soup

    def find_country(self, web_page):
        return 'GB'

    def find_city(self, soup):
        return None
        # The following isn't always displaying the city
        tags = [item for item in soup.find_all('span', attrs={'data-testid' : 'address-label'})]

        for tag in tags:
            data = tag.get_text()
            data = data.split(',')[-1].strip()
            data = data.split(' ')[0]
            return data

        return None


    def find_address(self, soup):
        try:
            tags = [item for item in soup.find_all('span', attrs={'data-testid' : 'address-label'})]

            for tag in tags:
                data = tag.get_text()
                return data
        except:
            return None

    def find_post_code(self, soup):
        try:
            tags = [item for item in soup.find_all('span', attrs={'data-testid' : 'address-label'})]

            for tag in tags:
                data = tag.get_text()
                data = data.split(',')[-1].strip()
                data = data.split(' ')[-1]
                return data
        except:
            return None

    def find_long_lat(self, web_page):
        return None
        tags = [item for item in soup.find_all('img', attrs={'data-testid' : 'static-google-map'})]

        for tag in tags:
            data = tag['src']
            # From the source can extract the centre == Long/lat -- but the googlemap isn't loading


    def find_area_m_2(self, web_page):
        return None #Not on Zoopla


    def find_is_rental(self, web_page):
        return False

    def find_is_shared_accomodation(self, web_page):
        return False

    def find_is_student(self, web_page):
        return False

    def find_is_furnished(self, web_page):
        # https://www.zoopla.co.uk/to-rent/details/54368982/ -- This is furnished -- but would have to parse the description text
        return None

    def find_price_per_month_gbp(self, soup):
        try:
            prices = [item for item in soup.find_all('span', attrs={'data-testid' : 'price'}) if 'pcm' in item.text]

            for p in prices:
                final_pcm = p.get_text()
                final_pcm = final_pcm[1:-4]
                final_pcm = final_pcm.replace(",", "")
                return float(final_pcm)
        except:
            return None

    def find_number_of_bathrooms(self, soup):
        try:
            baths = [item for item in soup.find_all('span', attrs={'data-testid' : 'baths-label'})]

            for tag in baths:
                baths = tag.get_text()
                baths = baths.split(' ')[0]
                return baths
        except:
            return None

    def find_number_of_bedrooms(self, soup):
        try:
            beds = [item for item in soup.find_all('span', attrs={'data-testid' : 'beds-label'})]

            for p in beds:
                beds = p.get_text()
                beds = beds.split(' ')[0]
                return beds
        except:
            return None

    def find_property_type(self, web_page):
        return None

    def find_description(self, soup):
        try:
            tags = [item for item in soup.find_all('section', attrs={'data-testid' : 'page_features_section'})]

            for tag in tags:
                data = tag.get_text(separator="\n")
                return data
        except:
            return None

    def find_pictures(self, web_page):
        return None


    def scrape_url(self, url):
        web_page = self.fetch_url(url)
        scraped_property = Property(
            country= self.find_country(web_page),
            city= self.find_city(web_page),
            address= self.find_address(web_page),
            post_code= self.find_post_code(web_page),
            long_lat= self.find_long_lat(web_page),

            area_m_2= self.find_area_m_2(web_page),
            number_of_bedrooms= self.find_number_of_bedrooms(web_page),
            number_of_bathrooms = self.find_number_of_bathrooms(web_page),

            is_rental= self.find_is_rental(web_page),
            is_shared_accomodation= self.find_is_shared_accomodation(web_page),
            is_student= self.find_is_student(web_page),
            is_furnished= self.find_is_furnished(web_page),

            price_per_month_gbp= self.find_price_per_month_gbp(web_page),
            property_type= self.find_property_type(web_page),
            
            url= url,
            description= self.find_description(web_page),
            pictures= self.find_pictures(web_page),

        )

        self.save_property(scraped_property)



class ZooplaRentScraper(ZooplaScraper):
    def __init__(self, db_factory) -> None:
        super().__init__(db_factory)
        self.property_scraper='ZooplaRent'
    
    def find_is_rental(self, web_page):
        return True

    def find_is_shared_accomodation(self, web_page):
        return None

    def find_is_student(self, web_page):
        return None

    def find_is_furnished(self, web_page):
        # https://www.zoopla.co.uk/to-rent/details/54368982/ -- This is furnished -- but would have to parse the description text
        return None
