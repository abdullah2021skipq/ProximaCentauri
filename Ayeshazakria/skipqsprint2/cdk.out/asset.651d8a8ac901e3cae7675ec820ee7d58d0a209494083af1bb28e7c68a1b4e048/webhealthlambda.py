import datetime
import urllib3
import constant as constants
from cloudwatch import Cloudwatchputmetrics
from uploadtobucket import get_file

def lambda_handler(event,context):
    urls = get_file("ayeshaskipqbucket","url_list.txt")
    values =dict()
    cw=Cloudwatchputmetrics()
    for url in urls:
        avail=get_availability(url)
        dimensions=[ 
        { "Name":"URL",
          "Value":url
        },
        {  "Name":"Region", 
           "Value":" DUB"
        }
        ]
        cw.put_data(url,"url_availability",dimensions,avail)
        latency=get_latency(url)
        dimensions=[ 
        { "Name":"URL",
          "Value":url
        },
        {  "Name":"Region", 
           "Value":" DUB" 
        }
        ]
    
        cw.put_data(url,"url_latency",dimensions,latency)
        values.update({"availability":avail, "Latency":latency})
    return values
    
def get_availability(url):
    http=urllib3.PoolManager()
    response = http.request("GET",url)
    if response.status==200:
        return 1.0
    else:
        return 0.0
def get_latency(url):
    http= urllib3.PoolManager()
    start=datetime.datetime.now()
    response = http.request("GET",url)
    end = datetime.datetime.now()
    delta=end-start
    latencySec=round(delta.microseconds * .000001,6)
    return latencySec

    