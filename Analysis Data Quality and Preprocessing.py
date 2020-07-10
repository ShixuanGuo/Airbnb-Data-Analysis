#!/usr/bin/env python
# coding: utf-8

# In[1]:


# Import necessary packages
import pandas as pd
import numpy as np
import operator

from nltk.corpus import stopwords
stop = stopwords.words('english')

import string
from string import digits
punctuation = string.punctuation

from pandasql import sqldf

import datetime as dt

import matplotlib.pyplot as plt
import matplotlib.dates as mdates
from matplotlib.dates import DateFormatter
import seaborn as sns


# # 1. Overview of database

# In[2]:


#import data
df_list=pd.read_csv('listings.csv')
df_review=pd.read_csv('reviews.csv',parse_dates=['date'])
df_cal=pd.read_csv('calendar.csv',parse_dates=['date'])


# In[7]:


df_review.head()


# In[7]:


df_list.head()


# ## 1.1 Listing

# There are 45053 unique listings in LA. 

# In[41]:


unique_listing=df_list.id.nunique()
print(unique_listing)


# The recorded prices start from 2019-09-14 and end at 2020-09-12

# In[14]:


df_cal['date'].max(),df_cal['date'].min()


# ## 1.2 Host

# There are 26286 unique hosts in LA in total.

# In[5]:


print(df_list.host_id.nunique())


# On average, each host has 12 listings.  
# The maximum and minimum number of listings per host is 29584 and 1.  
# The number of listings per host varies a lot. 

# In[58]:


df_2=df_list.groupby(by=['host_id'])['calculated_host_listings_count'].sum()
df_2a=df_2.agg([np.mean,np.median,np.std, np.min])
df_2a


# In[61]:


df_2=df_2.to_frame().reset_index().sort_values(['calculated_host_listings_count'])


# In[62]:


df_2['calculated_host_listings_count'].value_counts()


# In[43]:


# host_id=df_list['host_id'].value_counts()
fig, ax=plt.subplots(figsize=(20,10))
plt.scatter(df_2.index,df_2,color = 'b',s=15)
ax.set_title('The Number of Listings per Host')
plt.show()


# ## 1.3 Reviews

# There are 1509564 reviews in total.

# In[10]:


df_review.shape[0]


# # 2. Analysis of Data Quality

# ## 2.1 Key Features

# In[5]:


# extract key columns we want to analysis
list_columns=['id','price','room_type','neighbourhood','beds',
              'host_id','calculated_host_listings_count','host_is_superhost','host_verifications',
              'number_of_reviews','reviews_per_month','review_scores_location', 'review_scores_cleanliness','review_scores_rating',
              'zipcode','latitude','longitude']
df_list=df_list[list_columns]


# ## 2.2 Missing Data

# In[7]:


#find all missing data
miss_listings = df_list.isnull()
miss_cal=df_cal.isnull()
miss_review=df_review.isnull()
print(miss_listings.shape[0],miss_cal.shape[0],miss_review.shape[0])


# In[8]:


miss_listings.sum()


# In[9]:


#remove all columns with more than 50% missing values
miss_50=df_list.columns[miss_listings.sum()/len(df_list)>0.5]
df_list=df_list.drop(miss_50,axis=1)

#fill other missing values
df_list.fillna(0,inplace=True)


# In[10]:


miss_50


# ## 2.2 Data Transforming

# In[11]:


#price: in string format; transform into float values
def getmoney(price):
    str_pri=str(price)
    str_price=str_pri.replace(",","").strip('$')
    num_price=float(str_price)
    return num_price
df_list['price']=df_list['price'].apply(getmoney)
df_cal['price']=df_cal['price'].apply(getmoney)


# In[41]:


#comments: only select comments in English and normalize text
for index, row in df_review.iterrows():
        l=row['comments']
        if type(l) is str:
            l=l.lower()
            list1 = "".join(c for c in l if (c not in string.punctuation and not c.isdigit()))        
            df_7a.loc[index,'comments']=list1
        else:
            df_7a.drop(index, axis=0, inplace=True)
    df_7s=df_7a['comments'].apply(lambda x: [item for item in x.split(' ') if (item not in stop)])


# In[12]:


# Boolean types are replaced with a 0 or 1
def repl_f_t(l):
    l = l.replace('f', 0);
    l = l.replace('t', 1);
    return l


# In[13]:


#date
df_cal['date']=df_cal['date'].dt.date
df_review['date']=df_review['date'].dt.date


# In[ ]:




