# Airbnb-Data-Analysis

![Airbnb](https://github.com/ShixuanGuo/Airbnb-Data-Analysis/blob/master/img/airsmall.png)

## Part 1 Project Introduction

In this project, I performed statistical analysis and regression analysis using the [Inside Airbnb](http://insideairbnb.com/get-the-data.html) listings and reviews data for Los Angeles, to give a deeper understanding of data patterns and trends in Los Angeles rental market.

1) **Files** used in the project:(download from : [Inside Airbnb](http://insideairbnb.com/get-the-data.html))
* listings.csv
* calendar.csv
* reviews.csv

**listings.csv** contains all historical and active listings in Los Angeles including descriptions of each listing and host, price, number of reviews, review scores, etc.   
**calendar.csv** contains details of calendar data including listing availability and price  
**reviews.csv** contains all reviews for each listing  

2) **Packages** used in the project:
* NumPy
* Pandas
* nltk
* string
* datetime
* pandasql
* matplotlib
* Scikit-learn  

3) **A quick glance at the data**:
-	There are 45k unique listings in LA in total. 
-	26k unique hosts in LA. On average, each host has 12 listings. The number of listings each host has is highly variant (standard deviation=242.144). The maximum and minimum number of listings per host is 29584 and 1.
-	1509564 of reviews have been written by guests
-	The average price of listing in LA in the first quarter of 2020 is $254.8. The average price of a listing in the first quarter of 2020 ranging from $10 to $25000 per night.


## Part 2 Analysis of Data Quality and Preprocessing  
1) Input data
First, I input all data and parse 'date' columns into date format using  
```python
df_list=pd.read_csv('listings.csv')
df_review=pd.read_csv('reviews.csv',parse_dates=['date'])
df_cal=pd.read_csv('calendar.csv',parse_dates=['date'])
```
Then I looked at the head, shape and some interesting features at the dataset to have an overview.
* There are 1509564 reviews in total. 
* Records started from 2019-09-14 to 2020-09-12.
```python
df_list.head()
unique_listing=df_list.id.nunique()
df_2=df_list.groupby(by=['host_id'])['calculated_host_listings_count'].sum()
df_2a=df_2.agg([np.mean,np.median,np.std, np.min, np.max])
# plot the number of listings per host
fig, ax=plt.subplots(figsize=(20,10))
plt.scatter(df_2.index,df_2,color = 'b',s=15)
ax.set_title('The Number of Listings per Host')
plt.show()
# look at outliers
df_2=df_2.to_frame().reset_index().sort_values(['calculated_host_listings_count'])
df_2['calculated_host_listings_count'].value_counts()
```
![Number of listings per host](https://github.com/ShixuanGuo/Airbnb-Data-Analysis/blob/master/img/Number%20of%20listings%20per%20host.png)  
* Most hosts have 1 listings (#:19872, above 2/3 of total hosts). On average, each host has 12 listings. The number of listings each host has is highly variant (standard deviation=242.144). Several hosts who have extremely large number of listings might be 'private real estate agency'.
* There are 45053 unique listings in LA.


2) Key features extraction  
* **price** (listings, calendar): string format, ‘$100’ with ‘,’ separator;  transformed into float values
* **date** (reviews, calendar): string format, transformed into date format, ‘mm-dd-yyyy’
* **location** (listings): ‘zipcode’, ‘latitude’, ‘longitude’, etc
* **rating** (listings): several columns including ‘review_scores_location’, ‘review_scores_cleanliness’ and 'review_scores_rating'
* **host** (listings): several columns including ‘host_id’, ‘host_is_superhost’,
* **comment** (reviews): string format, in multiple languages; sliced reviews that were in English and normalized text to remove common stop words and phrases that do not significantly contribute to the meaning of the review.

I extracted only key columns in the listing dataset. 

3) Missing values  
```python
miss_listings = df_list.isnull()
miss_50=df_list.columns[miss_listings.sum()/len(df_list)>0.5]
df_list=df_list.drop(miss_50,axis=1)
df_list.fillna(0,inplace=True)
```
The data had null values. I dropped the rows and columns containing more than 50% missing values and filled other missing values with 0.

4) Key features data cleaning  
a.I converted price from string into float.
```python
def getmoney(price):
    str_pri=str(price)
    str_price=str_pri.replace(",","").strip('$')
    num_price=float(str_price)
    return num_price
df_list['price']=df_list['price'].apply(getmoney)
```
b. I selected only English comments and normalized texts.
```python
for index, row in df_review.iterrows():
        l=row['comments']
        if type(l) is str:
            l=l.lower()
            list1 = "".join(c for c in l if (c not in string.punctuation and not c.isdigit()))        
            df_7a.loc[index,'comments']=list1
        else:
            df_7a.drop(index, axis=0, inplace=True)
    df_7s=df_7a['comments'].apply(lambda x: [item for item in x.split(' ') if (item not in stop)])
 ```
 c. I replaced boolean type columns with 0 and 1
 ```python
 def repl_f_t(l):
    l = l.replace('f', 0);
    l = l.replace('t', 1);
    return l
 ```

## Part 3 Exploratory Data Analysis
1) **Spatial Data Analysis**    
    Analysis the pattern of prices and ratings across different locations in LA:  
    * Zipcode  
    ![Zipcode1](https://github.com/ShixuanGuo/Airbnb-Data-Analysis/blob/master/img/zipcode1.png)  
    Expensive listings concentrate in areas with *zipcodes* of 90210, 90077, 93063, 90265, 90069.  
    ![Zipcode2](https://github.com/ShixuanGuo/Airbnb-Data-Analysis/blob/master/img/zipcode2.png)  
    Is it expensive to travel on weekend? The highest average price difference is $300. The prices of listings vary most from weekdays to weekends in the areas with zipcodes of 91001, 91105, 93063, 90210, 90305. The result indicates that these areas are popular travel or vocation spots.  

2) **Price and D&S Analysis**  
    * Average listing price    
    ![Trend of price](https://github.com/ShixuanGuo/Airbnb-Data-Analysis/blob/master/img/Trend%20of%20price.png)  
    The number of listing did not change in the most recent year, while the price has increased. So the price can indicate the changes of demand.  
    * Number of reviews  
    ![Trend of demand](https://github.com/ShixuanGuo/Airbnb-Data-Analysis/blob/master/img/Trend%20of%20demand.png)  
    ![Trend of demand annually](https://github.com/ShixuanGuo/Airbnb-Data-Analysis/blob/master/img/Trend%20of%20demand%20annually.png)  
    From year 2009, Airbnb demand has continuously increasd. After year 2015, the demand has increased rapidly. We can see the peak and drop in each year: The demand is lowest in January and increases until October, when it begins to falls until the end of the year. This could possibly be due to the holiday season kicking in, with people celebrating Thanksgiving and Christmas at home with their family, leading to a slump in tourism and hence the demand for tourist lodging.  
    * Daily occupancy  
    ![Daily occupancy](https://github.com/ShixuanGuo/Airbnb-Data-Analysis/blob/master/img/Daily%20occupancy.png)  
    ![Trend of occupancy](https://github.com/ShixuanGuo/Airbnb-Data-Analysis/blob/master/img/Trend%20of%20occupancy.png)  
    Daily average occupancy percentage varied a lot. From Sep 2019 to Sep 2020, the highest daily average occupancy percentage was on Nov 2019. It also indicates the changes of demand.  
    Price reflects the demands of the market. By sharing the same x-axis, which is date, we can know that the occupancy keeps increasing from the beginning of Sep 2019 to the mid of Dec 2019, which could be a potential reason for Airbnb's host to increase the price. After Christmas and new year celebration, the demand of house decreases rapidly which simultaneously leads to a decrease in price.  
    * Duration  
    ![Duration of listings](https://github.com/ShixuanGuo/Airbnb-Data-Analysis/blob/master/img/Duration%20of&20listings.png)  
    ![Duration and Price](https://github.com/ShixuanGuo/Airbnb-Data-Analysis/blob/master/img/Duration%20and%20Price.png)  
    We analyzed the relationship between duration and average price. This answer will help us to figure out the host behavior. For example, we will know whether the host is considered their Airbnb house as a commerical house to generate rent revenue or as a residential house. Based on our result, we know that most of the houses are under the normal range of 150-250. There are around 10 neighbourhoods that have a higher average durations with values greater than 250, which may indicates that the people in these neighbourhoods have a higher tendency to consider the house as a commercial house.  

3) **Host Data Analysis**  
    * What makes someone a superhost?  
    Super host policy is designed as an incentive program that is a win-win for both the host, Airbnb, and their customers. Super host have more listings than non-super host on average.  
    * Popular host verification types  
    phone, email, reviews, government_id and offline_government_id  
    ![Host Verification](https://github.com/ShixuanGuo/Airbnb-Data-Analysis/blob/master/img/Host%20Verification.png)  

4) **User Review Analysis**  
    * Top Words  
    Top frequently occurred words were ‘great’, ‘stay’, ‘clean’, ‘location’, ‘nice’, ‘host’, ‘comfortable’, which shows the features of the listings customers care about most:  environment, location and cleanliness.  
    * Review Sentiment  
    ![Review sentiment](https://github.com/ShixuanGuo/Airbnb-Data-Analysis/blob/master/img/Review%20sentiment.png)  
    ![Ranking](https://github.com/ShixuanGuo/Airbnb-Data-Analysis/blob/master/img/Ranking.png)  
    ![Sentiment ranking](https://github.com/ShixuanGuo/Airbnb-Data-Analysis/blob/master/img/Sentiment%20ranking.png)  
    There is a small correlation (around 0.193) between positive words in comments with review score values, but there should be other factors that attribute more than positive words. Also, according on the visualization we created, we know that counting purely positive words would not reflect the hotel’s review score values, because two graphs does not have a similar trend. We might need to analyze more factors to finalize our model to answer this question.  

