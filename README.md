# property_scraper
Property Scraper

ToDo:
- Write scraper (url_finder) to find URLs that we want to scrape and add them to a queue in the DB
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

Extension ideas?
- Further datasets/websites to scrape and add to the dataset
- Time based data so that the same property can be scraped monthly to detect any pricing variations?
- Frontend with metrics?
