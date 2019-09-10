###### Updated as of 09/10/2019
# Logs Analysis

A python script that queries a database and prints the answer to three questions:
1. What are the most popular three articles of all time?
2. Who are the most popular article authors of all time?
3. On which days did more than 1% of requests lead to errors?


## Table of contents
- [Introduction](#introduction)
- [Technologies](#technologies)
- [Setup](#setup)
- [Launch](#launch)
- [What have I done?](#what-have-i-done?)


## Introduction
Working on a newspaper site, I've been asked to build an internal reporting tool that will use information from the database to discover what kind of articles the site's readers like.

The database contains newspaper articles, as well as the web server log for the site. The log has a database row for each time a reader loaded a web page. Using this information, my code will answer questions about the site's user activity. 

The program will run from the command line and it won't take any input from the user. It will connect to the database, use SQL queries to analyze the log data, and print out the answers to the questions.

My task is to create a reporting tool that prints out reports (in plain text) based on the data in the site database. This reporting tool is a Python program using the `psycopg2` module to connect to the database.


## Technologies
Terminal (macOS) • Python 2.7.16 • Psycopg 2.8.3 • Vagrant 2.2.0 • VirtualBox 6.0.10


## Setup
### 1. Install VitualBox 
Download [VirtualBox](https://www.virtualbox.org/wiki/Downloads). Install the platform package for your operating system.

### 2. Install Vagrant
Download [Vagrant](https://www.vagrantup.com/downloads.html). Install the version for your operating system.

If Vagrant is successfully installed, you will be able to run `vagrant --version`   in your terminal to see the version number.

### 3. Download the VM configuration
Download and unzip this file: [FSND-Virtual-Machine.zip](https://s3.amazonaws.com/video.udacity-data.com/topher/2018/April/5acfbfa3_fsnd-virtual-machine/fsnd-virtual-machine.zip).
(Alternately, you can use Github to fork and clone this [repository](https://github.com/udacity/fullstack-nanodegree-vm).)

### 4. Start the virtual machine
In your terminal, `cd` to the **/vagrant** subdirectory and run the command `vagrant up` to start the Ubuntu Linux installation.

When it is finished running, run the command `vagrant ssh` to log in.

### 5. Download the data
Download and unzip this file: [newsdata.zip](https://d17h27t6h515a5.cloudfront.net/topher/2016/August/57b5f748_newsdata/newsdata.zip). Move the file *newsdata.sql* into the **/vagrant** subdirectory.

`cd` into the **/vagrant** subdirectory and run the command `psql -d news -f newsdata.sql` to connect to the *news* database and run SQL commands in *newsdata.sql*.

### 6. Create the following views:
#### Views for Question 1
```sql
CREATE VIEW articles_author AS
    SELECT title, name
    FROM articles JOIN authors
    ON articles.author = authors.id;
```
```sql
CREATE VIEW top_articles AS
    SELECT articles.title, count(log.path)
    FROM articles
    JOIN log ON log.path LIKE concat('%',articles.slug) 
    GROUP BY articles.title ORDER BY count(log.path) desc limit 3;
```

#### Views for Question 2
```sql
CREATE VIEW articles_author AS
    SELECT title, name
    FROM articles JOIN authors
    ON articles.author = authors.id;
```
```sql 
CREATE VIEW article_views AS
    SELECT articles.title, count(log.path)
    FROM articles
    JOIN log ON log.path LIKE concat('%',articles.slug) 
    GROUP BY articles.title ORDER BY count(log.path) desc;
```

#### Views for Question 3
```sql
CREATE VIEW daily_logs AS
    SELECT to_char(time,'DD-MON-YYYY') as date, count(*) as log_count
    FROM log
    GROUP BY date;
```
```sql
CREATE VIEW error_logs AS
    SELECT to_char(time,'DD-MON-YYYY') as date, count(*) as error_count
    FROM log
    WHERE STATUS = '404 NOT FOUND'
    GROUP BY date ORDER BY date;
```

####
After creating the views, exit psql.


## Launch
### 1. Download the script
Download and unzip this file: [logs_analysis_project-master.zip](https://github.com/coldice1915/logs_analysis_project/archive/master.zip).
(Or, you can use Github to fork and clone this [repository](https://github.com/coldice1915/logs_analysis_project.git))

### 2. Run the script
`cd` to the directory and run `python logs_analysis.py` to execute the script


## What have I done?
- [x] Installed and launched a virtual machine to create a familiar environment
- [x] Interacted with the database from both the command line and my code
- [x] Ran SQL commands to view tables and data types within the large database
- [x] Ran SQL statements to analyze the log data (SELECT, WHERE, JOIN, etc.)
- [x] Tested queries to better understand complex relationships
- [x] Built queries to answer the three questions
- [x] Created views to the database to refine queries
- [x] Drew business conclusions by answering significant questions
- [x] Connected Python code to the database using psycopg2, a PostgreSQL database adapter
- [x] Cleaned and edited code for readability
- [x] Submitted project for review


##### Sources
Udacity