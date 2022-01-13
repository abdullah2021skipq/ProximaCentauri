import datetime
import urllib3
import constants as constant_
from cloud_watch import CloudWatch_PutMetric
from s3bucket_read import s3bucket_read as bucket

def lambda_handler(event,context):
    value = dict()
    cloudwatch = CloudWatch_PutMetric();
    list_url=bucket(constant_.bucket,constant_.file_name).bucket_as_list()
    for url in list_url:
        avail = availabilty_value(url)
        Dimensions=[{'Name': 'URL', 'Value': url}]
        cloudwatch.put_data(constant_.URL_NameSpace, constant_.URL_Aailibilty,Dimensions,avail)
        latency = latency_value(url)
        cloudwatch.put_data(constant_.URL_NameSpace, constant_.URL_Latency,Dimensions,latency)
        value.update({"availibility":avail,"latency":latency})
    return value
    
def availabilty_value(url):
    http = urllib3.PoolManager()
    response = http.request("GET", url)
    if response.status==200:
        return 1.0
    else:
        return 0.0
    

def latency_value(url):
    http = urllib3.PoolManager()
    begin = datetime.datetime.now()
    response = http.request("GET",url)
    end = datetime.datetime.now()
    duration = end - begin
    latency_sec = round(duration.microseconds * 0.000001,6)
    return latency_sec
    