import boto3
import os
import json

def lambda_handler(event,context):
    value = dict()
    client = boto3.client('dynamodb')
    #print(event)
    tablename = os.getenv('table_name')
    operation=event["httpMethod"]
    #print(operation)
    url=event['body']
    #print(url)
    response=""
    #https://dynobase.dev/dynamodb-python-with-boto3/#:~:text=To%20get%20all%20items%20from,the%20results%20in%20a%20loop
    if operation=="PUT":
        client.put_item(TableName= tablename,Item={'URL':{'S' : url}})
        response="The item has been successfully putted into DynamoDB table."
    elif operation=="DELETE":
        client.delete_item(TableName= tablename,Item={'URL':{'S' : url}}) #https://stackoverflow.com/questions/64187825/how-to-delete-all-the-items-in-the-dynamodb-with-boto3
        response="The item has been successfully deleted from DynamoDB table."
    elif operation=="GET":
        url_list=read_table(tablename)
        response="url is done"
    else:
        response="invalid request."
    
    return {'statusCode':200,'body':json.dumps(reponse)}   
    
    
    
    def read_table(table_name):
        client = boto3.client('dynamodb')
        table_data = client.scan(TableName=table_name,AttributesToGet=['URL'])
        return table_data
        
        