import json
from dynamo import dynamodbPut

def lambda_handler(events, context):
    db=dynamodbPut();
    message = events['Records'][0]['Sns']['Message']
    message = json.loads(message)
    parsed_message =  message['alarmID']
    createdDate = message['StateChangeTime']
    db.dynamo_data("alarmtable", parsed_message, createdDate)