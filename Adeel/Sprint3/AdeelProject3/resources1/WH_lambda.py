
import datetime
import urllib3
import constants1 as constants
from cloudwatchm import cloudWatchPutMetric
from bucket import Bucket as bo   

def lambda_handler(events, context):
    
     ############################## Accessing S3 bucket links in list ###############################
    
    cw = cloudWatchPutMetric();
    Url_Monitor= bo(Bucket = 'adeelskipq', key = 'urls.json').bucket_as_list()
    print(Url_Monitor)
    
    
     ############################## Availabiity matrix ###############################
    
    values = dict()
    four_url_values  = []
    a = 1
    for url in Url_Monitor:
        avail = get_availability(url)
        dimensions=[
        {'Name': 'URL', 'Value': url}
        ]
        cw.put_data(constants.URL_MONITOR_NAMESPACE , constants.URL_MONITOR_NAME_AVAILABILITY+'_'+url+ str(a),dimensions,avail)
    
    
     ############################## Latency matrix ###############################
    
        latency = get_latency(url)
        dimensions=[
        {'Name': 'URL', 'Value': url}
        ]
        cw.put_data(constants.URL_MONITOR_NAMESPACE, constants.URL_MONITOR_NAME_LATENCY+'_'+url+ str(a),dimensions,latency)
        
        a+=1
    
        values.update({"avaiability":avail, "Latency":latency})
        four_url_values.append(values)
    return four_url_values
    
     ############################## Availability function ###############################
    
def get_availability(url):
    http = urllib3.PoolManager()
    response = http.request("GET", url)
    if response.status==200:
        return 1.0
    else: 
        return 0.0

 ############################## Latency function ###############################
    
def get_latency(url):
    http = urllib3.PoolManager()        # Creating a PoolManager instance for sending requests.
    start = datetime.datetime.now()
    response = http.request("GET", url) #  Sending a GET request and getting back response as HTTPResponse object.
    end = datetime.datetime.now()       # check time after getting the website contents
    delta = end - start                 #take time difference
    latencySec = round(delta.microseconds * .000001, 6) 
    return latencySec