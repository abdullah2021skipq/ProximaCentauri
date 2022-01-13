import json
import boto3
import os
#from dynamo import dynamodbPut

def lambda_handler(events, context):
    client = boto3.client('dynamodb')
    msg1 = event['Records'][0]['Sns']['MessageId']
    msg2 = event['Records'][0]['Sns']['Timestamp']
    
    name = os.getenv('table_name')
    
    
    client_.put_item(
        TableName = name,
        Item={
            'alarmdetails':{'S' : msg1},
            'timestamp':{'S': msg2}
        #     'URL':{'S':parsed_msg['Trigger']['Dimensions'][0]['value']}
         })