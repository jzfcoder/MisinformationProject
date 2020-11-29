from tld import get_tld

import sqlite3
from sqlite3 import Error

import os

link = input("Enter Article Link Here: ")
#link = "http://abcnews.go.com"
domain = get_tld(link, as_object=True)
print("We found this domain from your link: " + domain.fld) # --> www.example.test


# Initialize Connection to Source Bias Database
def create_connection(db_file):

    print("Creating Connection ...")
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

# Find Row relative to DOMAIN thru SQL
def select_bias(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute("SELECT BiasRating FROM BiasDB WHERE Domain like '%" + domain.fld + "%' ")

    rows = cur.fetchall()

    for row in rows:
        print(row[0])

def main():
    database = r"sqlite\BiasDB.db"
    
    # create a database connection
    conn = create_connection(database)
    with conn:
        print(domain.fld + "'s bias is...")
        select_bias(conn)

if __name__ == '__main__': 
    main()