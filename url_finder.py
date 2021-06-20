from models import UrlToScrape
from datetime import datetime

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
