# MisinformationProject
 
RUN sqlite3 from powershell!!!
$env:GOOGLE_APPLICATION_CREDENTIALS="C:\Users\timfl\Documents\GoogleCloudKeys\MyFirstProject-e85779938beb.json"

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