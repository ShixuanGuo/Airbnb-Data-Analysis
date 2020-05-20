# Airbnb-Data-Analysis

In this project, I performed statistical analysis and regression analysis using the [Inside Airbnb](http://insideairbnb.com/get-the-data.html) listings and reviews data for Los Angeles, to give a deeper understanding of data patterns and trends in Los Angeles rental market.

Files used in the project:(download from : [Inside Airbnb](http://insideairbnb.com/get-the-data.html))
* listings.csv
* calendar.csv
* reviews.csv

**listings.csv** contains all historical and active listings in Los Angeles including descriptions of each listing and host, price, number of reviews, review scores, etc.   
**calendar.csv** contains details of calendar data including listing availability and price  
**reviews.csv** contains all reviews for each listing  

Packages used in the project:
* NumPy
* Pandas
* nltk
* string
* pandasql
* matplotlib
* Scikit-learn  

Summary of insights:  

1. Price reflects the demands of the market. By sharing the same x-axis, which is date, we can know that the occupancy keeps increasing from the beginning of Sep 2019 to the mid of Dec 2019, which could be a potential reason for Airbnb's host to increase the price. After Christmas and new year celebration, the demand of house decreases rapidly which simultaneously leads to a decrease in price.

2. We analyzed the relationship between duration and average price. This answer will help us to figure out the host behavior. For example, we will know whether the host is considered their Airbnb house as a commerical house to generate rent revenue or as a residential house. Based on our result, we know that most of the houses are under the normal range of 150-250. There are around 10 neighbourhoods that have a higher average durations with values greater than 250, which may indicates that the people in these neighbourhoods have a higher tendency to consider the house as a commercial house.

3. There is a small correlation (around 0.193) between positive words in comments with review score values, but there should be other factors that attribute more than positive words. Also, according on the visualization we created, we know that counting purely positive words would not reflect the hotel’s review score values, because two graphs does not have a similar trend. We might need to analyze more factors to finalize our model to answer this question.
