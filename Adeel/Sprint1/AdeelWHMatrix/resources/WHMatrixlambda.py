
import datetime
import urllib3
import constants as constants
from cloudwatchM import cloudWatchPutMetric

def lambda_handler(events, context):
    values = dict()
    cw = cloudWatchPutMetric();
    
    avail = get_availability()
    dimensions=[
        {'Name': 'URL', 'Value': constants.URL_TO_MONITOR},
        {'Name':'Region', 'Value':'DUB'}
    ]
    cw.put_data(constants.URL_MONITOR_NAMESPACE, constants.URL_MONITOR_NAME_AVAILABILITY,dimensions,avail)
    
    
    latency = get_latency()
    dimensions=[
        {'Name': 'URL', 'Value': constants.URL_TO_MONITOR},
        {'Name':'Region', 'Value':'DUB'}
    ]
    cw.put_data(constants.URL_MONITOR_NAMESPACE, constants.URL_MONITOR_NAME_LATENCY,dimensions,latency)
    
    values.update({"avaiability":avail, "Latency":latency})
    return values
    
def get_availability():
    http = urllib3.PoolManager()
    response = http.request("GET", constants.URL_TO_MONITOR)
    if response.status==200:
        return 1.0
    else: 
        return 0.0

    
def get_latency():
    http = urllib3.PoolManager()        # Creating a PoolManager instance for sending requests.
    start = datetime.datetime.now()
    response = http.request("GET", constants.URL_TO_MONITOR) #  Sending a GET request and getting back response as HTTPResponse object.
    end = datetime.datetime.now()       # check time after getting the website contents
    delta = end - start                 #take time difference
    latencySec = round(delta.microseconds * .000001, 6) 
    return latencySec