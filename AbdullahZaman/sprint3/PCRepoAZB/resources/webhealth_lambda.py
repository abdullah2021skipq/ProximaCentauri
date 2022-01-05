import datetime
import urllib3
import constants as constants
from cloudwatch_putMetric import CloudWatchPutMetric
import s3bucket

def lambda_handler(events, context):
	
	URL_list = s3bucket.read_file("abdullahzamanbucket", "urlsList.json")
	values = dict()
	cw = CloudWatchPutMetric()
	
	for Url in URL_list:
		avail = get_availability(Url)
		dimensions = [
			{"Name": "URL", "Value": Url}
			]
		
		cw.put_data(constants.URL_MONITOR_NAMESPACE,constants.URL_MONITOR_NAME_Availability+"_"+Url, dimensions, avail)
		
		latency = get_latency(Url)
		dimensions = [
			{"Name": "URL", "Value": Url}
			]
		
		cw.put_data(constants.URL_MONITOR_NAMESPACE,constants.URL_MONITOR_NAME_Latency+"_"+Url, dimensions, latency)
		
		values.update({"availability":avail,"Latency":latency})
	return values

def get_availability(Url):
	http = urllib3.PoolManager()
	response = http.request("GET", Url)
	if response.status==200:
		return 1.0
	else:
		return 0.0

def get_latency(Url):
	http = urllib3.PoolManager()
	start = datetime.datetime.now()
	response = http.request("GET", Url)
	end = datetime.datetime.now()
	delta = end - start
	latencySec = round(delta.microseconds * .000001, 6)
	return latencySec