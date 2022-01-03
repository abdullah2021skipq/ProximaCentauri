import datetime
import urllib3
import constants as constants
from CW_putMetric import CloudWacthPutMetric
import s3bucket_url
def lambda_handler(events, context):
    values=dict()
#    print("My URLs list:", s3bucket_url.read_url_list())
    #creating an instant our CWPM class
    cw=CloudWacthPutMetric();
    for urltomonitor in s3bucket_url.read_url_list():
 #       print(urltomonitor," ")
        avail=get_availability(urltomonitor)
        dimensions=[
                { 'Name':'URL', 'Value': urltomonitor}
                ]
    #put the data to CW using put-metric-data(put_data) method
        cw.put_data(constants.URL_MONITOR_NAMESPACE, urltomonitor+constants.URL_MONITOR_NAME1A, dimensions,avail )
    #get value of latency
        latency=get_latency(urltomonitor)
    #put the data to CW using put-metric-data(put_data) method
        cw.put_data(constants.URL_MONITOR_NAMESPACE, urltomonitor+constants.URL_MONITOR_NAME1L, dimensions,latency )
    #to get the values of metrics updated
        values.update({"availability": avail, "Latency": latency})
    return values
def get_availability(urll):
    http=urllib3.PoolManager()
    response=http.request("GET", urll)
    if response.status==200:
        return 1.0
    else: return 0.0
def get_latency(urll):
    http=urllib3.PoolManager()
    start =datetime.datetime.now()
    response=http.request("GET", urll)
    end=datetime.datetime.now()
    dif=end-start
    latency=round(dif.microseconds * 0.000001,6)
    return latency



    