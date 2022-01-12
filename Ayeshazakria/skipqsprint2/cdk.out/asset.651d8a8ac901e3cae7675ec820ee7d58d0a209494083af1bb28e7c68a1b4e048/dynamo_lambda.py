import datetime
import urllib3
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
    
    dynamodb = boto3.client('dynamodb')
    dynamodb.put_item(TableName='ayeshabetastage-sprint2projectinstance-DynamoTableB2B22E15-1P0XLWSL2GYCK', Item={'id':{'S':metric_name},'url':{'S':url},'region':{'S':region},'timestamp':{'S':time}})
    