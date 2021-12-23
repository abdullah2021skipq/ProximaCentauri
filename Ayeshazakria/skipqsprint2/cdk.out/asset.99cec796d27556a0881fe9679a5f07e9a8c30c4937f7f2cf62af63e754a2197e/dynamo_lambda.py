import datetime
import urllib3
import constant as constants
from cloudwatch import Cloudwatchputmetrics
import json
import boto3
def lambda_handler(event,context):
    message = event['Records'][0]["Sns"]['Message']
    result = json.loads(message)
    metric_name = result['Trigger']['MetricName']
    time = result['StateChangeTime']
    region = result['Trigger']['Dimensions'][0]['value']
    url = result['Trigger']['Dimensions'][1]['value']
    
    dynamodb = boto3.resource('dynamodb')
    data_table = dynamodb.Table('DynamoTable')
    dynamodb.put_item(TableName='DynamoTable', Item={'id':{'S':metric_name}})
    # why here.