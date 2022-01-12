import datetime
import urllib3
import os
import constants as constant_
from cloud_watch import CloudWatch_PutMetric
#from s3bucket_read import s3bucket_read as bucket
from tablescan import tablescan 
from s3bucket_read import s3bucket_read as bucket

#lambda function will invoke after each 1 minutes(periodic) #########################################
def lambda_handler(event,context):
    value = dict()
    tablename = os.getenv('table_name') #getting url table name 
    cloudwatch = CloudWatch_PutMetric();    #creating cloudwatch instance
    dbscan=tablescan()
#    list_url=dbscan.read_table(tablename)    #getting url list from url table
    list_url=bucket(constant_.bucket,constant_.file_name).bucket_as_list()
    
    ########################### creating metrics for each webpage ######################################
    for url in list_url:
        avail = availabilty_value(url)
        Dimensions=[{'Name': 'URL', 'Value': url}]
        cloudwatch.put_data(constant_.URL_NameSpace, constant_.URL_Aailibilty,Dimensions,avail)
        latency = latency_value(url)
        cloudwatch.put_data(constant_.URL_NameSpace, constant_.URL_Latency,Dimensions,latency)
        value.update({"availibility":avail,"latency":latency})
    return value
    
    
########### function to get availbilyti of url #############################################    
def availabilty_value(url):
    http = urllib3.PoolManager()
    response = http.request("GET", url)
    if response.status==200:
        return 1.0
    else:
        return 0.0
    
################# getting latency of webpage ##################################################
def latency_value(url):
    http = urllib3.PoolManager()
    begin = datetime.datetime.now()
    response = http.request("GET",url)
    end = datetime.datetime.now()
    duration = end - begin
    latency_sec = round(duration.microseconds * 0.000001,6)
    return latency_sec
    