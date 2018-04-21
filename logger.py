
import datetime

def log(string):
	now = str(datetime.datetime.now())
	print("[{0}] {1}".format(now, string))

def err_log(string, exception=None):
	now = str(datetime.datetime.now())	
	error_message = "[{0}] ==== ERROR ==== {1}".format(now, string)
	print(error_message)

	with open('err.log', 'a') as errlog:
		# Write the error message to error log
		# In the future, also write the traceback (if applicable)
		errlog.write(error_message)
		errlog.write("\n")
