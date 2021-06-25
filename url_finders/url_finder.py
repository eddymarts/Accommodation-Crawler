from models import UrlToScrape

class UrlFinder():
    def __init__(self, db_session) -> None:
        self.db_session = db_session
        if not self.parser_to_use:
            raise Exception("No website specified. e.g: Zoopla, Prime Location. Please specify the website that this is scrapingo use when instantiating th")
        pass


    def create_db_object_from_url(self, new_url):
        new_url_obj = UrlToScrape(
            url=new_url,
            parser_to_use=self.parser_to_use,
            scraped_yet=False
        )

        self.db_session.add(new_url_obj)
        self.db_session.commit()
        

    def save_urls_to_db(self, urls_to_save):
        for url in urls_to_save:
            self.create_db_object_from_url(url)


    def find(self):
        raise NotImplementedError