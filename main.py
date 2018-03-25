############################################
#### Main scraper for Newssight
#### v0.1
############################################

import time
import requests

from settings import getSettings
from news_api_scraper import getSources
from logger import log 
from logger import err_log

settings = getSettings()	

while 1:
	log("Querying NEWS API")
	sources_json = getSources(settings)
	log("Recieved sources from NEWS API. Type = " + str(type(sources_json)))

	res = requests.post(settings["newssight_/"] + settings["source_update_endpoint"], json={
			"sources" : sources_json["sources"]
		});	
	log("Sent request to Newssight. Status code = {0}, content = {1}".format(res.status_code, res.content))

	time.sleep(5)