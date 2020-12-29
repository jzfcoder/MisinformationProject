from google.cloud import language_v1
from fuzzywuzzy import process
from sqlite3 import Error
from tld import get_tld
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
results = []

headline = input("article headline here: ")
link = input("article link here: ")
domain = get_tld(link, as_object=True)
strOptions = []
strBase = []
matches = []

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
def convert1(lst): 
      
    return ' '.join(lst)
def convert(lst):
    str =  ''.join(lst) 
    return str

def sentiment_main(text):
    # Instantiates a client
    client = language_v1.LanguageServiceClient()
    # [END language_python_migration_client] 

    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Sends API Request to detect the sentiment of the text
    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment

    return(sentiment.score, sentiment.magnitude)
    # print("Text: {}".format(text))
    # print("Sentiment: {}, {}".format(sentiment.score, sentiment.magnitude))

def bias_main():
    database = r"sqlite\Databases\BiasDatabase\BiasDB.db"
    
    # create a database connection
    conn = create_connection(database)
    with conn:
        print(domain.fld + "'s bias is...")
        print(select_bias(conn))

def related_main():
    analyze_entities(headline)
    
    database = r"sqlite\Databases\ArticleDatabase\ArticleSQL.db"
    conn = create_connection(database)
    with conn:
        select_headlines(conn)
    isolate()

def report_main(input_):
    input = input_
    x = 0
    for i in input:
        x = x + 1
        tstring = str(i).replace("''", "''''")
        input.pop(x - 1)
        input.insert(x - 1, tstring)
    for i in input:
        # access database and search for headline
        database = r"sqlite\Databases\ArticleDatabase\ArticleSQL.db"
        conn = create_connection(database)
        with conn:
            select_source(conn, i)
        # return source in sourceAr
    for i in sourceAr:
        # access bias database and search domains for source/bias
        database = r"sqlite\Databases\BiasDatabase\BiasDB.db"
        conn = create_connection(database)
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
'''
    fArray = []
    fArray.append(left)
    fArray.append(leanLeft)
    fArray.append(center)
    fArray.append(leanRight)
    fArray.append(right)
    fArray.append(mixed)
    print("Coverage Report: " + str(fArray))
'''



def create_connection(db_file):

    # print("Creating Connection ...")
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
        return(row[0])

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
    # print(bcolors.OKGREEN + "I'm Done :D" + bcolors.ENDC)

def select_source(conn, headline):
    cur = conn.cursor()
    cur.execute("SELECT Provider FROM ArticleTest1 WHERE Headline LIKE ('%" + headline + "%')")
    rows = cur.fetchall()
    for row in rows:
        tempString = str(row)
        fString = tempString.replace('(','').replace('\'','').replace(',','').replace(')','')
        sourceAr.append(fString)

def find_bias(conn, domain_):
    cur = conn.cursor()
    cur.execute("SELECT BiasRating FROM BiasDB WHERE Domain LIKE ('%" + domain_ + "%')")
    rows = cur.fetchall()
    for row in rows:
        tempString = str(row)
        fString = tempString.replace('(','').replace('\'','').replace(',','').replace(')','')
        biasAr.append(fString)

def isolate():
    str2Match = ""
    base2Match = []

    for i in strBase:
        temp = i[0]
        base2Match.append(temp)
    
    str2Match = (convert1(base2Match))
    print("keywords: " + str2Match)
    Ratios = process.extract(str2Match,strOptions)
    matches = []
    for i in Ratios:
        if (i[1] >= 50):
            matches.append(i)
    highest = process.extractOne(str2Match,strOptions)

    '''
        f = open(r"TestingSaves\relatedArticle12.27.txt", "a")
        f.write("\nINPUT: " + str(input) + "\n")
        f.write("   MATCHES: " + str(matches))
        f.close()
    '''
    print(bcolors.HEADER + "HIGHEST:" + bcolors.ENDC , bcolors.OKCYAN + str(highest) + bcolors.ENDC)
    print(bcolors.HEADER + "MATCHES: " + bcolors.ENDC, bcolors.OKCYAN + str(matches) + bcolors.ENDC)
    for i in matches:
        results.append(i[0])

def analyze_entities(text_content):
    """
        Analyzing Entities from a String

        Args:
        text_content The text content to analyze
    """
    # Set connection to client as variable
    client = language_v1.LanguageServiceClient()

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
        
        # Loop over the mentions of entity from input document.
        for mention in entity.mentions:
            tempArray = []

            # append name of entity to tempArray
            tempArray.append(u"{}".format(mention.text.content))

            # Get mention type, e.g. PROPER for proper noun
            tempArray.append(u"{}".format(language_v1.EntityMention.Type(mention.type_).name))

            strBase.append(tempArray)
            # print(tempArray)
    # print(strBase)

if __name__ == '__main__':
    sentiment = sentiment_main(headline)
    print(sentiment)
    bias_main()
    related_main()
    report_main(results)