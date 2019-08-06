# -*- coding: utf-8 -*-
"""
Created on Fri Aug  2 23:06:34 2019

@author: chaeg
"""

import numpy as np
import pandas as pd
import time
import re
import matplotlib.pyplot as plt

#import sci-kit learn module

from sklearn.mixture import BayesianGaussianMixture
from sklearn.datasets import make_spd_matrix
from sklearn.datasets import make_sparse_spd_matrix
from sklearn.utils import shuffle
from sklearn.datasets import make_blobs
from sklearn.metrics import silhouette_score

#importing data from the Zoopla_scrape code

df = pd.read_excel(io=r"C:\Users\chaeg\Desktop\ZOOPLA\house_hunt.xlsx")

#code to convert letters to numbers for further analysis including post codes

#No need to include all letters just those included in London postcodes

alphabet = {'N':1,'E':2,'W':3,'S':4,'C':5,'IG':6,'UB':7,'TW':8,'KT':9,'CR':10,'HA':11,'RM':12
            ,'NE':13,'NW':14,'SE':15,'SW': 16,'EC':17,'EN':18,'WC':19,'EMPTY':''}

#transforming the Postcodes into numbers to form a coordinate space
#the adding as a string in the return
# avoids two post codes as ints adding to the same ie. N6 != E5 etc.

def letter_to_number(post_code):
    if re.match('([A-Z]\d)', str(post_code)) is not None:
        slice_1= post_code[0]
        slice_2 = post_code[1]
    elif re.match('([A-Z]+\d+)', str(post_code)) is not None:   
        slice_1= post_code[0]+post_code[1]
        slice_2 = post_code[2:]
    else:
        slice_1='EMPTY'
        slice_2=post_code
    return str(alphabet[str(slice_1)]) + str(slice_2)

df['post_code'] = df['location'].str.extract('([A-Z]+\d+)', expand=True)

df['post_code'] = df['post_code'].apply(letter_to_number)
df['post_code'] = df['post_code'].str.replace('nan','0')
df['post_code'] = df['post_code'].apply(int)

df_1 = df.filter(['post_code','score'], axis=1)

df = df[df.Chae_time <= 45]
df = df[df.Catriona_time <= 45]
df = df[df.Connie_time <= 45]
df = df[df.Celia_time <= 45]
df = df[df.Kate_time <= 45]
df= df[df.Ellie_time <= 45]
df = df.drop_duplicates(subset='webpage')

df.to_excel('filtered_houses.xlsx')
#now look to cluster the data
"""
#creating the model
clf = BayesianGaussianMixture(covariance_type='full')
#fitting the model to the data
clf.fit(df_1)

#predicting cluster lables

labels = clf.predict(df_1)

#plotting the data with the clusters labelled
ax_1 = df_1.plot.scatter(x = 'post_code', y= 'score', c=labels, cmap='viridis')
fig_1 = ax_1.get_figure()
fig_1.suptitle('Clustered Data', fontsize=16)
fig_1.savefig('price_postcode_clustered.pdf')

#no use, not enough data. so will need more features/potentially more data
#add commute_time (gives distance)
#add std_dev (gives centrality)
#these may correlate with post_code
"""


#currently the two length ones are seperated from the 4 length ones, price not 
#well correlated with post code/ post codes, its a bit better with score

#maybe need bigger dataset so have multiple from same postcode?