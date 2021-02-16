from google.oauth2 import service_account
from google.cloud import language_v1
from fuzzywuzzy import process
from sqlite3 import Error
import sqlite3
import os

def convert(lst): 
      
    return ' '.join(lst) 
def convert1(lst):
    return ' '.join(lst)


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

    # Loop through entitites returned from the API
    base = []
    for entity in response.entities:
        '''
            Get entity name
            print(entity.name)
            Get entity type (PERSON, LOCATION, ADDRESS, NUMBER, etc)
            print(language_v1.Entity.Type(entity.type_).name)
        '''
        # Loop over the mentions of entity from input document.
        for mention in entity.mentions:
            tempArray = []

            mentionType = u"{}".format(language_v1.EntityMention.Type(mention.type_).name)

            if (mentionType != "PROPER"):
                # append name of entity to tempArray
                tempArray.append(u"{}".format(mention.text.content))

                # Get mention type, e.g. PROPER for proper noun
                tempArray.append(u"{}".format(language_v1.EntityMention.Type(mention.type_).name))

                base.append(tempArray)
    return base

def create_connection(db_file):
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
    headlines = []
    cur = conn.cursor()
    cur.execute("SELECT Headline FROM ArticleTable")
    rows = cur.fetchall()
    for row in rows:
        headlines.append(row[0])
    return headlines

def isolate(strBase, strOptions):
    str2Match = ""
    base2Match = []

    for i in strBase:
        temp = i[0]
        base2Match.append(temp)

    str2Match = (convert1(base2Match))
    Ratios = process.extract(str2Match, strOptions)
    matches = []
    for i in Ratios:
        if (i[1] >= 50):
            matches.append(i)

    results = []
    for i in matches:
        results.append(i[0])
    return results

def get_related(headline):
    database = r"sqlite\Databases\MainDatabase\MainDatabase.db"
    conn = create_connection(database)
    with conn:
        return isolate(analyze_entities(headline), select_headlines(conn))

if __name__ == "__main__":
    Input = input("text here: ")
    print(get_related(Input))