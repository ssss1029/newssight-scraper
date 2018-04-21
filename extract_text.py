
import sys
import csv
import os.path

from boilerpipe.extract import Extractor

from logger import log
from logger import err_log


def get_text(url):
    extractor = Extractor(extractor='ArticleExtractor', url=url)
    extracted_text = extractor.getText()
    return extracted_text


# If __main__: update the /articledata/ folder by going through articles in articles.csv
if __name__ == "__main__":
    if not os.path.isfile("articles.csv"):
        err_log("No articles.csv found. Exiting now.")
        sys.exit(0)
    
    with open("articles.csv", 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=' ', lineterminator='\n', quotechar='|', quoting=csv.QUOTE_ALL)
        next(reader) # Ignore the header line
        
        log("Beginning to go through everything in articles.csv")

        # Go through all of the articles
        for row in reader: 
            sourceId = row[0]
            articleId = row[1]
            author = row[2]
            title = row[3]
            description = row[4]
            url = row[5]
            urlToImage = row[6]
            publishedAt = row[7]
            article_data_file = 'articledata/{0}.txt'.format(articleId)

            # Do not try to make request for new data
            if os.path.isfile(article_data_file):
                continue

            # Put the article data at the top
            log("Scraping text from source: {0} AT {1}".format(sourceId, url))
            
            try:
                article_text = get_text(url)
                article_text = article_text.encode('ascii', 'ignore')
                with open(article_data_file, 'wb') as adf:
                    adf.write(str(row))
                    adf.write('\n')                    
                    adf.write(article_text)
            except Exception:
                err_log("Error with extracting text from {0}".format(url))                    

            

