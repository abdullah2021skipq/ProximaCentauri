import os 
import boto3
import json
from S3bucket import S3Bucket as sb

TABLE_PATH = '/TABLE'
BUCKET_PATH = '/BUCKET_LIST'

def lambda_handler(event, context):
    
    path = event['path']
    httpMethod = event['httpMethod']
    
    body = event['body']
    table_name = os.getenv("api_table_name")
    
    response = {}
    if path == BUCKET_PATH and httpMethod == 'PUT':
        
        bucket_name = event['queryStringParameters']["bucket_name"]
        object_key = event['queryStringParameters']["object_key"]
        response = bucket_to_table(bucket_name, object_key, table_name)
        
    if path == TABLE_PATH and httpMethod == 'GET':
        
        url_name = event['queryStringParameters']['url_name']
        response = fetch_url(table_name, url_name)
        
    else:
        response = {
                    "statusCode":200,
                    "body": "request failed"
                    }
   
    return response


def construct_response(msg):
    response = {
                "statusCode":200,
                "body": msg
               }
    return response

def bucket_to_table(bucket_name, object_key, table_name):
    
    URLS = sb(bucket_name).load(object_key)
    K=list(URLS['URLS'][0].keys())
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    
    for i in range(len(K)):
        table.put_item(Item = {'Name': K[i],
                               'URL': URLS['URLS'][0][K[i]]})
    
    msg = f"{len(K)} urls added/updated"
    return construct_response(msg)

    
def fetch_url(table_name, url_name):
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    
    URL = table.get_item(Key = {'Name': url_name})
    
    if 'Item' in URL:
        msg = URL['Item']['URL']
    else:
        msg = "Specified URL name does not exist"
    
    return construct_response(msg)
    