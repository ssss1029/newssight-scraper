############################################
#### Main scraper for Newssight
#### v0.1
############################################

import time
import requests
import sys

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