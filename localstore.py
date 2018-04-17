#######################################
## Handles storing data
##
## Currently uses CSV Files
#######################################

import csv
import os

article_store_columns = [
    "sourceId",
    "articleId",
    "author",
    "title",
    "description",
    "url",
    "urlToImage",
    "publishedAt"
]

def writeArticle(settings, article):
    filepath = settings["csv_article_store"]
    
    # Put titles in if the file does not exist
    if not os.path.isfile(filepath):
        with open(filepath, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=' ', lineterminator='\n', quotechar='|', quoting=csv.QUOTE_ALL)
            writer.writerow(article_store_columns)

    with open(filepath, 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ', quotechar='|', quoting=csv.QUOTE_ALL)
        row = []
        for col in article_store_columns:
            if article.get(col, None) == None:
                row.append("NOVALUE")
            else:
                row.append(' '.join(article.get(col, None).split()))
        row = [unicode(s).encode("utf-8") for s in row]
        writer.writerow(row)