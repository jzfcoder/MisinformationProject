from sqlite3 import Error
import sqlite3
import os

def select_keywords(conn):
    """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
    """
    strOptions = []
    cur = conn.cursor()
    cur.execute("SELECT Keywords, Headline, url FROM ArticleTable")
    rows = cur.fetchall()
    for row in rows:
        strOptions.append(row)
        print(row)
    # print(bcolors.OKGREEN + "I'm Done :D" + bcolors.ENDC)
    return strOptions

def create_connection(db_file):
    # print("Creating Connection ...")

    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)
    return conn

if __name__ == "__main__":
    database = r"sqlite\Databases\MainDatabase\MainDatabase.db"
    conn = create_connection(database)
    with conn:
        select_keywords(conn)