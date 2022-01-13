import boto3
import json

client = boto3.client('dynamodb')
  
  
   ############################## Creating object for table  ###############################
  
def lambda_handler(event, context):
   # db = boto3.resource('dynamodb')
    client = boto3.client('dynamodb')
    message = event['Records'][0]['Sns']
    msg = json.loads(message['Message'])
    #table_name = db.Table('AdeelAlarm')

     ############################## Putting values in dynamo table###############################
    
    client.put_item(
    TableName = 'AdeelAlarmdynamo',
    Item={
        'Timestamp':{'S' : message['Timestamp']},
        'Reason':{'S':msg['NewStateReason']},
        'URL':{'S':data['Trigger']['Dimensions'][0]['value']}
    })