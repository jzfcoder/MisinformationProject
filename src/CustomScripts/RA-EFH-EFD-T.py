from google.oauth2 import service_account
from google.cloud import language_v1
from fuzzywuzzy import process
from fuzzywuzzy import fuzz
from sqlite3 import Error
import sqlite3
import os

def convert1(lst):

    return ' '.join(lst)

def get_related(headline):
    database = r"sqlite\Databases\MainDatabase\MainDatabase.db"
    conn = create_connection(database)
    with conn:
        return isolate(analyze_entities(headline), select_keywords(conn), headline)

def isolate(strBase, strOptions, Input):
    str2Match = ""
    base2Match = []
    test = {i: val for i, val in enumerate(strOptions)}

    for i in strBase:
        temp = i[0]
        base2Match.append(temp)

    str2Match = (convert1(base2Match))
    Ratios = process.extract(str2Match, test, scorer=fuzz.WRatio)
    matches = []
    for i in Ratios:
        if (i[1] >= 55):
            matches.append(i)

    results = []
    headlineURL = []

    for i in matches:
        temp = []
        temp.append(i[0])
        temp.append(i[2])
        results.append(temp)
    for i in results:
        database = r"sqlite\Databases\MainDatabase\MainDatabase.db"
        conn = create_connection(database)
        with conn:
            test = select_db(conn, i[1])
            test = convert1(test[0])
            test.replace("(", "")
            test.replace(")", "")
            test.replace("]", "")
            test.replace("[", "")
            test.replace(",", "")
            headlineURL.append(test)
    
    f = open(r"TestingSaves\RA-EFH-EFD\Trial1\RA-EFH-EFD-T55.2.16.txt", "a")
    f.write("\nINPUT: " + str(Input) + "\n")
    f.write("   MATCHES: " + str(headlineURL))
    f.close()
    return headlineURL

def analyze_entities(text_content):
    credentials = service_account.Credentials.from_service_account_file(
        r"C:\Users\timfl\Documents\GoogleCloudKeys\MyFirstProject-e85779938beb.json")
    # Instantiates a client
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
    response = client.analyze_entities(
        request={'document': document, 'encoding_type': encoding_type})

    # Loop through entitites returned from the API
    for entity in response.entities:
        '''
            Get entity name
            print(entity.name)
            Get entity type (PERSON, LOCATION, ADDRESS, NUMBER, etc)
            print(language_v1.Entity.Type(entity.type_).name)
        '''

        # print(entity.name)
        # Get salience score in [0, 1.0] range
        # print(u"Salience score: {}".format(entity.salience))
        strBase = []
        # Loop over the mentions of entity from input document.
        for mention in entity.mentions:
            tempArray = []

            # append name of entity to tempArray
            tempArray.append(u"{}".format(mention.text.content))

            # Get mention type, e.g. PROPER for proper noun
            tempArray.append(u"{}".format(
                language_v1.EntityMention.Type(mention.type_).name))

            strBase.append(tempArray)
            # print(tempArray)
        return strBase
    # print(strBase)

def select_keywords(conn):
    strOptions = []
    cur = conn.cursor()
    cur.execute("SELECT Keywords FROM ArticleTable")
    rows = cur.fetchall()
    for row in rows:
        strOptions.append(row[0])
    # print(bcolors.OKGREEN + "I'm Done :D" + bcolors.ENDC)
    return strOptions

def select_db(conn, location):
    strOptions = []
    cur = conn.cursor()
    cur.execute("SELECT Headline FROM ArticleTable WHERE ROWID = " + str(location))
    rows = cur.fetchall()
    for row in rows:
        strOptions.append(row)
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
    headline = input("text here: ")
    print(get_related(headline))