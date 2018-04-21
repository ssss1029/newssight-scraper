import argparse
import os
import sys
import json
import six
import math
import csv 

from logger import log
from logger import err_log

from google.cloud import language
from google.cloud.language import enums
from google.cloud.language import types

# entity types from enums.Entity.Type
entity_type = ('UNKNOWN', 'PERSON', 'LOCATION', 'ORGANIZATION',
                'EVENT', 'WORK_OF_ART', 'CONSUMER_GOOD', 'OTHER')

def entities_text(text):
    """Detects entities in the text."""

    client = language.LanguageServiceClient()

    if isinstance(text, six.binary_type):
        text = text.decode('utf-8')

    # Instantiates a plain text document.
    document = types.Document(
        content=text,
        type=enums.Document.Type.PLAIN_TEXT)

    # Detects entities in the document. You can also analyze HTML with:
    #   document.type == enums.Document.Type.HTML
    entities = client.analyze_entities(document).entities

    """ 
    for entity in entities:
        print('=' * 20)
        print(u'{:<16}: {}'.format('name', entity.name))
        print(u'{:<16}: {}'.format('type', entity_type[entity.type]))
        print(u'{:<16}: {}'.format('metadata', str(list(entity.metadata.iterkeys()))))
        print(u'{:<16}: {}'.format('salience', entity.salience))
        print(u'{:<16}: {}'.format('wikipedia_url', entity.metadata.get('wikipedia_url', '-').encode('ascii', 'ignore')))
        print(u'{:<16}: {}'.format('mid', entity.metadata.get('mid', '-').encode('ascii', 'ignore')))
    """

    return entities

# If __main__, lookat every article in the /articledata directory and make sure there is a corresponding
# file in the /entityanalysis directory
if __name__ == "__main__":
    total_words_used = 0
    current_article_id = 0
    current_article_data = "articledata/{0}.txt".format(current_article_id)
    current_entity_data  = "entityanalysis/{0}.csv".format(current_article_id)
    while os.path.isfile(current_article_data):
        if os.path.isfile(current_entity_data):
            current_article_id = current_article_id + 1
            current_article_data = "articledata/{0}.txt".format(current_article_id)
            current_entity_data  = "entityanalysis/{0}.csv".format(current_article_id)
            continue

        log("Getting article data from: {0}".format(current_article_data))
        with open(current_article_data, 'r') as artdata:
            next(artdata)
            article_lines = []
            for line in artdata:
                article_lines.append(line)
            article = reduce(lambda x, y: x + "\n" + y, article_lines)
            entities = entities_text(article)
            log("Article is {0} characters long.".format(len(article)))
            total_words_used += math.ceil(len(article) / 1000.0) * 1000 # Round to the nearest 1000

            with open(current_entity_data, 'wb') as entdata:
                writer = csv.writer(entdata, delimiter=' ', lineterminator='\n', quotechar='|', quoting=csv.QUOTE_ALL)
                for entity in entities:
                    row = [
                        entity.name,
                        entity_type[entity.type],
                        entity.salience,
                        entity.metadata.get('wikipedia_url', '-').encode('ascii', 'ignore'),
                        entity.metadata.get('mid', '-').encode('ascii', 'ignore')
                    ]

                    for metakey in entity.metadata.iterkeys():
                        if metakey != "wikipedia_url" and metakey != "mid":
                            row.append(entity.metadata.get(metakey, '-').encode('ascii', 'ignore'))
                    
                    writer.writerow(row)

        # Go to the next article even if the with() fails
        current_article_id = current_article_id + 1
        current_article_data = "articledata/{0}.txt".format(current_article_id)
        current_entity_data  = "entityanalysis/{0}.csv".format(current_article_id)
        

    sys.exit(0)