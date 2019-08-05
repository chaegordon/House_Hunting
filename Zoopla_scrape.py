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

url = 'https://www.zoopla.co.uk/to-rent/property/5-bedrooms/london/?furnished_state=furnished&price_frequency=per_month&price_max=4250&price_min=2500&q=London&radius=0&results_sort=newest_listings&search_source=refine'
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
Connie_add = str(input("what is the fifth work address?: ")).replace(" ","+")
Chae_add = str(input("what is the sixth work address?: ")).replace(" ","+")
"""

#addresses for TESTING!

Ellie_add = "Cockspur+Street,London,SW1"
Kate_add = "69+chepstow+road,W2+5QR"
Celia_add = "3+Primrose+Mews,NW1+8YW"
Catriona_add = "Gray's+Inn+Place,4+Warwick+St,Holborn,London,WC1R+5DX"
Connie_add = "2+Marsham+St,Westminster,London,SW1P+4DF"
Chae_add ="1+Fore+St+Ave,London+EC2Y+5EJ"


url_loop = "https://www.zoopla.co.uk/to-rent/property/5-bedrooms/london/?beds_min=5&price_max=4250&identifier=london&furnished_state=furnished&price_min=2500&q=London&beds_max=5&search_source=refine&radius=0&price_frequency=per_month&pn="

#do on over 1 page initially during TESTING!

for page in range(2,12):
    url_get = url_loop + str(page)
    web_page_loop = requests.get(url_get,headers = headers)
    soup_loop = BS(web_page_loop.text,'html.parser')
    time.sleep(2*np.random.rand())
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
    url_dir = "https://maps.googleapis.com/maps/api/directions/json?origin=" + str(location) + "&destination=" + str(Celia_add) + "&mode=transit&key="+API_KEY
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
    url_dir = "https://maps.googleapis.com/maps/api/directions/json?origin=" + str(location) + "&destination=" + str(Catriona_add) + "&mode=transit&key="+API_KEY
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

def Connie_Commute(location):
    url_dir = "https://maps.googleapis.com/maps/api/directions/json?origin=" + str(location) + "&destination=" + str(Connie_add) + "&mode=transit&key="+API_KEY
    json_dir = requests.get(url_dir,headers = headers)
    dir_dict = json_dir.json()
    routes = dir_dict["routes"]
    routes_dict  = routes[0]
    legs = routes_dict["legs"]
    legs_dict = legs[0]
    duration = legs_dict["duration"]
    travel_time = duration["value"] #in seconds
    status = dir_dict["status"]
    #print("result: "+travel_time)
    #print("error: "+error)
    return travel_time, status

def Ellie_Commute(location):
    url_dir = "https://maps.googleapis.com/maps/api/directions/json?origin=" + str(location) + "&destination=" + str(Ellie_add) + "&mode=transit&key="+API_KEY
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
    url_dir = "https://maps.googleapis.com/maps/api/directions/json?origin=" + str(location) + "&destination=" + str(Kate_add) + "&mode=transit&key="+API_KEY
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
    url_dir = "https://maps.googleapis.com/maps/api/directions/json?origin=" + str(location) + "&destination=" + str(Chae_add) + "&mode=transit&key="+API_KEY
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
connie_time = []
chae_time = []
commute_time = []
std_dev=[]


for i in location:
        celia_time.append(Celia_Commute(i)[0])
        time.sleep(2*np.random.rand())
        ellie_time.append(Ellie_Commute(i)[0])
        time.sleep(np.random.rand())
        catriona_time.append(Catriona_Commute(i)[0])
        time.sleep(2*np.random.rand())
        connie_time.append(Connie_Commute(i)[0])
        time.sleep(np.random.rand())
        chae_time.append(Chae_Commute(i)[0])
        time.sleep(2*np.random.rand())
        kate_time.append(Kate_Commute(i)[0])
        A = Celia_Commute(i)[0]
        B = Ellie_Commute(i)[0]
        C = Catriona_Commute(i)[0]
        D = Connie_Commute(i)[0]
        E = Chae_Commute(i)[0]
        commute_time.append(A+B+C+D+E)
        std_dev.append(np.std([A,B,C,D,E]))



TEST = Celia_Commute(location[0])[0]

        
commute_seconds = commute_time
commute_time = (np.array(commute_time,dtype=float)/60)#in minutes
kate_time = (np.array(kate_time,dtype=float)/60)#in minutes
celia_time = (np.array(celia_time,dtype=float)/60)#in minutes
chae_time = (np.array(chae_time,dtype=float)/60)#in minutes
catriona_time = (np.array(catriona_time,dtype=float)/60)#in minutes
ellie_time = (np.array(ellie_time,dtype=float)/60)#in minutes
connie_time = (np.array(connie_time,dtype=float)/60)#in minutes
avg_commute_time = commute_time/6
avg_commute_time = avg_commute_time.tolist()
commute_time = commute_time.tolist()

#better practice to rescale to 30*60 and 800 for example
score = (np.array(commute_seconds)/max(commute_seconds)) + (np.array(price)/max(price)) - 2*(np.array(std_dev)/max(std_dev))
score = score.tolist()


d = {'location': location, 'price': price,'webpage': url_list ,'avg_commute_time': avg_commute_time,'std_dev': std_dev,'score': score,'Kate_time':kate_time,'Catriona_time':catriona_time,'Chae_time':chae_time,'Celia_time':celia_time,'Connie_time':connie_time,'Ellie_time':ellie_time}
df = pd.DataFrame(data=d)

#this isnt saved to memory
df_sort = df.sort_values('score', ascending = True)

df_sort.to_excel("house_hunt.xlsx")

print("SCRAPING DONE")
