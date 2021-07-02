import sys
from url_finders.zoopla_url_finder import ZooplaUrlFinder, ZooplaRentUrlFinder
from url_finders.prime_location_url_finder import PrimeLocationUrlFinder

from url_scrapers.zoopla_scraper import ZooplaRentScraper, ZooplaScraper
from url_scrapers.prime_location_scraper import PrimeLocationScraper


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
        zoopla_url_finder = ZooplaRentUrlFinder(db_session)
        zoopla_url_finder.find()
    except Exception as error:
        print(f"Got error:{error}")
        print(f"Failed to scrape all ZooplaRentUrls")

    try:
        zoopla_url_finder = ZooplaUrlFinder(db_session)
        zoopla_url_finder.find()
    except Exception as error:
        print(f"Got error:{error}")
        print(f"Failed to scrape all ZooplaBuyUrls")

    try:
        prime_location_finder = PrimeLocationUrlFinder(db_session)
        prime_location_finder.find()
    except Exception as error:
        print(f"Got error:{error}")
        print(f"Failed to scrape all PrimeLocationUrls")


def scrape_urls():
    db_factory = setup_pooled_db_for_multitasking()
    number_to_scrape = 10000
    while True:
        try:
            zoopla_rent_scraper = ZooplaRentScraper(db_factory)
            zoopla_rent_scraper.scrape(number_to_scrape)
        except Exception as error:
            print(f"Got error:{error}")
            print(f"Failed to scrape ZooplaRent URLs")

        try:
            zoopla_scraper = ZooplaScraper(db_factory)
            zoopla_scraper.scrape(number_to_scrape)
        except Exception as error:
            print(f"Got error:{error}")
            print(f"Failed to scrape ZooplaBuy URLs")

        try:
            prime_location_scraper = PrimeLocationScraper(db_factory)
            prime_location_scraper.scrape(number_to_scrape)
        except Exception as error:
            print(f"Got error:{error}")
            print(f"Failed to scrape PrimeLocation URLs")

        # scrape 1000 at a time with a wait in between in-case the queue is empty.
        time.sleep(5)
        print(
            f"\n\nWaiting for 5 seconds before scraping next {number_to_scrape} urls.\n\n"
        )


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
