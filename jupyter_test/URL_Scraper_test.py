#!/usr/bin/env python
# coding: utf-8

# In[7]:


areas_of_UK = ["London", "South East England", "East Midlands", "East of England", "North East England", "North West England", "South West England", "West Midlands", "Yorkshire and The Humber", "Isle of Man", "Channel Isles", "Scotland", "Wales", "Northern Ireland"]


# In[13]:


def scrape_URLs_for_region(region):
    url = f"https://www.zoopla.co.uk/to-rent/property/london/?page_size=25&price_frequency=per_month&q=london&radius=0&results_sort=newest_listings&pn=2#listing_58997893"
    return region

def find(number_to_find=None):
    # finds URLs and saves them to the DB.
    for region in areas_of_UK:
        scrape_URLs_for_region(region)
    


find()    


# In[14]:





# In[16]:


from bs4 import BeautifulSoup
import requests


# In[28]:



url = f"https://www.zoopla.co.uk/to-rent/property/London/?page_size=50&price_frequency=per_month&q=London&radius=0&results_sort=newest_listings&pn=6111"
print(url)

page = requests.get(url)
soup = BeautifulSoup(page.content)

urls = [item for item in soup.find_all('a', attrs={'data-testid' : True}) if item['data-testid']=='listing-details-link']
for a in urls:
    print(a['href'])


# In[ ]:




