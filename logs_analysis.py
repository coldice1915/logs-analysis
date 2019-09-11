#!/usr/bin/env python
# -*- coding: utf-8 -*-

# A reporting tool that answers three questions about 'newsdata.sql'

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

query3 = """SELECT error_logs.date,
                round(100.0 * error_count / log_count, 2) as percent
            FROM daily_logs
            JOIN error_logs
            ON daily_logs.date = error_logs.date
            AND error_count > log_count/100;"""


def connect(query):
    try:
        db = psycopg2.connect(database=DBNAME)
    except psycopg2.Error:
        pass
    c = db.cursor()
    c.execute(query)
    results = c.fetchall()
    db.close()
    return results


# Question 1: What are the most popular three articles of all time?
def top_three_articles(query):
    results = connect(query)
    print('\n The three most viewed articles of July 2016:\n')
    for article, views in results:
        print('\t{} - {} views\n'.format(article, views))


# Question 2: Who are the most popular article authors of all time?
def top_authors(query):
    results = connect(query)
    print('\n The most popular authors of July 2016:\n')
    for author, views in results:
        print('\t{} - {} views\n'.format(author, views))


# Question 3: On which days did more than 1% of requests lead to errors?
def error(query):
    results = connect(query)
    print('\n The day >1% of requests led to a 404 error:\n')
    for date, error in results:
        print('\t{} - {}% 404 errors\n'.format(date, error))


# Print results to three questions
top_three_articles(query1)
top_authors(query2)
error(query3)
