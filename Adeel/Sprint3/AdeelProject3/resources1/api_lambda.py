import boto3,os
import db_ReadWrite_handler as dynamo_RW

client = boto3.client('dynamodb')

def lambda_handler(events, context):
    client = boto3.client('dynamodb')
    
    if events['httpMethod'] == 'GET':
        
        data = dynamo_RW.ReadFromTable(os.getenv(key = 'table_name'))
        response_msg = data
    
    elif events['httpMethod'] == 'PUT':
        
        
        new_url = event['body']
        client.put_item(
        TableName = os.getenv(key='table_name'),
        Item={
        'Links':{'S' : new_url},
        })
        response_msg = 'Url is successfully added into the table'
        
    elif events['httpMethod'] == 'DELETE':
    
        new_url = event['body']
        client.delete_item(
        TableName = os.getenv(key='table_name'),
        Item={
        'Links':{'S' : new_url},
        })
        response_msg = 'Url is successfully deleted from the table'
    else:
        
        response_msg = 'You can only put a item in table, delete it or get items from table'
        
    return{
        
        'statusCode' : 200
        'body'  :  response_msg
        
    }