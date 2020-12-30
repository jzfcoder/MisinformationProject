# MisinformationProject

+-------------------------------------------------------------------------------------------------------------------------------+
|OVERVIEW:                                                                                                                      |
|This coding project tackles a portion of online misinformation using a variety of methods. It provides a sentiment analysis of |
|the headline, and returns an article source's political bias (from allsides.com). This program also provides related articles  |
|to widen a consumer's perspective and a coverage report for a viewer to see who is reporting certain issues.                   |
+-------------------------------------------------------------------------------------------------------------------------------+

+-------------------------------------------------------------------------------------------------------------------------------+
|TECHNOLOGIES:                                                                                                                  |
|This project utilizes the following libraries and APIs:                                                                        |
| - SQLite                                                                                                                      |
| - Fuzzy Wuzzy                                                                                                                 |
| - Google Cloud Natural Language                                                                                               |
| - tld python library                                                                                                          |
+-------------------------------------------------------------------------------------------------------------------------------+

+-------------------------------------------------------------------------------------------------------------------------------+
|CREDENTIAL KEY:                                                                                                                |
|$env:GOOGLE_APPLICATION_CREDENTIALS="C:\Users\timfl\Documents\GoogleCloudKeys\MyFirstProject-e85779938beb.json"                |
+-------------------------------------------------------------------------------------------------------------------------------+

+-------------------------------------------------------------------------------------------------------------------------------+
|CREATE SQLite DATABASE:                                                                                                        |
+-------------------------------------------------------------------------------------------------------------------------------+
RUN sqlite3 from powershell!!!
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

+-------------------------------------------------------------------------------------------------------------------------------+
|REMOVE SINGLE QUOTES:                                                                                                          |
+-------------------------------------------------------------------------------------------------------------------------------+

UPDATE 
    ArticleTest1
SET 
    Headline = REPLACE(Headline,'''','''''')
WHERE 
    Headline LIKE '%''%'

COMMIT;