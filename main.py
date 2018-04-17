############################################
#### Main scraper for Newssight
#### v0.1
############################################

import time
import requests
from logger import log 
from logger import err_log

from settings import getSettings
from news_api_scraper import getSources
from news_api_scraper import getArticles

settings = getSettings()

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

	# Query News API for articles for each source
	for source in supported_sources:
		response = getArticles(settings, source["id"])
		# Check if the response is ok
		if response["status"] == "ok":
			log("Got articles from {0}".format(source["id"]))
		else:
			err_log("Error getting articles from {0}".format(["id"]))
			err_log(response)

		articles = response["articles"]

		for article in articles:
			log(article)
			break
		
		break
		# For each article, extract text with boilerpipe, send extracted text to analysis, send everything to app



	time.sleep(5)