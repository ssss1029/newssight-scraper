
import datetime

def log(string):
	now = str(datetime.datetime.now())
	print("[{0}] {1}".format(now, string))

def err_log(string):
	now = str(datetime.datetime.now())
	print("[{0}] ==== ERROR ====> {1}".format(string))