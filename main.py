from url_finder import UrlFinder
from url_scraper import UrlScraper

from models import DB_factory


# https://docs.sqlalchemy.org/en/14/orm/tutorial.html
def setup_db():
    db = DB_factory()
    return db.get_session();


def main():
    db_session = setup_db()

    url_finder = UrlFinder(db_session)
    url_finder.find(100) 

    url_scraper = UrlScraper(db_session)
    url_scraper.scrape(100)


main()