############################################
#### Main scraper for Newssight
#### v0.1
############################################

import time
import requests
import sys
import csv

from logger import log 
from logger import err_log
from settings import getSettings
from news_api_scraper import getSources
from news_api_scraper import getArticles
from localstore import get_article_id
from localstore import writeArticle

settings = getSettings()

# Sources we will use.
wanted_sources = [
	'abc-news',
	'associated-press',
	'bleacher-report',
	'bloomberg',
	'breitbart-news',
	'cbs-news',
	'cnbc',
	'cnn',
	'fox-news',
	'national-geographic',
	'nbc-news',
	'techcrunch',
	'the-huffington-post',
	'the-new-york-times',
	'the-verge',
	'the-washington-post',
	'time'
]

while 1:
	
	# Get sources from News API
	sources_json = getSources(settings)
	
	with open("sources.csv", "wb") as sourcescsv:
		writer = csv.writer(sourcescsv, delimiter=',', lineterminator='\n', quotechar='"', quoting=csv.QUOTE_ALL)
		for source in sources_json["sources"]:
			row = [source["id"], source["name"], source["description"],  source["url"],  source["category"],  source["country"],  source["language"], 0, 0, 0]
			row = [unicode(s).encode("utf-8") for s in row]
			writer.writerow(row)
	sys.exit(0)

	# Send sources to app
	res = requests.post(settings["newssight_/"] + settings["source_update_endpoint"], json={
			"sources" : sources_json["sources"]
		})
	
	log("Sent sources {0}".format(res))

	# Get sources from app
	res = requests.post(settings["newssight_/"] + settings["source_list_endpoint"])
	supported_sources = res.json()
	
	id_to_data = dict()

	for source in supported_sources:
		id_to_data[source["id"]] = source

	# Query News API for articles for each source
	for source_id in wanted_sources:
		response = getArticles(settings, id_to_data[source_id]["id"])
		# Check if the response is ok
		if response["status"] == "ok":
			log("Got articles from {0}".format(id_to_data[source_id]["id"]))
		else:
			err_log("Error getting articles from {0}".format(id_to_data[source_id]["id"]))
			err_log(response)

		articles = response["articles"]

		# Add all the articles from the given source into the database
		for article in articles:
			get_article_id(article)
			writeArticle(settings, article)

	sys.exit(0)