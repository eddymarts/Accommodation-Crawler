# property_scraper
Property Scraper

## Running the project


The project has two parts:

1. fetching URLs that we want to scrape
To fetch URLs that we scrape later run:
```bash
$  python main.py fetch
```

2. Scraping those URLs
To scrape the URLs that have been saved for scraping run:
```bash
$  python main.py scrape
```



## Setting up venv
```bash
$ virtualenv env
$ source env/bin/activate
$ pip3 install -r requirements.txt
```
## ToDo:

- write PrimeLocationScraper to scrape PrimeLocation for properties

- Parallelise the url_scraper call so that multiple pages can be scraped at once
- Shift to using postgresDB on AWS


- Scrape images and put in s3 bucket


Extension ideas?
- Further datasets/websites to scrape and add to the dataset
- Time based data so that the same property can be scraped monthly to detect any pricing variations?
- Frontend with metrics?

- Multithread the fetcher 
- Multithread the scraper

## Helpful:
https://www.worthwebscraping.com/how-to-scrape-zoopla-uk-real-estate-property-listings-scraping-using-python/
https://github.com/Tawfiqh/BeautifulSoupNotebookTest/blob/master/ParseWikipedia%20(YouTube%20Version).py (last time i used bs4)


## Done:
- add a requirements.txt file (need to setup a venv for this project)✅

- Write scraper (url_finder) to find URLs that we want to scrape and add them to a queue in the DB ✅
    - Do a search and add all of the results to the URLs table ✅

- Store results in DB ✅

- Scrape other website beyond Zoopla.  ✅
    - Find website to scrape  ✅
    - Extend url_finder to also find properties from new-website and add them to the URL queue ✅
    - Extend url_scraper to have a ZooplaRentScraper and a "PrimeLocationScraper" ✅

- url_scraper should pick records from the queue and scrape them with the right scraper either zoopla or PrimeLocationScraper ✅

- Write scraper (url_scraper) for individual zoopla-rented properties ✅

- url-fetcher should check the DB first, to check if the URL is already in the dataset before saving it. ✅

- Write scraper (url_scraper) for individual zoopla properties ✅

- Setup url_scraper to read from the queue and scrape that property ✅
    - Mark scraped property as NULL ==> SCRAPING ==> SCRAPED + date_scraped ✅


## Helpful SQL:
```SQL
-- if you end a run in the middle of scraping, some results will still be marked as 'CURRENTLY_SCRAPING'
-- cleanup with the following:
UPDATE urls_to_scrape SET scraped_yet = 0 WHERE scraped_yet = 'CURRENTLY_SCRAPING';
select distinct scraped_yet from urls_to_scrape limit 5;

select count(distinct urls) from urls_to_scrape;
select count(distinct *) from urls_to_scrape; -- should be the same as the line above

select count(distinct urls) from urls_to_scrape;
select count(distinct *) from urls_to_scrape; -- should be the same as the line above

```

## MacOS multi-threading Issue
If multi-threading is enabled you may run into an issue on newer versions of macOS
```
[__NSCFConstantString initialize] may have been in progress in another thread when fork() was called.
```
Details and fix here: 
https://stackoverflow.com/questions/50168647/multiprocessing-causes-python-to-crash-and-gives-an-error-may-have-been-in-progr

In Bash:
OBJC_DISABLE_INITIALIZE_FORK_SAFETY=YES

In Fish:
set -x OBJC_DISABLE_INITIALIZE_FORK_SAFETY YES



