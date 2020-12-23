from google.cloud import language_v1

def main():
    
    # Instantiates a client
    client = language_v1.LanguageServiceClient()
    # [END language_python_migration_client]

    # The text to analyze
    text = input("Type this here: ")
    # text = 

    document = language_v1.Document(content=text, type_=language_v1.Document.Type.PLAIN_TEXT)

    # Detects the sentiment of the text
    sentiment = client.analyze_sentiment(request={'document': document}).document_sentiment

    print("Text: {}".format(text))
    print("Sentiment: {}, {}".format(sentiment.score, sentiment.magnitude))
    # [END language_quickstart]

if __name__ == "__main__":
    main()