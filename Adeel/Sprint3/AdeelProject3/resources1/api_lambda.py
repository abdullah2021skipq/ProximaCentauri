import boto3,os


client = boto3.client('dynamodb')

def lambda_handler(events, context):
    client = boto3.client('dynamodb')
    
    if events['httpMethod'] == 'GET':
    
    elif events['httpMethod'] == 'PUT':
        
    elif events['httpMethod'] == 'DELETE':
    
    