# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 20:11:42 2019

@author: chaeg
"""

# -*- coding: utf-8 -*-
"""
Created on Tue Jul  9 20:41:59 2019

@author: chaeg

Aim to rank all properties and select the highest rated postcodes for further investigation
"""

#NB: Keep your API KEY TO HAND! (can get from google)
#This code requires you to input your work locations and will take ca. 20 mins 
#to run (to avoid scraping too aggressively)
#Enter your work address in the following format: 3 Primrose Mews,NW1 8YW

#ONCE run once can always just run for top page and drop duplicates to get new
#additions

import requests 
from bs4 import BeautifulSoup as BS
import numpy as np
import pandas as pd
import time
import re

#please replace headers if you would like
headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
    }
#Your API_KEY is availible from google just google how do I get an API key and 
#be sure to enable the Directions API

API_KEY = str(input("What is your API KEY?"))

url = 'https://www.zoopla.co.uk/to-rent/property/london/?beds_min=4&furnished_state=furnished&price_frequency=per_month&price_max=3250&price_min=2500&q=London&results_sort=newest_listings&search_source=home'
web_page = requests.get(url,headers = headers)
html_content = web_page.text
soup = BS(html_content, 'html.parser')

#this selects the locations inside dividers
class_a = soup.find_all("a",{"class":"listing-results-address"})
class_b = soup.find_all("a",{"class":"listing-results-price text-price"})
class_c = soup.find_all("span",{"class":"num-icon num-baths"})


location = []
for i in range(len(class_a)):
    location.append(class_a[i].get_text().replace(" ","+"))

p = re.compile("\d\,\d+")

price = [] 
for i in range(len(class_b)):
    price.append(float(p.findall(class_b[i].get_text())[0].replace(",","")))


url_list = []
for a in soup.find_all('a',{"class":"listing-results-price text-price"} ,href=True):
    actual_url = "https://www.zoopla.co.uk" + str(a['href'])
    url_list.append(actual_url)
"""    
print("when writing addresses please format like: 3 Primrose Mews,NW1 8YW")
Ellie_add = str(input("what is the first work address?: ")).replace(" ","+")
Kate_add = str(input("what is the second work address?: ")).replace(" ","+")
Celia_add = str(input("what is the third work address?: ")).replace(" ","+")
Catriona_add = str(input("what is the fourth address?: ")).replace(" ","+")
Chae_add = str(input("what is the sixth work address?: ")).replace(" ","+")
"""


Ellie_add = "Cockspur+Street,London,SW1"
Kate_add = "69+chepstow+road,W2+5QR"
Celia_add = "3+Primrose+Mews,NW1+8YW"
Catriona_add = "Northampton+Square,Clerkenwell,London,EC1V+0HB"
Chae_add ="1+Fore+St+Ave,London+EC2Y+5EJ"


url_loop = "https://www.zoopla.co.uk/to-rent/property/london/?beds_min=4&price_max=3250&identifier=london&furnished_state=furnished&price_min=2500&q=London&search_source=home&radius=0&price_frequency=per_month&pn="

#want it to have range for itself
#CURRENTLY adjust range from checking Zoopla to see how many pages there are
#don't think it matters if range> actual number of pages
#therefore leave as 34 as wouldn't want more than that anyway

for page in range(2,34):
    url_get = url_loop + str(page)
    web_page_loop = requests.get(url_get,headers = headers)
    soup_loop = BS(web_page_loop.text,'html.parser')
    time.sleep(2*np.random.rand())
    print("page " + str(page) +" done")
    for a in soup_loop.find_all('a',{"class":"listing-results-price text-price"},href=True):
        actual_url = "https://www.zoopla.co.uk" + str(a['href'])
        url_list.append(actual_url)
        
    class_a_loop = soup_loop.find_all("a",{"class":"listing-results-address"})
    for i in range(len(class_a_loop)):
        location.append(class_a_loop[i].get_text().replace(" ","+"))
    class_b_loop = soup_loop.find_all("a",{"class":"listing-results-price text-price"})
    for i in range(len(class_b_loop)):
        price.append(float(p.findall(class_b_loop[i].get_text())[0].replace(",","")))
    

def Celia_Commute(location):
    url_dir = "https://maps.googleapis.com/maps/api/directions/json?origin=" + str(location) + "&destination=" + str(Celia_add) + "&mode=transit&departure_time=1565078400&key="+API_KEY
    json_dir = requests.get(url_dir,headers = headers)
    dir_dict = json_dir.json()
    #print(dir_dict["status"])
    routes = dir_dict["routes"]
    routes_dict  = routes[0]
    legs = routes_dict["legs"]
    legs_dict = legs[0]
    duration = legs_dict["duration"]
    travel_time = duration["value"] #in seconds
    status = dir_dict["status"]
    return travel_time, status

def Catriona_Commute(location):
    url_dir = "https://maps.googleapis.com/maps/api/directions/json?origin=" + str(location) + "&destination=" + str(Catriona_add) + "&mode=transit&departure_time=1565078400&key="+API_KEY
    json_dir = requests.get(url_dir,headers = headers)
    dir_dict = json_dir.json()
    routes = dir_dict["routes"]
    routes_dict  = routes[0]
    legs = routes_dict["legs"]
    legs_dict = legs[0]
    duration = legs_dict["duration"]
    travel_time = duration["value"] #in seconds
    status = dir_dict["status"]
    return travel_time, status


def Ellie_Commute(location):
    url_dir = "https://maps.googleapis.com/maps/api/directions/json?origin=" + str(location) + "&destination=" + str(Ellie_add) + "&mode=transit&departure_time=1565078400&key="+API_KEY
    json_dir = requests.get(url_dir,headers = headers)
    dir_dict = json_dir.json()
    routes = dir_dict["routes"]
    routes_dict  = routes[0]
    legs = routes_dict["legs"]
    legs_dict = legs[0]
    duration = legs_dict["duration"]
    travel_time = duration["value"] #in seconds
    status = dir_dict["status"]
    return travel_time, status

def Kate_Commute(location):
    url_dir = "https://maps.googleapis.com/maps/api/directions/json?origin=" + str(location) + "&destination=" + str(Kate_add) + "&mode=transit&departure_time=1565078400&key="+API_KEY
    json_dir = requests.get(url_dir,headers = headers)
    dir_dict = json_dir.json()
    routes = dir_dict["routes"]
    routes_dict  = routes[0]
    legs = routes_dict["legs"]
    legs_dict = legs[0]
    duration = legs_dict["duration"]
    travel_time = duration["value"] #in seconds
    status = dir_dict["status"]
    return travel_time, status

def Chae_Commute(location):
    url_dir = "https://maps.googleapis.com/maps/api/directions/json?origin=" + str(location) + "&destination=" + str(Chae_add) + "&mode=transit&departure_time=1565078400&key="+API_KEY
    json_dir = requests.get(url_dir,headers = headers)
    dir_dict = json_dir.json()
    routes = dir_dict["routes"]
    routes_dict  = routes[0]
    legs = routes_dict["legs"]
    legs_dict = legs[0]
    duration = legs_dict["duration"]
    travel_time = duration["value"] #in seconds
    status = dir_dict["status"]
    return travel_time, status




celia_time = []
ellie_time = []
kate_time = []
catriona_time = []
chae_time = []
commute_time = []
std_dev=[]


for i in location:
        time.sleep(0.1)
        celia_time.append(Celia_Commute(i)[0])
        time.sleep(0.1)
        ellie_time.append(Ellie_Commute(i)[0])
        time.sleep(0.1)
        catriona_time.append(Catriona_Commute(i)[0])
        time.sleep(0.1)
        chae_time.append(Chae_Commute(i)[0])
        time.sleep(0.1)
        kate_time.append(Kate_Commute(i)[0])
        time.sleep(0.1)
        #A = Celia_Commute(i)[0]
        #B = Ellie_Commute(i)[0]
        #C = Catriona_Commute(i)[0]
        #E = Chae_Commute(i)[0]
        #F = Kate_Commute(i)[0]
        #commute_time.append(A+B+C+E+F)
        #std_dev.append(np.std([A,B,C,E,F]))

#vectorising some elements of above loop
        
commute_time = np.array(celia_time) + np.array(ellie_time) + np.array(kate_time) + np.array(catriona_time) + np.array(chae_time)
std_dev = np.std([celia_time,ellie_time,kate_time,catriona_time,chae_time], axis = 0)#inseconds
std_dev = np.array(std_dev)/60.0 # in minutes
        
commute_seconds = commute_time
commute_time = (np.array(commute_time,dtype=float)/60)#in minutes
kate_time = (np.array(kate_time,dtype=float)/60)#in minutes
celia_time = (np.array(celia_time,dtype=float)/60)#in minutes
chae_time = (np.array(chae_time,dtype=float)/60)#in minutes
catriona_time = (np.array(catriona_time,dtype=float)/60)#in minutes
ellie_time = (np.array(ellie_time,dtype=float)/60)#in minutes
avg_commute_time = commute_time/6
avg_commute_time = avg_commute_time.tolist()
commute_time = commute_time.tolist()


score = (np.array(commute_seconds)/max(commute_seconds)) + (np.array(price)/max(price)) + 2*(np.array(std_dev)/max(std_dev))
score = score.tolist()


d = {'location': location, 'price': price,'webpage': url_list ,'avg_commute_time': avg_commute_time,'std_dev': std_dev,'score': score,'Kate_time':kate_time,'Catriona_time':catriona_time,'Chae_time':chae_time,'Celia_time':celia_time,'Ellie_time':ellie_time}
df = pd.DataFrame(data=d)

#this isnt saved to memory
df_sort = df.sort_values('score', ascending = True)

df_sort.to_excel("4_bed_house_hunt.xlsx")


print("SCRAPING DONE")