# MisinformationProject
 
+------------------------------------------------------------------------------------------------------------------------------------------+
|CREDENTIAL KEY                                                                                                                            |
|$env:GOOGLE_APPLICATION_CREDENTIALS="C:\Users\timfl\Documents\GoogleCloudKeys\MyFirstProject-e85779938beb.json"                           |
+------------------------------------------------------------------------------------------------------------------------------------------+

+------------------------------------------------------------------------------------------------------------------------------------------+
|CREATE SQLite DATABASE                                                                                                                    |
+------------------------------------------------------------------------------------------------------------------------------------------+

RUN sqlite3 from powershell!!!
 .\sqlite3.exe
.mode csv
sqlite> .import C:\\Users\\timfl\\Documents\\GitHub\\MisinformationProject\\sqlite\\Databases\\ArticleDatabase\\ArticleDb.csv Articles
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

+------------------------------------------------------------------------------------------------------------------------------------------+
|REMOVE SINGLE QUOTES                                                                                                                      |
+------------------------------------------------------------------------------------------------------------------------------------------+

UPDATE 
    ArticleTest1
SET 
    Headline = REPLACE(Headline,'''','''''')
WHERE 
    Headline LIKE '%''%'

COMMIT;