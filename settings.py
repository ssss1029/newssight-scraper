###########################################
#### Settings used by Newssight Scraper
####
###########################################

import sys
import os

from logger import log
from logger import err_log

settings = {
	# See readme on how to make sure these are set properly	
	"IBM_WATSON_API_KEY" :  None,
	"NEWS_API_KEY" : None,

	# News API Stuff
	"source_request_endpoint" : lambda key: "https://newsapi.org/v2/sources?apiKey={0}&languagr=en&country=us".format(key),
	"top_headlines_from_source_endpoint" : lambda key, source: "https://newsapi.org/v2/top-headlines?sources={1}&apiKey={0}".format(key, source),

	# Newssight endpoints1
	"newssight_/" : "http://127.0.0.1:3000",
	"source_update_endpoint" : "/api/sources/batchUpdate",
	"source_list_endpoint" : "/api/sources/",
	"article_storage_endpoint" : "",

	# Query Timings.
	"timings" : {
		"NEWS_SOURCES" : 60, # Seconds
		"NEWS_ARTICLES_BATCH" : 120,
		"NEWS_ARTICLES_INDV_BUFFER" : 5
	}
}

def getSettings():
	"""
	Replaces all the 'None' entries in the settings object
	with values from either setup_environment.py or OS Environment variables.
	"""
	try: 
		# Try looking in the additional setup_environment script
		from setup_environment import getEnvironment
		environment = getEnvironment()
		for key, value in settings.items():
			if value == None:
				new_value = environment.get(key, None)
				if new_value == None:
					err_log("Environment variable {0} not found in setup_environment module")
				else:
					settings[key] = new_value
	except ImportError:
		# Try looking in the OS Environment
		for key, value in settings.items():
			if value == None:
				new_value = os.getenv(key, None)
				if new_value == None:
					err_log("Environment variable {0} not found in OS environment".format(key))
				else:
					settings[key] = new_value

	log("Got all settings. Environment variables were found.")

	return settings