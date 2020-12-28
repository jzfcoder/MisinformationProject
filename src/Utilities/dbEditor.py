from sqlite3 import Error
import sqlite3
import os

def create_connection(db_file):
    print(bcolors.OKGREEN + "Creating Connection ..." + bcolors.ENDC)
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

def select_headlines(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT Headline FROM ArticleTest1")
    rows = cur.fetchall()
    for row in rows:
        strOptions.append(row[0])
    print(bcolors.OKGREEN + "I'm Done :D" + bcolors.ENDC)

def fuzzy_main():
    database = r"C:\Users\timfl\Documents\GitHub\MisinformationProject\sqlite\Databases\ArticleDatabase\ArticleSQL.db"
    conn = create_connection(database)
    with conn:
        select_headlines(conn)
    isolate()