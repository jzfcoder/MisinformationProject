from google.oauth2 import service_account
from google.cloud import language_v1
from fuzzywuzzy import process
from sqlite3 import Error
from tld import get_tld
import sqlite3
import os


def convert1(lst):

    return ' '.join(lst)
def convert(lst):
    str = ''.join(lst)
    return str

def convert_array(array):
    track = 0
    for x in array:
        x = x.replace("\'\'\'\'", "\'")
        array.pop(track)
        array.insert(track, x)
        print(x)
        track = track + 1
    print(array)
    return array

'''
    finds bias from article url
    takes domain from input url and searches database for domain's relative organization and bias
    args:
        link: link is the article url
    return: bias string
'''
def get_bias(link):
    domain_ = get_tld(link, as_object=True)
    database = r"sqlite\Databases\MainDatabase\MainDatabase.db"

    # create a database connection
    conn = create_connection(database)
    # with conn:
    return (select_bias(conn, domain_))

'''
    gets sentiment of text using google cloud language api
    args:
        text: text to analyze
    returns: sentiment score of given text
'''
def get_sentiment(text):
    credentials = service_account.Credentials.from_service_account_file(
        r"C:\Users\timfl\Documents\GoogleCloudKeys\MyFirstProject-e85779938beb.json")
    # Instantiates a client
    client = language_v1.LanguageServiceClient(credentials=credentials)
    # [END language_python_migration_client]

    document = language_v1.Document(
        content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Sends API Request to detect the sentiment of the text
    sentiment = client.analyze_sentiment(
        request={'document': document}).document_sentiment

    return(sentiment.score)
    # print("Text: {}".format(text))
    # print("Sentiment: {}, {}".format(sentiment.score, sentiment.magnitude))

'''
    uses entity analysis and fuzzy matching to find related articles.
    takes input headline, finds keywords, and searches database for headlines with high scoring fuzzy match
    using the levenshtein distance
    args:
        headline: original article headline
    return: array of related article headlines
'''
def get_related(headline):
    database = r"sqlite\Databases\MainDatabase\MainDatabase.db"
    conn = create_connection(database)
    with conn:
        return isolate(analyze_entities(headline), select_headlines(conn))

'''
    coverage report of who is reporting a topic on a political spectrum
    uses input array of related articles to query each article's bias
    args:
        related: array of related articles in a topic
    return: compiled list of # of times each part of the political spectrum has reported the story.
'''
def get_coverage(related):
    input = related
    print(input)
    x = 0
    biasAr = []
    sourceAr = []
    for i in input:
        x = x + 1
        tstring = str(i).replace("''", "''''")
        input.pop(x - 1)
        input.insert(x - 1, tstring)

    for i in input:
        # access database and search for headline
        database = r"sqlite\Databases\MainDatabase\MainDatabase.db"
        conn = create_connection(database)
        with conn:
            sourceAr.append(select_source(conn, i))
        # return source in sourceAr

    for i in sourceAr:
        # access bias database and search domains for source/bias
        database = r"sqlite\Databases\MainDatabase\MainDatabase.db"
        conn = create_connection(database)
        with conn:
            tempi = convert1(i)
            print(tempi)
            biasAr.append(find_bias(conn, tempi))
        # search bias db for bias type
        # add 1 to int var of any bias

    y = 0
    for i in biasAr:
        y = y + 1
        tstring = str(i).replace("[", "").replace("]", "").replace("\'", "")
        biasAr.pop(y - 1)
        biasAr.insert(y - 1, tstring)

    print(biasAr)

    left = biasAr.count("Left")
    leanLeft = biasAr.count("Lean Left")
    center = biasAr.count("Center")
    leanRight = biasAr.count("Lean Right")
    right = biasAr.count("Right")
    mixed = biasAr.count("Mixed")

    finArray = [left, leanLeft, center, leanRight, right, mixed]
    return finArray

'''
    create score using report, sentiment, and bias
    args:
        report: coverage report array
        sentiment: headline sentiment
        bias: article source bias
'''
def get_score(report, sentiment, bias):
    sum = 0
    left = 0
    right = 0
    center = 0
    difference = 0
    it = 0

    reportFin = 0
    sentFin = 0
    biasFin = 0

    for i in report:
        sum = sum + i
    
    for i in report:
        it = it + 1
        if (it <= 2):
            left = left + i
        if (it > 3):
            right = right + i
            
        if (it == 3):
            center = i
            left = left + center
            right = right + center  

    if (left > right):
        difference = left - right
    if (right > left):
        difference = right - left
    if (right == left):
        return 10

    reportRes = sum - difference
    reportQuot = reportRes/sum
    reportFin = reportQuot*10

    sentAbs = abs(sentiment)
    revSent = 1 - sentAbs
    sentFin = 10*revSent

    if (bias == "Left"):
        biasFin = 1
    if (bias == "Lean Left"):
        biasFin = 5
    if (bias == "Center"):
        biasFin = 10
    if (bias == "Lean Right"):
        biasFin = 5
    if (bias == "Right"):
        biasFin = 1

    sentFin = round(sentFin)
    reportFinn = reportFin*0.25
    sentFinn = sentFin*0.35
    biasFinn = biasFin*0.4

    fin = reportFinn + sentFinn + biasFinn

    return fin



'''
    Used to find sources relative to each article in related articles input
    Query using SQL in ArticleDB
    Args:
        conn: Connections to Database
        headline: Headline in for loop of related articles
    Return: Array of domains of each article 
'''
def select_source(conn, headline):
    sourceArray = []
    cur = conn.cursor()
    cur.execute(
        "SELECT Provider FROM ArticleTable WHERE Headline LIKE ('%" + headline + "%')")
    rows = cur.fetchall()
    for row in rows:
        tempString = str(row)
        fString = tempString.replace('(', '').replace('\'', '').replace(
            ',', '').replace(')', '').replace("''", '')
        sourceArray.append(fString)
    return sourceArray

'''
    Used to find bias from domains returned by select_source
    Query using SQL in BiasTable
    Args:
        conn: Connections to Database
        domain_: Domain in for loop of bias
    Return: Array of left, right, center strings directly from BiasTable database
'''
def find_bias(conn, domain_):
    biasArray = []
    cur = conn.cursor()
    cur.execute(
        "SELECT BiasRating FROM BiasTable WHERE Domain LIKE ('%" + domain_ + "%')")
    rows = cur.fetchall()
    for row in rows:
        tempString = str(row)
        fString = tempString.replace('(', '').replace(
            '\'', '').replace(',', '').replace(')', '')
        biasArray.append(fString)
    return biasArray

'''
    Used to return bias from given domain
    Query using SQL in BiasTable
    Args:
        conn: Connections to Database
        domain: Domain in for bias
    Return: Bias
'''
def select_bias(conn, domain):
    """
    Query all rows in the tasks table
    :param conn: the Connection object
    :return:
    """
    cur = conn.cursor()
    cur.execute(
        "SELECT BiasRating FROM BiasTable WHERE Domain like '%" + domain.fld + "%' ")

    rows = cur.fetchall()

    for row in rows:
        return(row[0])

'''
    Used to isolate/reduce related articles given from entity analysis and selected headlines
    Uses fuzzy matching to find all related articles from given entities
    Args:
        strBase: what to match against; matching base
        strOptions: options to match against
    Return: array of all related articles from given args
'''
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

    '''
        f = open(r"TestingSaves\relatedArticle12.27.txt", "a")
        f.write("\nINPUT: " + str(input) + "\n")
        f.write("   MATCHES: " + str(matches))
        f.close()
    '''
    results = []
    # print(bcolors.HEADER + "HIGHEST:" + bcolors.ENDC , bcolors.OKCYAN + str(highest) + bcolors.ENDC)
    # print(bcolors.HEADER + "MATCHES: " + bcolors.ENDC, bcolors.OKCYAN + str(matches) + bcolors.ENDC)
    for i in matches:
        results.append(i[0])
    return results

'''
    analyzes text for entities using google cloud language API
    can also return salience score
    args:
        text_content: text to analyze, generally input headline
    return: array of entities found in text_content
'''
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

'''
    create a database connection to the specified SQLite database
    args:
        db_file: database name
    return: connection object or none
'''
def create_connection(db_file):

    # print("Creating Connection ...")

    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn

'''
    select all headlines using SQL from Article Database
    used for related articles search
    args:
        conn: connection to database
    return: headlines in array
'''
def select_headlines(conn):
    """
        Query all rows in the tasks table
        :param conn: the Connection object
        :return:
    """
    strOptions = []
    cur = conn.cursor()
    cur.execute("SELECT Headline FROM ArticleTable")
    rows = cur.fetchall()
    for row in rows:
        strOptions.append(row[0])
    # print(bcolors.OKGREEN + "I'm Done :D" + bcolors.ENDC)
    return strOptions
