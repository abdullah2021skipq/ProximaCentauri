import boto3,os
import json

client = boto3.client('dynamodb')
  
  
   ############################## Creating object for table  ###############################
  
def lambda_handler(event, context):
    client = boto3.client('dynamodb')
    message = event['Records'][0]['Sns']
    msg = json.loads(message['Message'])
    
    
    name = os.getenv('table_name')#getting table name


     ############################## Putting values in dynamo table###############################


    client.put_item(
    TableName = name,
    Item={
        'Timestamp':{'S' : message['Timestamp']},
        'Reason':{'S':msg['NewStateReason']},
        'URL':{'S':msg['Trigger']['Dimensions'][0]['value']}
    })