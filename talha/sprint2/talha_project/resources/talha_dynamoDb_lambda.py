import json,os
from db_putdata import dynamoTablePutData
import constants as constants
def lambda_handler(events, context):
    print(events)
    db = dynamoTablePutData();#creating an instance of my putdata class
    message = events['Records'][0]['Sns'] #['Message']
    msggg = json.loads(message['Message'])
    parsed_message =  msggg['AlarmName']
    createdDate = message['Timestamp']#['StateChangeTime']
   # reason=message['ReasonforStateChange']
  #  if parsed_message[0]=="B":
   #    table_name="Beta-infraStack-TableCD117FA1-10BTARD7DGVYY"
    #else:
     #   table_name="Prod-infraStack-TableCD117FA1-Y8JNEH8OHXPY"
    table_name= os.environ['table_name'] #constants.TABLE_NAME
    db.dynamo_data(table_name,parsed_message, createdDate)
#constants.TABLE_NAME, 