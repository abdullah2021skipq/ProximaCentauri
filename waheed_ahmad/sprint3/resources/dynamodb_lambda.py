import json
import boto3
import os
#from dynamo import dynamodbPut
client = boto3.client('dynamodb')
def lambda_handler(events, context):
    
    message = event['Records'][0]['Sns']
    parsed_msg = json.loads(message['Message'])
    
    name = os.getenv('table_name')
    
    
    client.dynamodbPut(
        TableName = name,
        Item={
            'Timestamp':{'S' : message['Timestamp']},
            'Reason':{'S':parsed_msg['NewStateReason']},
            'URL':{'S':parsed_msg['Trigger']['Dimensions'][0]['value']}
        })