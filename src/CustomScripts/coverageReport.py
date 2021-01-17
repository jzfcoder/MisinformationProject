from sqlite3 import Error
import sqlite3
import os

left = 0
leanLeft = 0
center = 0
leanRight = 0
right = 0
mixed = 0

sourceAr = []
biasAr = []

def article_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def select_source(conn, headline):
    cur = conn.cursor()
    cur.execute("SELECT Provider FROM ArticleTable WHERE Headline LIKE ('%" + headline + "%')")
    rows = cur.fetchall()
    print(headline)
    for row in rows:
        tempString = str(row)
        fString = tempString.replace('(','').replace('\'','').replace(',','').replace(')','')
        sourceAr.append(fString)

def bias_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def find_bias(conn, domain_):
    cur = conn.cursor()
    cur.execute("SELECT BiasRating FROM BiasTable WHERE Domain LIKE ('%" + domain_ + "%')")
    rows = cur.fetchall()
    for row in rows:
        tempString = str(row)
        fString = tempString.replace('(','').replace('\'','').replace(',','').replace(')','')
        biasAr.append(fString)

def report_main(input):
    x = 0
    for i in input:
        x = x + 1
        tstring = str(i).replace("''", "''''")
        input.pop(x - 1)
        input.insert(x - 1, tstring)
    for i in input:
        # access database and search for headline
        database = r"sqlite\Databases\MainDatabase\MainDatabase.db"
        conn = article_connection(database)
        with conn:
            select_source(conn, i)
        # return source in sourceAr
    for i in sourceAr:
        # access bias database and search domains for source/bias
        database = r"sqlite\Databases\MainDatabase\MainDatabase.db"
        conn = bias_connection(database)
        with conn:
            find_bias(conn, i)
        # search bias db for bias type
        # add 1 to int var of any bias

    left = biasAr.count("Left")
    leanLeft = biasAr.count("Lean Left")
    center = biasAr.count("Center")
    leanRight = biasAr.count("Lean Right")
    right = biasAr.count("Right")
    mixed = biasAr.count("Mixed")

    print(left, leanLeft, center, leanRight, right, mixed)
    # fox fox ap abc

if __name__ == '__main__':
    input_ = input = [
        "FBI scrambles to assess damage from Russia-linked US government hack",
        "Senator: Treasury Dept. email accounts compromised in hack",
        "White House coronavirus response coordinator Birx plans to retire after travel backlash",
        "Fauci receives vaccine, has ''extreme confidence'' it''s safe, effective"
        ]
    report_main(input_)