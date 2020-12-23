from google.cloud import language_v1
# https://cloud.google.com/natural-language/docs/analyzing-entities

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
        print(u"Representative name for the entity: {}".format(entity.name))

        # Get entity type (PERSON, LOCATION, ADDRESS, NUMBER, etc)
        print(u"Entity type: {}".format(language_v1.Entity.Type(entity.type_).name))

        # Get salience score in [0, 1.0] range
        print(u"Salience score: {}".format(entity.salience))

        
        # Loop over the metadata associated with entity.  
        '''
            Many known entities have a wiki (wikipedia_url) and Knowledge Graph MID (mid)/
            (Knowledge Graph is used by google to show widgets of condensed info from multiple sources)

            Some entity types may also have additional metadata
            e.g. ADDRESS entities may have metadata for the address street_name, postal_code, etc
        '''      
        for metadata_name, metadata_value in entity.metadata.items():
            print(u"{}: {}".format(metadata_name, metadata_value))
        
        # Loop over the mentions of entity from input document.
        '''
            API also supports proper noun mentions.
            # of appearances in given text will affect an entity's salience score.
        '''
        for mention in entity.mentions:
            print(u"Mention text: {}".format(mention.text.content))

            # Get mention type, e.g. PROPER for proper noun
            print(
                u"Mention type: {}".format(language_v1.EntityMention.Type(mention.type_).name)
            )

    # outputs the language, useful if language needs to be automatically detected.
    print(u"Language of the text: {}".format(response.language))

if __name__ == "__main__":                                                                        
    input = input("text here: ")
    analyze_entities(input)