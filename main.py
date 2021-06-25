import sys
from url_finders.zoopla_url_finder import ZooplaUrlFinder
from url_finders.prime_location_url_finder import PrimeLocationUrlFinder

from url_scrapers.zoopla_scraper import ZooplaRentScraper
from url_scrapers.zoopla_scraper import ZooplaScraper
from url_scrapers.prime_location_scraper import PrimeLocationScraper


from models import DB_factory
import time


# https://docs.sqlalchemy.org/en/14/orm/tutorial.html
def setup_db():
    db = DB_factory()
    return db.get_session();


def fetch_urls():
    db_session = setup_db()

    zoopla_url_finder = ZooplaUrlFinder(db_session)
    zoopla_url_finder.find()

    prime_location_finder = PrimeLocationUrlFinder(db_session)
    prime_location_finder.find()



def scrape_urls():
    db_session = setup_db()
    number_to_scrape = 1000
    while True:

        zoopla_rent_scraper = ZooplaRentScraper(db_session)
        zoopla_rent_scraper.scrape(number_to_scrape)

        zoopla_scraper = ZooplaScraper(db_session)
        zoopla_scraper.scrape(number_to_scrape)

        prime_location_scraper = PrimeLocationScraper(db_session)
        prime_location_scraper.scrape(number_to_scrape)
        
        # scrape 1000 at a time with a wait in between in-case the queue is empty.
        time.sleep(5)
        print(f"Waiting for 5 seconds before scraping next {number_to_scrape} urls.")

VALID_ARGUMENTS = ['scrape', 'fetch']

def get_argument():
    argument = 'fetch_URLs'
    argument = 'scrape'

    args = [arg for arg in sys.argv[1:]]
    if len(args):
        argument = args[0]
    
    # print(f"Argument is {argument}")
    if argument not in VALID_ARGUMENTS:
        raise Exception("Invalid argument specified")

    return argument


argument = get_argument()

if argument == 'scrape':
    scrape_urls();

elif argument == 'fetch':
    fetch_urls()

