#!/usr/bin/env python
# coding: utf-8

# In[1]:


areas_of_UK = ["London", "South East England", "East Midlands", "East of England", "North East England", "North West England", "South West England", "West Midlands", "Yorkshire and The Humber", "Isle of Man", "Channel Isles", "Scotland", "Wales", "Northern Ireland"]


# In[2]:


def scrape_URLs_for_region(region):
    url = f"https://www.zoopla.co.uk/to-rent/property/london/?page_size=25&price_frequency=per_month&q=london&radius=0&results_sort=newest_listings&pn=2#listing_58997893"
    return region

def find(number_to_find=None):
    # finds URLs and saves them to the DB.
    for region in areas_of_UK:
        scrape_URLs_for_region(region)
    


find()    


# In[ ]:





# In[3]:


from bs4 import BeautifulSoup
import requests


# In[4]:



url = f"https://www.zoopla.co.uk/to-rent/property/London/?page_size=50&price_frequency=per_month&q=London&radius=0&results_sort=newest_listings&pn=6111"
print(url)

page = requests.get(url)
soup = BeautifulSoup(page.content)

urls = [item for item in soup.find_all('a', attrs={'data-testid' : True}) if item['data-testid']=='listing-details-link']
for a in urls:
    print(a['href'])


# In[5]:



url = f"https://www.zoopla.co.uk/to-rent/details/58998958/"
print(url)

page = requests.get(url)
soup = BeautifulSoup(page.content)


# In[6]:


print(soup)


# In[11]:


# price = [item for item in soup.find_all('a', attrs={'data-testid' : True}) if item['data-testid']=='listing-details-link']
prices = [item for item in soup.find_all('span', attrs={'data-testid' : True}) if item['data-testid']=='price' and 'pcm' in item.text]

final_pcm = None
for p in prices:
    print(p.get_text())
    final_pcm = p.get_text()


# In[12]:


final_pcm[1:-4]


# In[24]:


baths = [item for item in soup.find_all('span', attrs={'data-testid' : 'baths-label'})]

for tag in baths:
    baths = tag.get_text()
    baths = baths.split(' ')[0]
    print(baths)


# In[ ]:




