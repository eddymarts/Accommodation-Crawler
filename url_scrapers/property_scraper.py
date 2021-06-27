from models import Property, UrlToScrape
from datetime import datetime
import multiprocessing
from functools import partial

def fun(f, q_in, q_out):
    while True:
        i, x = q_in.get()
        if i is None:
            break
        q_out.put((i, f(x)))

# https://stackoverflow.com/questions/3288595/multiprocessing-how-to-use-pool-map-on-a-function-defined-in-a-class
def parmap(f, X, nprocs=multiprocessing.cpu_count()):
    q_in = multiprocessing.Queue(1)
    q_out = multiprocessing.Queue()

    proc = [multiprocessing.Process(target=fun, args=(f, q_in, q_out))
            for _ in range(nprocs)]
    for p in proc:
        p.daemon = True
        p.start()

    sent = [q_in.put((i, x)) for i, x in enumerate(X)]
    [q_in.put((None, None)) for _ in range(nprocs)]
    res = [q_out.get() for _ in range(len(sent))]

    [p.join() for p in proc]

    return [x for i, x in sorted(res)]


class PropertyScraper():
    def __init__(self, db_factory) -> None:
        self.db_factory = db_factory
        pass


    def get_urls_from_db(self, number_to_scrape):
        db_session =self.db_factory.get_fresh_session_for_multiprocessing()
        
        query = db_session.query(UrlToScrape).filter_by(
            parser_to_use=self.property_scraper
        ).filter_by(
            scraped_yet=False #default value is false
        )

        urls = query[:number_to_scrape] # Limit it to just the ones to scrape
        db_session.close()
        return urls

    def current_date(self):
        # datetime object containing current date and time
        now = datetime.now()
        return now;

    def save_property(self, property_object):
        property_object.updated_date=self.current_date();

        db_session = self.db_factory.get_fresh_session_for_multiprocessing()

        db_session.add(property_object)
        db_session.commit()
        db_session.close()

    def scrape(self, number_to_scrape):
        urls_to_scrape = self.get_urls_from_db(number_to_scrape)
        print(f"{self.property_scraper} -- Need to scrape {len(urls_to_scrape)} URLs")
        print(urls_to_scrape)
        
        # Define it in here so it isn't defined as an object on the class
        def _scrape_url_obj_individual(self, url_obj):
            db_session = self.db_factory.get_fresh_session_for_multiprocessing()

            def _mark_url_obj_status(url_obj, status):
                print(f"{url_obj.url} = {status}")
                url_obj.scraped_yet = status
                db_session.add(url_obj)
                db_session.commit()

            def mark_as_currently_scraping(url_obj):
                _mark_url_obj_status(url_obj, 'CURRENTLY_SCRAPING')

            def mark_as_finished_scraping(url_obj):
                _mark_url_obj_status(url_obj, 'FINISHED')

            def mark_as_failed_scraping(url_obj):
                _mark_url_obj_status(url_obj, 'FAILED')

            url = url_obj.url
            print(f"\n{self.property_scraper} scraping url {url}")
            try:
                mark_as_currently_scraping(url_obj)
                self.scrape_url(url)
                mark_as_finished_scraping(url_obj)

            except Exception as error:
                print(f"Got error:{error}")
                print(f"Failed to scrape URL: {url}")
                mark_as_failed_scraping(url_obj)

        # Multithreading
        multithreaded_scraper = True; # Change this to False if multithreading is causing issues such as concurrency locks
        # multithreaded_scraper = False; # Change this to False if multithreading is causing issues such as concurrency locks

        if multithreaded_scraper:
            sub_processes = multiprocessing.cpu_count() - 1 # -1 so it doesn't freeze the whole computer.
            parmap(lambda i: _scrape_url_obj_individual(self,i), urls_to_scrape, nprocs=sub_processes)
            # with mp.Pool(mp.cpu_count()-1) as pool:
            #     pool.map(partial(_scrape_url_obj_individual, self=self), urls_to_scrape)
        else:
            for url_obj in urls_to_scrape:
                _scrape_url_obj_individual(self, url_obj)

