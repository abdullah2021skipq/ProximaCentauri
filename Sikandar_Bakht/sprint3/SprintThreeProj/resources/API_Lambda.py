import os 
import boto3
import json
from S3bucket import S3Bucket as sb
import botocore
from boto3.dynamodb.conditions import Attr

TABLE_PATH = '/TABLE'
BUCKET_PATH = '/BUCKET_LIST'

def lambda_handler(event, context):
    
    path = event['path']
    httpMethod = event['httpMethod']
    
    body = event['body']
    table_name = os.getenv("api_table_name")
    print(event)
    response = {}
    if path == BUCKET_PATH and httpMethod == 'PUT':
        
        bucket_name = event['queryStringParameters']["bucket_name"]
        object_key = event['queryStringParameters']["object_key"]
        response = bucket_to_table(bucket_name, object_key, table_name)
        
    elif path == TABLE_PATH and httpMethod == 'GET':
        
        url = event['queryStringParameters']['url']
        response = fetch_url(table_name, url)
        
    elif path == TABLE_PATH and httpMethod == 'POST':
        
        url_name = event['queryStringParameters']['url_name']
        new_url = event['queryStringParameters']['url']
        
        response = add_url(table_name, url_name, new_url)
        
    elif path == TABLE_PATH and httpMethod == 'PUT':
        
        url_to_update = event['queryStringParameters']['url']
        url_name = event['queryStringParameters']['url_name']
        
        body = json.loads(event['body'])
        updated_url_name = body['updated_url_name']
        updated_url = body['updated_url']
        response = update_url(table_name, url_name, url_to_update, updated_url_name, updated_url)
    
    elif path == TABLE_PATH and httpMethod == 'DELETE':
        
        print(event)
        url_name = event['queryStringParameters']['url_name']
        url_del = event['queryStringParameters']['url']
        response = delete_url(table_name, url_name, url_del)   

    else:
        print(event)
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
        table.put_item(Item = {
                                'URL': URLS['URLS'][0][K[i]],
                                'Name': K[i]})
    
    msg = f"{len(K)} urls added/updated"
    return construct_response(msg)

    
def fetch_url(table_name, url):
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    
    URL = table.get_item(Key = {'URL': url})
    
    if 'Item' in URL:
        msg = URL['Item']['Name'] + ": " + URL['Item']['URL'] 
    else:
        msg = "Specified URL name does not exist"
    
    return construct_response(msg)
    
def add_url(table_name, url_name, new_url):
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    
    try:
        table.put_item (Item = {'URL': new_url,
                                'Name' : url_name
                              },
                        ConditionExpression=Attr('URL').ne(new_url)
                        )
        msg = f'''
            URL Name: {url_name}
            URL: {new_url}
        '''               
        
    except botocore.exceptions.ClientError as e:
    
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            
            msg = f'URL: {new_url} already exists'
            
    return construct_response(msg)
    
def delete_url(table_name, url_name, url_del):
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    
    try:
        table.delete_item (Key = {'URL': url_del,
                              },
                        ConditionExpression=Attr('URL').eq(url_del)
                        )
        msg = f'''
            Deleted
            URL Name: {url_name}
            URL: {url_del}
        '''               
        
    except botocore.exceptions.ClientError as e:
    
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            
            msg = f'URL: {url_del} does not exist'
            
    return construct_response(msg)
    
def update_url(table_name, url_name, url_to_update, updated_url_name, updated_url):
    
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    msg = ''
    
    try:
        table.delete_item (Key = {'URL': url_to_update,
                              },
                        ConditionExpression=(Attr('URL').eq(url_to_update) & Attr('URL').ne(updated_url))
                        )
        
    except botocore.exceptions.ClientError as e:
    
        if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
            
            msg = f'URL: {url_to_update} does not exist'
    
    if msg != f'URL: {url_to_update} does not exist':
        try:
            table.put_item (Item = {'URL': updated_url,
                                    'Name' : updated_url_name
                                  },
                            ConditionExpression=Attr('URL').ne(updated_url)
                            )
            msg = f'''
            Update from:
                URL: {url_to_update}
                URL Name: {url_name}
            to:  
                URL Name: {updated_url_name}
                URL: {updated_url}
            '''               
            
        except botocore.exceptions.ClientError as e:
        
            if e.response['Error']['Code'] == 'ConditionalCheckFailedException':
                
                msg = f'URL: {updated_url} already exists'
            
    return construct_response(msg)