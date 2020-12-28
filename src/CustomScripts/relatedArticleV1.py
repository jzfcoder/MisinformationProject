from google.cloud import language_v1
from fuzzywuzzy import process
from sqlite3 import Error
import sqlite3
import os
'''
    str2Match = "Top Intelligence Democrat accuses Russia of cyber hack that resulted in 'big haul'"
        "'Pretty clear' Russia behind SolarWinds hack, Pompeo says, becoming 1st US official to blame Moscow",
        "FBI scrambles to assess damage from Russia-linked US government hack",
        "Senator: Treasury Dept. email accounts compromised in hack"

    str2Match = "Fauci receives vaccine, has extreme confidence it's safe, effective"
        "These lawmakers are refusing COVID-19 vaccine until health care workers, seniors get it"
        "Biden receives first dose of COVID-19 vaccine, says nothing to worry about"
        "I would encourage the president to get a vaccine' for health, generating confidence"
        "Why 3 former presidents said they'd get the COVID vaccine on camera"
        "AOC defends decision to get vaccine amid criticism from fellow lawmakers, including teammate"

    str2Match = "Arizona GOP leaders' quarrel over election results could impact party's future"
        "Trump entertains desperate schemes to overturn election"
        "Barr says no reason for special counsels to investigate election, Hunter Biden, no basis for seize voting machines
        "Voting machine firm demands pro-Trump attorney retract bogus claims about 2020 election"
        "Pence urges conservatives 'to stay in the fight' as 'our election' continues"
        "EU greenlights COVID-19 vaccine after agency gives safety OK"
        "US close on deal with Pfizer for millions more vaccine doses"
        "Panel recommends Moderna vaccine, paving way for FDA authorization"
'''
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
def convert(lst): 
      
    return ' '.join(lst) 
strOptions = []
strBase = []

'''
    analyze_entities using Google Cloud Language API

'''
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
        
        print(entity.name)
        # Get salience score in [0, 1.0] range
        print(u"Salience score: {}".format(entity.salience))
        
        # Loop over the mentions of entity from input document.
        for mention in entity.mentions:
            tempArray = []

            # append name of entity to tempArray
            tempArray.append(u"{}".format(mention.text.content))

            # Get mention type, e.g. PROPER for proper noun
            tempArray.append(u"{}".format(language_v1.EntityMention.Type(mention.type_).name))

            strBase.append(tempArray)
            # print(tempArray)
    print(strBase)

'''
    str2Match = "Top Intelligence Democrat accuses Russia of cyber hack that resulted in big haul"
    "Top Intelligence Democrat accuses Russia of cyber hack that resulted in 'big haul'",
    "'Pretty clear' Russia behind SolarWinds hack, Pompeo says, becoming 1st US official to blame Moscow",
    "FBI scrambles to assess damage from Russia-linked US government hack",
    "Senator: Treasury Dept. email accounts compromised in hack"
    ]
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
    cur.execute("SELECT Headline FROM ArticleTest1")
    rows = cur.fetchall()
    for row in rows:
        strOptions.append(row[0])
    print(bcolors.OKGREEN + "I'm Done :D" + bcolors.ENDC)
def isolate():
    str2m=Match = ""
    base2Match = []

    for i in strBase:
        temp = i[0]
        base2Match.append(temp)
    
    str2Match = (convert(base2Match))
    print(str2Match)
    Ratios = process.extract(str2Match,strOptions)
    matches = []
    for i in Ratios:
        if (i[1] >= 50):
            matches.append(i)
    highest = process.extractOne(str2Match,strOptions)

    f = open(r"TestingSaves\relatedArticle12.27.txt", "a")
    f.write("\nINPUT: " + str(input) + "\n")
    f.write("   MATCHES: " + str(matches))
    f.close()
    print(bcolors.HEADER + "HIGHEST:" + bcolors.ENDC , bcolors.OKCYAN + str(highest) + bcolors.ENDC)
    print(bcolors.HEADER + "MATCHES: " + bcolors.ENDC, bcolors.OKCYAN + str(matches) + bcolors.ENDC)
def fuzzy_main():
    database = r"C:\Users\timfl\Documents\GitHub\MisinformationProject\sqlite\Databases\ArticleDatabase\ArticleSQL.db"
    conn = create_connection(database)
    with conn:
        select_headlines(conn)
    isolate()

'''
    call main, kickoff functions
    grab user input
'''
if __name__ == "__main__":
    input = input("text here: ")
    analyze_entities(input)
    fuzzy_main()