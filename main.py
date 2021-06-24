import sys
from url_finder import UrlFinder
from url_scraper import UrlScraper

from models import DB_factory


# https://docs.sqlalchemy.org/en/14/orm/tutorial.html
def setup_db():
    db = DB_factory()
    return db.get_session();


def fetch_urls():
    db_session = setup_db()

    url_finder = UrlFinder(db_session)
    url_finder.find() 


def scrape_urls():
    db_session = setup_db()

    url_scraper = UrlScraper(db_session)
    url_scraper.scrape(100)

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

