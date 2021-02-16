from google.oauth2 import service_account
from google.cloud import language_v1
from fuzzywuzzy import process
from sqlite3 import Error
import sqlite3
import os

def analyze_entities(text_content):
    """
        Analyzing Entities from a String

        Args:
        text_content The text content to analyze
    """
    # Set connection to client as variable
    credentials = service_account.Credentials.from_service_account_file(r"C:\Users\timfl\Documents\GoogleCloudKeys\MyFirstProject-e85779938beb.json")
    client = language_v1.LanguageServiceClient(credentials=credentials)

    # Set type_ to read PLAIN_TEXT
    type_ = language_v1.Document.Type.PLAIN_TEXT

    # specify language & set document variable
    '''
        https://cloud.google.com/natural-language/docs/languages
        if language is not set, it will be detected.
    '''
    lang = "en"
    document = {"content": text_content, "type_": type_, "language": lang}

    # Set Encoding type to UTF8
    encoding_type = language_v1.EncodingType.UTF8

    # Pass in client request with defined specifications
    response = client.analyze_entities(request = {'document': document, 'encoding_type': encoding_type})

    entArray = []
    # Loop through entitites returned from the API
    for entity in response.entities:
        '''
            Get entity name
            print(entity.name)
            Get entity type (PERSON, LOCATION, ADDRESS, NUMBER, etc)
            print(language_v1.Entity.Type(entity.type_).name)
        '''
        entArray.append(entity.name.replace("'", "''"))
        print(entArray)
    return entArray

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

def select_headlines(conn):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    pos = 0
    result = []
    cur = conn.cursor()
    cur.execute("SELECT Headline FROM ArticleTable")
    rows = cur.fetchall()
    for row in rows:
        row = " ".join(str(x) for x in row)

        result = analyze_entities(row)
        result = " ".join(str(i) for i in result)
        cursor = conn.cursor()
        cursor.execute("UPDATE ArticleTable SET Keywords = \'" + result + "\' WHERE ROWID = " + str(pos))
        pos = pos + 1

if __name__ == "__main__":
    database = r"sqlite\Databases\MainDatabase\MainDatabase.db"
    conn = create_connection(database)
    with conn:
        select_headlines(conn)