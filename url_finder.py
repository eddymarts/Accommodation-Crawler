from models import UrlToScrape
from datetime import datetime

# How do you know what you want to scrape
# https://www.zoopla.co.uk/to-rent/property/london/?page_size=25&price_frequency=per_month&q=london&radius=0&results_sort=newest_listings&pn=2
areas_of_UK = {
    "London": "107,234",
    "South East England": "106,175",
    "East Midlands": "35,487",
    "East of England": "66,151",
    "North East England": "22,936",
    "North West England": "48,863",
    "South West England": "50,903",
    "West Midlands": "37,278",
    "Yorkshire and The Humber": "29,093",
    "Isle of Man": "1,157",
    "Channel Isles": "474",
    "Scotland": "26,008",
    "Wales": "21,682",
    "Northern Ireland": "1,035",
}

class UrlFinder():
    def __init__(self, db_session) -> None:
        self.db_session = db_session
        pass

    def current_date(self):
        # datetime object containing current date and time
        now = datetime.now()
        # dd/mm/YY H:M:S
        dt_string = now.strftime("%d/%m/%Y %H:%M:%S")
        dt_string = now.strftime("%d/%m/%Y--%H:%M:%S")
        return dt_string

    def find(self, number_to_find):
        # finds URLs and saves them to the DB.
        for i in range(number_to_find):
            new_url = UrlToScrape(
                url=f'new-URL_{self.current_date()}', 
                parser_to_use='Zoopla',
                scraped_yet=False
            )
            self.db_session.add(new_url)

        self.db_session.commit()
