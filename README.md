These aren the API scraping scripts to make Newssight work

# Building and Running
```
$ git clone git@github.com:ssss1029/newssight-scraper.git
$ cd python-boilerpipe
$ git submodule init
$ git submodule update
```
or
```
$ git clone --recurse-submodules git@github.com:ssss1029/newssight-scraper.git	
```

Create a virtualenv
```
$ virtualenv env
```

```
$ cd python-boilerpipe
$ pip install -r requirements.txt
$ python setup.py install
```

Make sure `JAVA_HOME` is set properly and Python & Java are both either 32 or 64 bit.

# Text Extraction
Text extraction done using boilerpipe.
See https://www.l3s.de/~kohlschuetter/publications/wsdm187-kohlschuetter.pdf for more information. "Boilerplate Detection using Shallow Text Features" by Christian Kohlschütter, Peter Fankhauser, Wolfgang Nejdl

# Settings
Most of the required settings are in `settings.py`. However, API Keys are missing. There are two ways to fix this.
 - Add a new file called `setup_environment.py` next to `main`. Fill it with the following contents:
 ```python
###########################################
#### Sets up the run environment for these modules
####
###########################################

variables = {
	"NEWS_API_KEY" : "<Your Key Here>"
	"IBM_WATSON_API_KEY" : "<Your Key Here>"
}

def getEnvironment():
	return variables
 ```
  - Add the appropriate environment variables so they can be accessed by `os.getenv()`. Use the same key/value pairs as the above code indicates.

  