#!/usr/bin/env python
# -*- coding: utf-8 -*-

# A reporting tool that answers three questions about 'newsdata.sql'
# Question 1: What are the most popular three articles of all time?
# Question 2: Who are the most popular article authors of all time?
# Question 3: On which days did more than 1% of requests lead to errors?

__author__ = 'JamesHan'
import psycopg2
try:
    db = psycopg2.connect(database="news")
    print ("Connection to the news database successful!")
except psycopg2.connect.Error as e:
    print ("Oh no, a connection error has occurred!")


# Helper function in executing and returning queries
def get_results(query):
    cursor = db.cursor()
    cursor.execute(query)
    results = cursor.fetchall()
    db.commit()
    cursor.close()
    return results


# Query statements
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


# Defining the three answers
def top_articles(query):
    results = get_results(query)
    print ('Q.1|| What are the most popular three articles of all time?\n')
    for (article, view) in results:
        print ('\t{0} - {1} views\n'.format(article, view))


def top_authors(query):
    results = get_results(query)
    print ('Q.2|| Who are the most popular article authors of all time?\n')
    for (author, views) in results:
        print ('\t{0} - {1} views\n'.format(author, views))


def error_percent(query):
    results = get_results(query)
    print ('Q.3|| Which day did more than 1% of requests lead to an error?\n')
    for (date, error) in results:
        print ('\t{0} - {1}% 404 errors\n'.format(date, error))


# Printing the answers to the three questions
answer_1 = top_articles(query1)
answer_2 = top_authors(query2)
answer_3 = error_percent(query3)

db.close()
