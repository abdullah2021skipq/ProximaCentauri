import json
from db_putdata import dynamoTablePutData
import constants as constants
def lambda_handler(events, context):
    print(events)
    db = dynamoTablePutData();#creating an instance of my putdata class
    message = events['Records'][0]['Sns']['MessageId']
    message = json.loads(message)
    parsed_message =  message['AlarmName']
    createdDate = message['StateChangeTime']
   # reason=message['ReasonforStateChange']
    db.dynamo_data(constants.TABLE_NAME, parsed_message, createdDate)
