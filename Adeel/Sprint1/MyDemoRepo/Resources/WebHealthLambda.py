import datetime
import urllib3

URL = "www.skipq.org"


def lambda_handler(event,context):
    values = dict()
    avail = get_availability()
    latancy = get_latency()
    values.update({
        "Availability":avail ,
        "Latancy":latancy
        
    })
    return values

def get_availability():
    http = urllib3.PoolManager()
    response = http.request("GET",URL)
    if response.status == 200:
        return 1.0
    else:
        return 0.0

def get_latency():
    http = urllib3.PoolManager()
    start = datetime.datetime.now()
    response = http.request("GET",URL)
    end = datetime.datetime.now()
    delta = end - start
    latancySec = round(delta.microseconds*0.000001 , 6)
    return latancySec
