import boto3,os
import json

client = boto3.client('dynamodb')
  
  
   ############################## Creating object for table  ###############################
  
def lambda_handler(event, context):
   # db = boto3.resource('dynamodb')
    tables = ["Beta-adeelStack-BDtable331D4FEF-1VA4X6BOIHL36","Prod-adeelStack-BDtable331D4FEF-1TTSO0FY0P0ZE"]
    client = boto3.client('dynamodb')
    message = event['Records'][0]['Sns']
    msg = json.loads(message['Message'])
    
    if msg['AlarmName'][0] == 'P':
        table_name = tables[1]
    elif msg['AlarmName'][0] == 'B':
        table_name = tables[0]
        
    table_name2 = os.getenv('Table_Name')
    record = event['Records'][0]['dynamodb']
    arnText = record['eventSourceARN']
    listof = arnText.split('/')
    index = listof.index('stream')
    table_name1 = listof[index-1]
    print('--------------------')
    print(table_name1)
    print(table_name2)
    print('--------------------')

     ############################## Putting values in dynamo table###############################
    #table_name=os.getenv('table_name')
    client.put_item(
    TableName = table_name,
    Item={
        'Timestamp':{'S' : message['Timestamp']},
        'Reason':{'S':msg['NewStateReason']},
        'URL':{'S':msg['Trigger']['Dimensions'][0]['value']}
    })