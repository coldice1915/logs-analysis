#!/usr/bin/env python
# -*- coding: utf-8 -*-

# A reporting tool that answers the following three questions about 'newsdata.sql'

# Import postgresql library
import psycopg2

# Database
DBNAME = "news"

# Queries
query1 = """SELECT *
            FROM top_articles;"""

query2 = """SELECT name, sum(article_views.count) AS views
            FROM articles_author 
            JOIN article_views
            ON articles_author.title = article_views.title
            GROUP BY name
            ORDER BY views desc;"""

query3 = """SELECT error_logs.date, round(100.0 * error_count / log_count, 2) as percent
            FROM daily_logs
            JOIN error_logs
            ON daily_logs.date = error_logs.date
            AND error_count > log_count/100;"""


def connect(query):
    db = psycopg2.connect(database=DBNAME)
    c = db.cursor()
    c.execute(query)
    results = c.fetchall()
    db.close()
    return results


# Question 1: What are the most popular three articles of all time?
def top_three_articles(query):
    results = connect(query)
    print('\n The three most viewed articles of July 2016:\n')
    for i in results:
        print('\t' + str(i[0]) + ' - ' + str(i[1]) + ' views')
        print(" ")

# Question 2: Who are the most popular article authors of all time?
def top_authors(query):
    results = connect(query)
    print('\n The most popular authors of July 2016:\n')
    for i in results:
        print('\t' + str(i[0]) + ' - ' + str(i[1]) + ' views')
        print(" ")

# Question 3: On which days did more than 1% of requests lead to errors?
def error(query):
    results = connect(query)
    print('\n The day >1% of requests led to a 404 error:\n')
    for i in results:
        print('\t' + str(i[0]) + ' - ' + str(i[1]) + ' %' + ' 404 errors')
        print(" ")


# Print results
print top_three_articles(query1)
print top_authors(query2)
print error(query3)