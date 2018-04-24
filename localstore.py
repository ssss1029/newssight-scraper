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

# Global non-static variable. 
# Bad design, but will change later.
# Use object, since python 2.7 does not support nonlocal
next_article_id = { 'id' : 0 }

def get_article_id(article):
    curr = next_article_id['id']
    next_article_id['id'] = next_article_id['id'] + 1
    article['id'] = curr
    return article

def writeArticle(settings, article):
    filepath = settings["csv_article_store"]
    
    # Put titles in if the file does not exist
    if not os.path.isfile(filepath):
        with open(filepath, 'wb') as csvfile:
            writer = csv.writer(csvfile, delimiter=' ', lineterminator='\n', quotechar='|', quoting=csv.QUOTE_ALL)
            writer.writerow(article_store_columns)

    with open(filepath, 'a') as csvfile:
        writer = csv.writer(csvfile, delimiter=' ', lineterminator='\n', quotechar='|', quoting=csv.QUOTE_ALL)
        row = []
        for col in article_store_columns:
            if article.get(col, None) != None and row.append(' '.join(article.get(col, None).split())) != "":
                row.append(' '.join(article.get(col, None).split()))
            elif col == "sourceId" and row.append(article["source"]["id"]) != "":
                row.append(article["source"]["id"])
            elif col == "articleId" and row.append(article['id']) != "":
                row.append(article['id'])              
            else:
                row.append("NOVALUE")
        row = [unicode(s).encode("utf-8") for s in row]
        writer.writerow(row)