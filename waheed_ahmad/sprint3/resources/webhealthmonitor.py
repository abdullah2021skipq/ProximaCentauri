import urllib3
import datetime
from cloudmatricdata import cloudmetric1
import constants as constants
from s3 import mywahedbuks3 as buk

# URL_TO_MONITOR='www.twitter.com'
# URL_MONITOR_NAMESPACE="waheedwebhealth"
# URL_MONIROR_NAME_AVAILABILITY= "url_availabiloty"
# URL_MONIROR_NAME_LATENCY= "url_latency"

def lambda_handler(events,context):
    cw= cloudmetric1();
     
    Url_Monitor= buk().bucket_as_list()
    
    values = dict()
    four_url_values  = []
    abc = 1
    for url in Url_Monitor:
        avail = get_availability(url)
        dimensions=[
        {'Name': 'URL', 'Value': url}
        ]
        cw.put_data(constants.URL_MONITOR_NAMESPACE , constants.URL_MONITOR_NAME_AVAILABILITY+'_'+url+ str(abc),dimensions,avail)
    

     #########Latency matrix 
    
        latency = get_latency(url)
        dimensions=[
        {'Name': 'URL', 'Value': url}
        ]
        cw.put_data(constants.URL_MONITOR_NAMESPACE, constants.URL_MONITOR_NAME_LATENCY+'_'+url+ str(a),dimensions,latency)
        
        a+=1
    
        values.update({"avaiability":avail, "Latency":latency})
        four_url_values.append(values)
    return four_url_values
    
    # avail= get_availability()   #now we are putting matrices to cloudwatch  
    # dimensions=[
    #     {'Name': 'URL' , 'Value':constants.URL_TO_MONITOR }
    #  #   {'Name': 'Region' , 'Value': "DUB"}
        
    #     ]
    # cw.put_data(constants.URL_MONITOR_NAMESPACE ,constants.URL_MONIROR_NAME_AVAILABILITY , dimensions,avail)
    
    
     
    # latency= get_latency()
    # dimensions=[
    #     {'Name': 'URL' , 'Value': constants.URL_TO_MONITOR }
    #  #   {'Name': 'Region' , 'Value': "DUB"}
        
    # ]
    # cw.put_data(constants.URL_MONITOR_NAMESPACE ,constants.URL_MONIROR_NAME_LATENCY ,dimensions, latency)
    
    
    # values.update({"Availability": avail,"Latency":latency})
    # return values

def get_availability():
    http=urllib3.PoolManager()
    response=http.request("GET", url )
    if response.status==200:
        return 1.0
    else:
        return 0.0
    
def get_latency():
    http=urllib3.PoolManager()
    start=datetime.datetime.now()
    response=http.request("GET",url)
    end=datetime.datetime.now()
    delta =end-start
    latencySecc=round(delta.microseconds * 0.000001,6)
    return latencySecc