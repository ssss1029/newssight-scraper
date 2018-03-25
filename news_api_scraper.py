############################################
#### News API scraper for Newssight
#### 
############################################

import requests

def getSources(settings):
	"""
	Gets all the sources
	"""
	query_url = settings["source_request_endpoint"](settings["NEWS_API_KEY"])
	r = requests.get(query_url)
	return r.json()