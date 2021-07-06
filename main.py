import sys
from url_finders.zoopla_url_finder import ZooplaUrlFinder
from url_finders.prime_location_url_finder import PrimeLocationUrlFinder
from url_scrapers.zoopla_scraper import ZooplaScraper
from url_scrapers.prime_location_scraper import PrimeLocationScraper
from data_cleaning import PropertyCleaning
from models import DB_factory
import time

# https://docs.sqlalchemy.org/en/14/orm/tutorial.html
def setup_db():
    db = DB_factory()
    return db.get_session()

def setup_pooled_db_for_multitasking():
    db_factory = DB_factory()
    return db_factory

def fetch_urls():
    db_session = setup_db()
    try:
        zoopla_url_finder = ZooplaUrlFinder(db_session)
        zoopla_url_finder.find()
    except Exception as error:
        print(f"Got error:{error}")
        print(f"Failed to scrape all Zoopla Urls")

    try:
        prime_location_finder = PrimeLocationUrlFinder(db_session)
        prime_location_finder.find()
    except Exception as error:
        print(f"Got error:{error}")
        print(f"Failed to scrape all PrimeLocation Urls")

def scrape_urls():
    db_factory = setup_pooled_db_for_multitasking()
    number_to_scrape = 100000
    while True:
        try:
            prime_location_scraper = PrimeLocationScraper(db_factory)
            prime_location_scraper.scrape(number_to_scrape)
        except Exception as error:
            print(f"Got error:{error}")
            print(f"Failed to scrape PrimeLocation URLs")

        try:
            zoopla_scraper = ZooplaScraper(db_factory)
            zoopla_scraper.scrape(number_to_scrape)
        except Exception as error:
            print(f"Got error:{error}")
            print(f"Failed to scrape Zoopla URLs")

        # scrape 1000 at a time with a wait in between in-case the queue is empty.
        time.sleep(5)
        print(
            f"\n\nWaiting for 5 seconds before scraping next {number_to_scrape} urls.\n\n"
        )

def clean_data():
    db_factory = setup_pooled_db_for_multitasking()
    property_data = PropertyCleaning(db_factory)
    property_data.analyse()
    property_data.clean()
    property_data.analyse()

VALID_ARGUMENTS = ["scrape", "fetch", "clean"]

def get_argument():
    argument = "fetch_URLs"
    argument = "scrape"
    argument = "clean"

    args = [arg for arg in sys.argv[1:]]
    if len(args):
        argument = args[0]

    # print(f"Argument is {argument}")
    if argument not in VALID_ARGUMENTS:
        raise Exception("Invalid argument specified")

    return argument


argument = get_argument()

if argument == "scrape":
    scrape_urls()
elif argument == "fetch":
    fetch_urls()
elif argument == "clean":
    clean_data()
