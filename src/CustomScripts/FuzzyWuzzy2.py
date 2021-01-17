from fuzzywuzzy import process
from sqlite3 import Error
import sqlite3
import os

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

'''
    str2Match = "hack democrat haul russia"
    "Top Intelligence Democrat accuses Russia of cyber hack that resulted in 'big haul'",
    "'Pretty clear' Russia behind SolarWinds hack, Pompeo says, becoming 1st US official to blame Moscow",
    "FBI scrambles to assess damage from Russia-linked US government hack",
    "Senator: Treasury Dept. email accounts compromised in hack"    
    https://www.datacamp.com/community/tutorials/fuzzy-string-python
'''
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
    cur.execute("SELECT Headline FROM ArticleTable")
    rows = cur.fetchall()
    for row in rows:
        strOptions.append(row[0])
    print(bcolors.OKGREEN + "I'm Done :D" + bcolors.ENDC)

def isolate():
    str2Match = input("Keywords here: ")
    Ratios = process.extract(str2Match,strOptions)
    matches = []
    for i in Ratios:
        if (i[1] >= 50):
            matches.append(i)
    highest = process.extractOne(str2Match,strOptions)
    print(bcolors.HEADER + "HIGHEST:" + bcolors.ENDC , bcolors.OKCYAN + str(highest) + bcolors.ENDC)
    print(bcolors.HEADER + "MATCHES: " + bcolors.ENDC, bcolors.OKCYAN + str(matches) + bcolors.ENDC)

def fuzzy_main():
    database = r"sqlite\Databases\MainDatabase\MainDatabase.db"
    conn = create_connection(database)
    with conn:
        select_headlines(conn)
    isolate()

if __name__ == '__main__': 
    strOptions = []
    matches = []
    fuzzy_main()

'''
    You can also select the string with the highest matching percentage
    highest = process.extractOne(str2Match,strOptions)
    print("HIGHEST: " , highest)
'''