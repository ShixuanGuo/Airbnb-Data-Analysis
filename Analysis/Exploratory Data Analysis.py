#!/usr/bin/env python
# coding: utf-8

# # 3. Exploratory Data Analysis

# ## 3.1 Spatial Data Analysis

# #### 2) Zipcode

# 5 active zipcode with the highest average listing price and more than 30 listing are 90210, 90077, 93063, 90265, 90069. Their average listing price are 1963.557367, 1909.066130, 1567.562500, 1559.605010, 998.113153 respectively. The number of active listings are 278, 74, 2, 329, 423 and the number of hosts are 173, 48, 1, 221, 305. 

# In[1]:


df_8a=df_cal.loc[(df_cal.date>='2020-01-01') & (df_cal.date<='2020-02-01') &                 (df_cal.available=='t'), :]
df_8a["price2"]=df_8a.price.apply(getmoney)
df_8b=df_8a.merge(df_list,how = "left", left_on = "listing_id", right_on="id").                  loc[:,["listing_id","price2","zipcode","host_id"]]
df_8c=df_8b.groupby(by=['zipcode']).filter(lambda x:x['listing_id'].count()>=30)
df_8d=sqldf('SELECT zipcode, AVG(price2) AS avg_price2, COUNT(DISTINCT listing_id) AS listing_id_count,              COUNT(DISTINCT host_id) AS host_id_count FROM df_8c GROUP BY zipcode ORDER BY avg_price2 DESC             LIMIT 5')
df_8d.head()


# Five zipcodes that have at least 30 listings and have the largest absolute difference between the average prices on weekends versus the average prices on weekdays are 91001, 91105, 93063, 90210, 90305

# In[2]:


df_9a=df_cal.loc[(df_cal.date>=dt.date(2020,1,1)) & (df_cal.date<=dt.date(2020,4,1)) &                 (df_cal.available=='t'), :]
df_9a["dayofweek"] = df_9a.dt.dayofweek
df_9a["weekday"] = df_9a["dayofweek"].apply(lambda x:"Weekend"if x[0]== "S" else ("Weekday"))
df_9b=df_9a.merge(df_list,how = "left", left_on = "listing_id", right_on="id")                  .loc[:,["date","dayofweek","weekday","listing_id","price","zipcode","host_id"]]
df_9c=df_9b.groupby(by=['zipcode']).filter(lambda x:x['listing_id'].count()>=30)
df_9d=sqldf("SELECT * FROM df_9c WHERE weekday='Weekday' GROUP BY zipcode")
df_9d=df_9d.groupby(by=["zipcode"])['price'].agg({"price":np.mean}).sort_values(by=["price"],ascending=False)
df_9e=sqldf("SELECT * FROM df_9c WHERE weekday='Weekend' GROUP BY zipcode")
df_9e=df_9e.groupby(by=["zipcode"])['price'].agg({"price":np.mean}).sort_values(by=["price"],ascending=False)
df_9f=df_9d.merge(df_9e,how = "outer", left_on = "zipcode", right_on="zipcode")
df_9f["max_abs_dif"]=df_9f["price_x"]-df_9f["price_y"]
df_9f.sort_values(by=["max_abs_dif"],ascending=False).head()


# ## 3.2 Price and D&S

# 1) Price of listing

# In[3]:


# Analysis of the average price of a listing in Los Angles
df_6=df_cal.groupby(by=['listing_id'])['price'].mean().agg([np.max,np.min,np.mean,np.std])
round(df_6,4)


# In[4]:


df_6b=df_cal.groupby(by=['date'])['price'].mean()
df_6b=pd.DataFrame(data=df_6b, columns=['price']).reset_index()


# In[5]:


fig,ax=plt.subplots(figsize=(7,5))
ax.plot(df_6b.date,df_6b.price,color='b')
ax.set(title = "Trend of Price", xlabel="Date", ylabel="Average price each day")
ax.xaxis.set_major_locator(mdates.MonthLocator())
plt.xticks(rotation=70)
plt.show()


# In[6]:


# Analysis of the average price of a listing in Los Angles from 01/01/2020 to 03/01/2020 (inclusive)
df_6a=df_cal.loc[(df_cal.date>='2020-01-01') & (df_cal.date<='2020-03-01') &                 (df_cal.available=='t'), :]

df_6=df_6a.groupby(by=['listing_id'])['price'].mean().agg([np.max,np.min,np.mean,np.std])
round(df_6,4)


# 2) The number of reviews  
# The number of reviews made has increased a lot.

# In[7]:


df_6c=df_review.groupby(by=['date'])['id'].nunique()
df_6c=pd.DataFrame(data=df_6c, columns=['id']).reset_index()


# In[8]:


fig,ax=plt.subplots(figsize=(7,5))
ax.plot(df_6c.date,df_6c.id,color='g')
ax.set(title = "Trend of Demand", xlabel="Date", ylabel="Number of reviews each day")
ax.xaxis.set_major_locator(mdates.YearLocator())
plt.xticks(rotation=70)
plt.show()


# In[9]:


df_6c2=df_review.loc[df_review.date>=dt.date(2015,1,1), :].groupby(by=['date'])['id'].nunique()
df_6c2=pd.DataFrame(data=df_6c2, columns=['id']).reset_index()


# In[10]:


fig,ax=plt.subplots(figsize=(7,5))
ax.plot(df_6c2.date,df_6c2.id,color='g')
ax.set(title = "Trend of Demand Annually", xlabel="Date", ylabel="Number of reviews each day")
ax.xaxis.set_major_locator(mdates.YearLocator())
plt.xticks(rotation=70)
plt.show()


# 3) Changes of number of listing  
# Number of listing did not change.

# In[11]:


df_6d=df_cal.groupby(by=['date'])['listing_id'].nunique().agg([np.max,np.min,np.mean,np.std])
df_6d


# In[12]:


df_6e=df_review.groupby(by=['date'])['listing_id'].nunique()
df_6e.agg([np.max,np.min,np.mean,np.std])


# In[13]:


df_6e=pd.DataFrame(data=df_6e, columns=['listing_id']).reset_index()

fig,ax=plt.subplots(figsize=(7,5))
ax.plot(df_6e.date,df_6e.listing_id,color='g')
ax.set(title = "Trend of Demand 2", xlabel="Date", ylabel="Number of listing each day")
ax.xaxis.set_major_locator(mdates.YearLocator())
plt.xticks(rotation=70)
plt.show()


# From year 2009, Airbnb demand has continuously increasd. After year 2015, the demand has increased rapidly.   
# We can see the peak and drop in each year: The demand is lowest in January and increases until October, when it begins to falls until the end of the year. This could possibly be due to the holiday season kicking in, with people celebrating Thanksgiving and Christmas at home with their family, leading to a slump in tourism and hence the demand for tourist lodging.

# 4) Daily capcaity

# From 2020-01-01 to 2020-04-01:  
# The average and standard deviation of the daily total capacity is 47091.648, 4921.138.  
# The average and standard deviation of the daily price per bed is 124.060, 5.634.

# In[14]:


ava_df_cal=df_cal.loc[(df_cal.date>=date(2020,1,1)) & (df_cal.date<date(2020,4,1))&            (df_cal.available=='t'), ["listing_id", "date", "price"]]
df_10a=df_list[['id','beds']].merge(ava_df_cal, how='inner', left_on='id', right_on='listing_id')

def getmoney(price):
    str_pri=str(price)
    str_price=str_pri.replace(",","").strip('$')
    num_price=float(str_price)
    return num_price

df_10a['price']=df_10a.price.apply(getmoney)


# In[15]:


df_10b=df_10a.groupby(by='date').agg({'beds':np.sum, 'price': np.sum})
df_10b.reset_index(inplace=True)
df_10b.beds.mean(),df_10b.beds.std()


# In[16]:


df_10b['price_pre_bed']=df_10b.apply(lambda x: x['price']/x['beds'], axis=1)
df_10b.price_pre_bed.mean(), df_10b.price_pre_bed.std()


# The daily occupancy trend from 2019-09-01 to 2020-09-01 (one year):  
# Price reflects the demands of the market. By sharing the same x-axis, which is date, we can know that the occupancy keeps increasing from the beginning of Sep 2019 to the mid of Dec 2019, which could be a potential reason for Airbnb's host to increase the price. After Christmas and new year celebration, the demand of house decreases rapidly which simultaneously leads to a decrease in price.

# In[17]:


#create a new database with target date and convert available data into numerical data
df_cal1=df_cal.loc[(df_cal.date>="2019-09-01") & (df_cal.date<="2020-09-01"),                    ["listing_id", "date", "available","price"]]

df_cal1['available_num']=df_cal1.available.apply(lambda x: 1 if x=='t' else 0)


# In[18]:


#calculate occupancy
from pandasql import sqldf
df_q1a=sqldf("SELECT date, COUNT(listing_id) AS total_list, SUM(available_num) AS total_available FROM df_cal1 GROUP BY date")
df_q1a["Occupancy"]=df_q1a['total_available']/df_q1a["total_list"]
df_q1a.head()

#plot result
import matplotlib.pyplot as plt
plt.style.use("ggplot")
fig, ax0=plt.subplots(nrows=1,ncols=1, figsize = (7,5))

df_q1a.plot(kind="line", x = "date", y = "Occupancy", color = 'b', label = "Occupancy",  ax = ax0 )
ax0.set(title = "Trend of Occupancy", xlabel="Date", ylabel="Occupancy each day")
# 4) Duration  
# Definition: The duration is the number of nights booked per year of a listing.  
# Most of the houses are under the normal range of 150-250. There are around 10 neighbourhoods that have a higher average durations with values greater than 250, which may indicates that the people in these neighbourhoods have a higher tendency to consider the house as a commercial house.

# In[19]:


import numpy as np
df_q3a=df_cal.loc[(df_cal.date>="2019-09-01") & (df_cal.date<="2020-09-01")&            (df_cal.available=='t'), ["listing_id", "available","price"]]

df_q3a['price']=df_q3a.price.apply(getmoney)
df_q3b=sqldf("SELECT listing_id, COUNT(available) AS Duration, AVG(price) AS Avg_Price              FROM df_q3a GROUP BY listing_id")
df_q3b.head()


# In[20]:


df_q3c=df_q3b.merge(df_list[['id','neighbourhood']], how='left', left_on='listing_id', right_on='id')
df_q3d=sqldf("SELECT neighbourhood, AVG(Duration) AS avg_Duration, AVG(Avg_Price) AS Avg_Price_N              FROM df_q3c GROUP BY neighbourhood ORDER BY AVG(Duration) DESC")
df_q3e=sqldf("SELECT neighbourhood, COUNT(DISTINCT id) AS total_list, AVG(Avg_Price) AS Avg_Price_N              FROM df_q3c GROUP BY neighbourhood ORDER BY total_list DESC")


# In[21]:


# plot the result
fig3, ax3_0=plt.subplots(nrows=1,ncols=1, figsize = (7,5))

df_q3d.plot(kind="scatter", x = "avg_Duration", y = "Avg_Price_N", color = 'b',  ax = ax3_0 )
ax3_0.set(title = "Listing Characters in Neighborhood", xlabel="Average Duration", ylabel="Average Price")


# ## 3.3 Host Data Analysis

# 1) What makes someone a superhost?

# For super host, the average number of listings is 7.359 with a standard deviation of 20.867. For non-super host, the average number of listings is 6.795 with a standard deviation of 14.348.

# In[22]:


df_3=df_list.groupby(by=['host_is_superhost'])['calculated_host_listings_count'].agg([np.mean,np.std])
df_3.reset_index(inplace=True)
df_3


# 2) What are the types of host verifications?

# There are 22 unique types of host veriftication in LA rental market.  
# The top 5 popular types are phone, email, reviews, government_id and offline_government_id

# In[23]:


for i in range(len(df_list)):
    a=df_list["host_verifications"][i].strip("[").strip("]").replace(' ', '').split(",")
    for j in range(len(a)):
        name=a[j][1:-1]
        print(name)


# In[24]:


#unique types of verification and the total number of hosts verify that type
d={}
count=0
for i in range(len(df_list)):
    a=df_list["host_verifications"][i].strip("[").strip("]").replace(' ', '').split(",")
    for j in range(len(a)):
        name=a[j][1:-1]
        if name in d:
            d[name]+=1
        else:
            d[name]=1
    count+=len(a)

len(d)
d


# In[25]:


host_verification=pd.DataFrame.from_dict(d, orient='index',columns=['Number'])


# In[26]:


#popular verification types and the percent of hosts verify that type
for name in d.keys():
    precent=d[name]/count
    d[name]=round(precent,4)

#sorted_d = sorted(d.items(), key=operator.itemgetter(1),reverse=True)


# In[27]:


host_verification['Frequency']=d.values()
host_verification.sort_values(by=['Number'],ascending=False)


# ## 3.4 User Reviews Analysis

# #### Top words

# In[28]:


df_review['date'].agg([np.max,np.min])


# In[29]:


#before convert date into date format
def gettopword(date, df_review):
    df_7a=df_review.loc[(df_review.date>=date[0]) & (df_review.date<=date[1]), :'comments']

    for index, row in df_7a.iterrows():
        l=row['comments']
        if type(l) is str:
            l=l.lower()
            list1 = "".join(c for c in l if (c not in string.punctuation and not c.isdigit()))        
            df_7a.loc[index,'comments']=list1
        else:
            df_7a.drop(index, axis=0, inplace=True)
    df_7s=df_7a['comments'].apply(lambda x: [item for item in x.split(' ') if (item not in stop)])

    wordcount={}
    for row in df_7s:
        for word in row:
            try:
                wordcount[word]+=1
            except:
                wordcount[word]=1

    wordcount_s=dict(sorted(wordcount.items(), key=operator.itemgetter(1), reverse=True)[1:11])
    return wordcount_s


# In[30]:


#top words from 2016-09-14 to 2019-09-14
wordcount=gettopword(df_review)
wordcount


# In[31]:


wordcount1=gettopword(['2016-01-01','2016-01-31'], df_review)
wordcount1


# In[32]:


wordcount2=gettopword(['2017-03-01','2017-03-31'], df_review)
wordcount2


# In[33]:


wordcount3=gettopword(['2018-04-01','2018-04-31'], df_review)
wordcount3


# #### Sentiment

# We analyzed scores and review sentiment in order to find the 'best' host with high score and positive feedback from reviews.

# In[34]:


# convert the database into a dictionary that include positive and negative words
dics = pd.read_excel('http://www.wjh.harvard.edu/~inquirer/inquirerbasic.xls',
                     dtype={'Entry':'str'})

df_q4a = dics[['Entry', 'Positiv', 'Negativ']].dropna(subset=['Positiv', 'Negativ'], how='all')
df_q4a['tag'] = 1
df_q4a.loc[(df_q4a['Negativ']=='Negativ'), 'tag'] = -1
df_q4a.drop(['Positiv', 'Negativ'], axis=1, inplace=True)
df_q4a[df_q4a['Entry'].str.contains(r'#')]
df_q4a['Entry'] = df_q4a['Entry'].str.replace(r'#\d+', '')
df_q4a = df_q4a.drop_duplicates()
cnts = df_q4a['Entry'].value_counts()
df_q4a[df_q4a['Entry'].isin(cnts[cnts==1].index)]
df_q4a['Entry'] = df_q4a['Entry'].str.lower()
df_q4a = df_q4a.set_index('Entry').squeeze()
df_q4a = df_q4a.to_dict()


# In[35]:


# create a clean comment list
def clean_comment(row):
    import string
    list2=[]
    l=row['comments']
    if type(l) is str:
        l=l.lower()
        list2 = "".join(c for c in l if (c not in string.punctuation and not c.isdigit()))        
    return list2

# count positive and negative words for each comment
def score(s, dic=df_q4a):
    negcnt, poscnt = 0, 0
    words = s['new_review'].split()
    for w in words:
        if dic.get(w,0) == 1:
            poscnt += 1
        elif dic.get(w,0) == -1:
            negcnt += 1
    return poscnt, negcnt, len(words)


# In[36]:


# using the purely positive score and rank the top 5 host
df_q4c=df_review.loc[:,["listing_id"]]
df_q4c["new_review"]=df_review.apply(clean_comment,axis=1)
df_q4d = df_q4c[df_q4c['new_review'].map(lambda x: len(x)) > 0]
df_q4d = df_q4d.apply(score,axis=1)
df_q4c['positive']=df_q4d.apply(lambda x: x[0])
df_q4c['negative']=df_q4d.apply(lambda x: x[1])
df_q4c['score']=df_q4c['positive']-df_q4c['negative']
df_q4d=df_q4c.groupby(by=['listing_id'])['score'].agg([np.sum])
df_q4e=df_q4d.sort_values(by=["sum"],ascending=False)
df_q4e=df_q4e.reset_index()
df_q4f=df_q4e.head(5)


# In[37]:


# develop a graph to illustrate the top 5 host ID with the most purely positive words
fig,ax0 = plt.subplots(figsize=(6,6))
fig.suptitle("Top 5 Hosts with Most Positive Review Words")

df_q4f.plot(kind="barh",x="listing_id",y="sum",color="r",ax=ax0) 
ax0.set(xlabel = "Number of Positive Words",ylabel="Host ID")
ax0.set_xlim([3000,4500])


# In[38]:


df_q5a=df_list.merge(df_q4e,how = "left", left_on = "id", right_on="listing_id").                     loc[:,['listing_id','review_scores_rating','review_scores_value','neighbourhood','sum']]
df_q5b=df_q5a.groupby(by='neighbourhood')['review_scores_rating'].agg([np.mean])
df_q5c=df_q5a.groupby(by='neighbourhood')['sum'].agg([np.mean])
df_q5d=df_q5b.sort_values(by=["mean"],ascending=False)
df_q5e=df_q5c.sort_values(by=["mean"],ascending=False)
df_q5f=df_q5d.reset_index()
df_q5f["Rank1"] = df_q5f["mean"].rank(ascending = 0) 
df_q5g=df_q5e.reset_index()
df_q5g["Rank2"] = df_q5g["mean"].rank(ascending = 0) 
df_q5h=df_q5f.merge(df_q5g,how = "inner", left_on = "neighbourhood", right_on="neighbourhood")
df_q5h.head()


# In[39]:


df_q5h[['Rank1','Rank2']].corr()


# In[40]:


fig, (ax0,ax1)=plt.subplots(nrows=2,ncols=1, figsize = (7,10),sharey=True)
df_q5h.plot(kind="line", x = "neighbourhood", y = "mean_x", color = 'g', label = "ranking by neighbourhood", ax = ax0)
ax0.set(title = "Review Value Ranking by Neighbourhood", xlabel="Neighbourhood", ylabel="Ranking")
df_q5h.plot(kind="line", x = "neighbourhood", y = "mean_y", color = 'r', label = "ranking by neighbourhood", ax = ax1 )
ax1.set(title = "Positive Ranking by Neighbourhood", xlabel="Neighbourhood", ylabel="Ranking")


# There is a small correlation (around 0.193) between positive words in comments with review score values, but there should be other factors that attribute more than positive words. Also, according on the visualization we created, we know that counting purely positive words would not reflect the hotel’s review score values, because two graphs does not have a similar trend. We might need to analyze more factors to finalize our model to answer this question.
