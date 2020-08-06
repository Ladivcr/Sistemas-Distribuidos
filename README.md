# Twitrends - Identifying possible trends on Twitter - MX
- José Vidal Cardona Rosas 

# Contact information
- vrosas832@gmail.com

# Type of licence
GNU General Public License v3.0
    
# Resume
* Identify possible trends Latin America
> This project was developed in Linux-Ubuntu, so, if you use Windows OS, maybe you will can have some 
problems with .sh file, but, you can rewrite the code for use it. Suppose that you use Ubuntu OS, 
with .sh you can use crontab and start to get Twets automatically. 
**Note:** This project was put into production on a web server with a static directory. You can see it here: http://www.gicc.unam.mx/twitrends/
      
# Software Tools
* Twitter API
* mysql Library
* json Library
* datetime Library
* Matplotlib Library
* sys Library
* Flask Library

# Data Source
* Twitter

# Architecture 
* Data source: Twitter
* Storage system: Mysql
* Processing system: Python, Tweepy, json and Mysql
* Data visualization: matplotlib.pyplot
* View Data: Python - Flask, HTML and CSS

# Install and use
## Some libraries that you need
```
   pip3 install Flask
   pip3 install matplotlib
   pip3 install mysql-connector
   pip3 install tweepy
```

## About our Data Base
Before, you need to install Server SQL in your machine
* > sudo apt install mysql-server

After the install and config, follow the steps for create the Data Base as follow:

* > CREATE DATABASE trends;
* > USE trends;
* > CREATE TABLE possible_trends(hashtag VARCHAR (280), quantity INT, publication_date DATE);


**Now, you have the necessary libraries. Follow the next steps for use the project** 
* Clone or download this project: https://github.com/Ladivcr/Sistemas-Distribuidos.git 
> You will need to use some credencial from API Twitter. If you have it Please read config.txt 
> If you don't have credencial, you can get it in: [Twitter developer](https://developer.twitter.com/en) 

> After that you download/clone this project, <strong>you need to read the file: config.txt</strong>
If you already read the file...
* Open a terminal and write:
```
    ./00runTrends.sh
```
* After this, you start to get the data from Twitter automatically.
## to view the page

* Open a terminal and write: (Only if the project has not been mounted on a server)
```
    cd www/
    python3 twitrends.py
```

> After this, the terminal display the addres for the web page 
* Copy the address
* Paste in a browser and...

# You can view something like: 
![mainPage](resources/mainPage.png)
![secondPage](resources/secondPage.png)
![filterPage](resources/filterPage.png)


# Abstract
    Currently, we have the power of social media for communication in real time
    and the principal use is communication. 
    But we can give a second use all this tools on different fields like e-commerce, 
    political, sales, etc. Twitter is a network of networks and the people share 
    "Tuits" with things about their day a day with some data, data about food,
    drinks, clothes, feelings, opinions, etc. Sometimes used "hashtags" for describe
    the "Tuit". So we can do  Web scraping for get this different kinds data, 
    clean the data and processing the data and finally try to identify a trend.

# Methodology
Extreme programming 

# Implementation and tests
We ran our code for get some tweets with filter per geographical coordinates
and we had lucky because we could catch many tweets but, we wanted to try our others
codes (02 and 03) so, we stored this tweets and plot this tweets. 
## Results
## Storage tweets 
![tuit](resources/mysql.png)
# Plot tweets
![code](resources/possible_trends-15-05-2020-19-43-46.png)

As we can see, there are many tweets because when we did the query, we didn't specify 
some range. 

# Conclusions
Our project is not over yet

# Bibliography
We can did it with some help.
* To get data: [documentation about tweepy](https://tweepy.readthedocs.io/en/v3.5.0/index.html#) 
* To visualize web page: [documentation about Flask](https://flask.palletsprojects.com/en/1.1.x/)
