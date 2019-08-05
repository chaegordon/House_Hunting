# -*- coding: utf-8 -*-
"""
Created on Thu Jul 25 02:11:26 2019

@author: chaeg
"""
#improve by looping over li, add a check for response 200, add exponential back-off, proxies
#eg TOR requests, workarounds for rendering


import requests 
from bs4 import BeautifulSoup as BS
import numpy as np
import pandas as pd
import time
import re

headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    }

url = 'https://www.zoopla.co.uk/to-rent/property/5-bedrooms/london/?furnished_state=furnished&price_frequency=per_month&price_max=4250&price_min=2500&q=London&radius=0&results_sort=newest_listings&search_source=refine'
web_page = requests.get(url,headers = headers)
html_content = web_page.text
soup = BS(html_content, 'html.parser')

#this selects the locations inside dividers
class_a = soup.find_all("a",{"class":"listing-results-address"})
class_b = soup.find_all("a",{"class":"listing-results-price text-price"})
class_c = soup.find_all("span",{"class":"num-icon num-baths"})


#have multiple +'s when have multiple spaces maybe remove
location = []
for i in range(len(class_a)):
    location.append(class_a[i].get_text().replace(" ","+"))

p = re.compile("\d\,\d+")

price = [] 
for i in range(len(class_b)):
    price.append(float(p.findall(class_b[i].get_text())[0].replace(",","")))

#because am doing it this way the properties without bathrooms will mean lists will 
#no longer line up
#in future could loop over the li elements if want to know about bathrooms
"""bathrooms = []
for i in range(len(class_b))"""

url_list = []
for a in soup.find_all('a',{"class":"listing-results-price text-price"} ,href=True):
    actual_url = "https://www.zoopla.co.uk" + str(a['href'])
    url_list.append(actual_url)