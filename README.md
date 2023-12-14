# Analysis of Movie Ratings

## _Details_

**Created by**: Eglė Švažienė and Vykintas Luciunas

This is the **end project** of Data Analysis and Python Programming Basics at Vilnius Coding School

**Course lecturer**: Modestas Viršila

**Project description**: ............(main goal)

## _Applied knowledge_

### In this project we have used:

**Programming language**: Python

**Libraries**: selenium, bs4 (BeautifulSoup), pandas, re, time, psycopg2, matplotlib, sqlalchemy, sklearn.linear_model, seaborn, numpy

**Database**: PostgreSQL

### Short description of files:

**ADDITIONALmain2.py**: full code for scraping the website and moving the data to a database (url scraped: https://www.imdb.com/search/title/?title_type=feature)

**main2Analysis.py**: code for taking the data from database, data cleanup, all of the analysis and their graphs

## Analysis results

1. graph - TOP 5 most frequent words in titles that are longer or equal to 4 letters.
![1_lentele.png](1_lentele.png)

2. graph - Comparison. Average Ratings by Year Critic vs People.
![2_lentele.png](2_lentele.png)
This graph, labeled as "Graph 2. Average Ratings by Year Critic vs People," illustrates the average ratings of movies over the years, comparing ratings from both critics and general audiences. The green line represents the average people rating, while the purple line represents the average critic rating. The x-axis shows the years, and the y-axes represent the rating scales. 
The graph provides a visual comparison of how movies have been rated over different years by both critics and the general audience.
Movies created until 1980 receive higher ratings from critics than from audiences. From 1980 to 2020, audience ratings are higher than those from critics.
Since 2020, the ratings from both critics and audiences have become very similar.

3. graph - Corelation between Votes and People's Ratings
![3_lentele.png](3_lentele.png)
Graph 3 illustrates the correlation between votes and people's ratings, revealing a correlation coefficient of 0.43. This positive correlation suggests a moderate association between the number of votes a movie receives and its people's rating. In other words, movies with higher people's ratings tend to attract more votes.

5. graph - 
![4_lentele.png](4_lentele.png)

6. graph - 
![5_lentele.png](5_lentele.png)

7. BONUS graph - TOP 10 "Christmas" Critically Acclaimed Movies with People Ratings and Votes.
![6_lentele.png](6_lentele.png)
Graph 6 is intended to provide you with movie recommendations for the Christmas season. It filters the best movies based on critic ratings with the word "Christmas" in the title. The graph also displays the audience rating and the number of votes for each film.

## Conclusion

_..............._
