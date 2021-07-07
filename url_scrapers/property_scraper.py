from models import UrlToScrape
from datetime import datetime
import multiprocessing
import urllib.request
import boto3
import os


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

    proc = [
        multiprocessing.Process(target=fun, args=(f, q_in, q_out))
        for _ in range(nprocs)
    ]
    for p in proc:
        p.daemon = True
        p.start()

    sent = [q_in.put((i, x)) for i, x in enumerate(X)]
    [q_in.put((None, None)) for _ in range(nprocs)]
    res = [q_out.get() for _ in range(len(sent))]

    [p.join() for p in proc]

    return [x for i, x in sorted(res)]


class PropertyScraper:
    def __init__(self, db_factory) -> None:
        self.db_factory = db_factory


        with open("dl_creds.txt", "r") as file:
            self.bucket = file.read() # S3 bucket

    def create_bucket(self):
        """
        Create bucket.

        UPDATE: Bucket already created.
        Error handled so that new creations are ignored.
        """
        try:
            self.s3 = boto3.client("s3")
            self.s3.create_bucket(
                ACL="public-read-write",
                Bucket=self.bucket,
                CreateBucketConfiguration={"LocationConstraint": "eu-west-2"},
            )

        except Exception as error:
            if "BucketAlreadyExists" in str(error) or "BucketAlreadyOwnedByYou" in str(
                error
            ):
                pass
            else:
                raise

    def download_image(self, src: str, number_of_image: int) -> str:
        """
        Saves image of property to file to upload it to S3 afterwards.

        INPUT:
        src: string containing the url of the image.

        number_of_image: int containing an identifier to store
                        the image in your computer. The image
                        will be deleted after uploaded to S3.

        OUTPUT: path of the image in S3
        """
        image = urllib.request.urlopen(src)
        file = f"{self.property_scraper}{self.property_id}image{number_of_image}.jpg"
        with open(f"{file}", "wb") as f:
            f.write(image.read())
        return self.pictures_to_S3(file, number_of_image)

    def pictures_to_S3(self, image: str, image_number: int) -> str:
        """
        Uploads image to S3.

        INPUT:
        image: string containing file identifier in your folder.
        image_number: number of image to create path in S3.

        OUTPUT: path of the image in S3
        """

        # Bucket already created
        # self.create_bucket()
        path = f"images/{self.property_scraper}/{self.property_id}/image{image_number}.jpg"
        try:
            self.s3r = boto3.resource("s3")
            self.s3r.meta.client.upload_file(image, self.bucket, path)
            os.remove(image)
        except Exception as e:
            print(f"Error while uploading picture to AWS S3:\n Error: {e}")
            path = "No picture uploaded."
        return path

    def get_urls_from_db(self, number_to_scrape):
        db_session = self.db_factory.get_fresh_session_for_multiprocessing()

        query = (
            db_session.query(UrlToScrape)
            .filter_by(parser_to_use=self.property_scraper)
            .filter_by(scraped_yet='false')  # default value is false
        )

        urls = query[:number_to_scrape]  # Limit it to just the ones to scrape
        db_session.close()
        return urls

    def current_date(self):
        # datetime object containing current date and time
        return datetime.now()

    def save_property(self, property_object):
        property_object.updated_date = self.current_date()

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
                _mark_url_obj_status(url_obj, "CURRENTLY_SCRAPING")

            def mark_as_finished_scraping(url_obj):
                _mark_url_obj_status(url_obj, "FINISHED")

            def mark_as_failed_scraping(url_obj):
                _mark_url_obj_status(url_obj, "FAILED")

            url = url_obj.url

            # Modify property_id in each scraper subclass to generate
            # a unique identifier for each property.
            # This will be used in the bucket path.
            self.property_id = url
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
        multithreaded_scraper = True
        # Change this to False if multithreading is causing issues such as concurrency locks
        # multithreaded_scraper = False; # Change this to False if multithreading is causing issues such as concurrency locks

        if multithreaded_scraper:
            sub_processes = (
                multiprocessing.cpu_count() - 1
            )  # -1 so it doesn't freeze the whole computer.
            parmap(
                lambda url: _scrape_url_obj_individual(self, url),
                urls_to_scrape,
                nprocs=sub_processes,
            )

        else:
            for url_obj in urls_to_scrape:
                _scrape_url_obj_individual(self, url_obj)
