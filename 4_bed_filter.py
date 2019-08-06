# -*- coding: utf-8 -*-
"""
Created on Tue Aug  6 20:25:57 2019

@author: chaeg
"""
import pandas as pd

#importing data from the Zoopla_scrape code

df = pd.read_excel(io=r"C:\Users\chaeg\Desktop\ZOOPLA\4_bed_house_hunt.xlsx")

df = df[df.Chae_time <= 40]
df = df[df.Catriona_time <= 40]
df = df[df.Celia_time <= 40]
df = df[df.Kate_time <= 40]
df= df[df.Ellie_time <= 40]
df = df.drop_duplicates(['webpage'], keep='first')
df.to_excel('4_bed_filtered_houses.xlsx')