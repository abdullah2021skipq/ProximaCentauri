import boto3
import json
import constants as constant_
client = boto3.client('dynamodb')

def lambda_handler(event, context):
    #print(event)
    client = boto3.client('dynamodb')
    message = event['Records'][0]['Sns']
    msg = json.loads(message['Message'])
    client.put_item(
    TableName = constant_.table_name,
    Item={
        'Timestamp':{'S' : message['Timestamp']},
        'Reason':{'S':msg['NewStateReason']}
    })