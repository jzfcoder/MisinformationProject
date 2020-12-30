# MisinformationProject

### OVERVIEW:
This coding project tackles a portion of online misinformation using a variety of methods. It provides a sentiment analysis of the headline, and returns an article source's political bias (from allsides.com). This program also provides related articles to widen a consumer's perspective and a coverage report for a viewer to see who is reporting certain issues.

##### TECHNOLOGIES:
This project utilizes the following libraries and APIs:
- SQLite (https://sqlite.com/docs.html)
- Fuzzy Wuzzy (https://pypi.org/project/fuzzywuzzy/)
    - Additional URLS: 
    - https://www.datacamp.com/community/tutorials/fuzzy-string-python
    - https://en.wikipedia.org/wiki/Levenshtein_distance
- Google Cloud Natural Language
    - Text Sentiment and entities function
    - https://cloud.google.com/natural-language/docs/analyzing-entities
    - https://cloud.google.com/natural-language/docs/analyzing-sentiment
- tld (https://pypi.org/project/tld/)

##### CREDENTIAL KEY:
```shell
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\Users\timfl\Documents\GoogleCloudKeys\MyFirstProject-e85779938beb.json"                
```
##### CREATE SQLite DATABASE:
Run sqlite3 from powershell!!!
```shell
 .\sqlite3.exe
.mode csv
sqlite> .import C:\\Path\\To\\CSV\\File\\Sample.csv Articles
sqlite> .schema Articles
CREATE TABLE Articles(
  "url" TEXT,
  "Headline" TEXT,
  "Headline2" TEXT,
  "Author" TEXT,
  "Provider" TEXT,
  "Date" TEXT,
  "Content" TEXT,
  "Keywords" TEXT
);
sqlite> .save ArticleSQL.db
sqlite>
```

##### REMOVE SINGLE QUOTES:           

```sql
UPDATE 
    ArticleTest1
SET 
    Headline = REPLACE(Headline,'''','''''')
WHERE 
    Headline LIKE '%''%'

COMMIT;
```