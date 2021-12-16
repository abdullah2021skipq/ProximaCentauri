import datetime
import urllib3
import constants as constants
from cloudwatch_putMetric import cloudwatchPutMetric

def lambda_handler(events, context):
    values=dict()
    cw = cloudwatchPutMetric()
    
    avail=get_availability()
    dimensions=[
        {"Name": "URL", "Value":constants.URL_TO_MONITOR},
        {"Name": "Region", "Value":"DUB"}
    ]
    cw.put_data(constants.URL_MONITOR_NAMESPACE, constants.URL_MONITOR_NAME_AVAILABILITY, dimensions, avail)
    
    latency=get_latency()
    cw.put_data(constants.URL_MONITOR_NAMESPACE, constants.URL_MONITOR_NAME_LATENCY, dimensions, latency)
    
    values.update({"availability": avail, "latency": latency})
    return values

def get_availability():
    http=urllib3.PoolManager()
    response=http.request("GET", constants.URL_TO_MONITOR)
    if response.status==200:
        return 1.0
    else:
        return 0.0
    

def get_latency():
    http=urllib3.PoolManager()
    start=datetime.datetime.now()
    response=http.request("GET", constants.URL_TO_MONITOR)
    end=datetime.datetime.now()
    delta=end-start
    latencySec=round(delta.microseconds * 0.000001, 6)
    return latencySec
    
    