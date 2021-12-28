import datetime
import urllib3
import json
import boto3
def lambda_handler(event,context):
    message = event["Records"][0]["Sns"]['Message']
    result = json.loads(message)
    metric_name = result['Trigger']['MetricName']
    time = result['StateChangeTime']
    region = "DUB"
    url = result['Trigger']['Dimensions'][0]['value']
    dynamodb = boto3.client('dynamodb')
    dynamodb.put_item(TableName="ayesha_table", Item={'metric_name':{'S':metric_name},'url':{'S':url},'region':{'S':region},'timestamp':{'S':time}})
    