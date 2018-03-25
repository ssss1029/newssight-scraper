###########################################
#### Settings used by Newssight Scraper
####
#### Make sure the following environment variables are defined:
#### - NEWS_API_KEY
#### - IBM_WATSON_API_KEY
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

	# Newssight endpoints
	"newssight_/" : "http://127.0.0.1:3000",
	"source_update_endpoint" : "/api/sources/batchUpdate"
}

def getSettings():
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