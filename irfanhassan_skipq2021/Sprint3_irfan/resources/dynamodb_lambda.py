import boto3
import os
import json
import constants as constant_

def lambda_handler(event, context):
    #print(eveny)
    client = boto3.client('dynamodb')
    
######### getiing timssetamp && message details fromm even(alarm)  #########################
    message = event['Records'][0]['Sns']
    msg = json.loads(message['Message'])  
    reason = msg['NewStateReason']
    timestamp=message['Timestamp']
####### getting name of table ##############################################################
    
    tablename = os.getenv('table_name')#getting table name

    #print(reason)
########### puuting Item in dynamo DB ####################################################3
    client.put_item(TableName= tablename,Item={'Timestamp':{'S' : timestamp}, 'Reason':{'S':reason} })
        



    