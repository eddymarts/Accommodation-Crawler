# property_scraper
Property Scraper

## Running the project
For now just run it as:
```bash
$ python main.py
```
Needs sqlite3 & sqlalchemy


## Setting up venv
```bash
$ virtualenv env
$ source env/bin/activate
$ pip3 install -r requirements.txt
```
## ToDo:
- add a requirements.txt file (need to setup a venv for this project)

- Write scraper (url_finder) to find URLs that we want to scrape and add them to a queue in the DB ✅
    - Do a search and add all of the results to the URLs table ✅


- Write scraper (url_scraper) for individual zoopla properties 


- Setup url_scraper to read from the queue and scrape that property
- Parallelise the url_scraper call so that multiple pages can be scraped at once
- Store results in DB

- Shift to using postgresDB on AWS

- Scrape other website beyond Zoopla. 
    - Find website to scrape
    - Extend url_finder to also find properties from new-website and add them to the URL queue
    - Extend url_scraper to have a ZooplaScraper and a "NewWebsiteScraper" 
    - write NewWebsiteScraper to scrape the new site for properties

- url_scraper should pick records from the queue and scrape them with the right scraper either zoopla or NewWebsiteScraper

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