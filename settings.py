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
	"IBM_WATSON_API_KEY" :  None,
	"NEWS_API_KEY" : None,

}

def getSettings():
	try: 
		# Try looking in the additional setup_environment script
		from setup_environment import getEnvironment
		environment = getEnvironment()
		for key, value in settings.iteritems():
			if value == None:
				new_value = environment.get(key, None)
				if new_value == None:
					err_log("Environment variable {0} not found in setup_environment module")
				else:
					settings[key] = new_value
	except ImportError:
		# Try looking in the OS Environment
		for key, value in settings.iteritems():
			if value == None:
				new_value = os.getenv(key, None)
				if new_value == None:
					err_log("Environment variable {0} not found in OS environment".format(key))
				else:
					settings[key] = new_value

	log("Got all settings. Environment variables were found.")

	return settings