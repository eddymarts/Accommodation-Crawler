from models import UrlToScrape

class UrlFinder():
    def __init__(self, db_session) -> None:
        self.db_session = db_session
        if not self.parser_to_use:
            raise Exception("No website specified. e.g: Zoopla, Prime Location. Please specify the website that this is scrapingo use when instantiating th")
        pass

    def url_already_exists(self, new_url):
        # print(f"Checking IF {new_url} already exists")
        query = self.db_session.query(UrlToScrape).filter_by(
            url=new_url
        ).exists()
        exists = self.db_session.query(query).scalar()
        # print(f"{new_url} exists = {exists}")
        return exists;


    # Return-value: whether or not a new DB object was created
    def create_db_object_from_url(self, new_url):
        if self.url_already_exists(new_url):
            return False

        new_url_obj = UrlToScrape(
            url=new_url,
            parser_to_use=self.parser_to_use,
            scraped_yet=False
        )

        self.db_session.add(new_url_obj)
        self.db_session.commit()
        return True
        

    def save_urls_to_db(self, urls_to_save):
        new_urls_added = 0
        for url in urls_to_save:
            new_obj_created = self.create_db_object_from_url(url)
            if new_obj_created:
                new_urls_added += 1
        print(f"Saved {new_urls_added} new URL(s) for {self.parser_to_use}")

    def find(self):
        raise NotImplementedError