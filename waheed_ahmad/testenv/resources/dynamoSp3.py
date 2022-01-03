import boto3,os

from bucket import Bucket as bo 
from resources import s3 as s3
def lambda_handler(event, context):
    
    
    client = boto3.client('dynamodb')
    URLS = s3.read_buk("waheedbuc", "urls.json") 
    #info = json.loads(info)
    
    
    for url in URLS:
        client.put_item(
        TableName = "urltable",
        Item={'url website':{'S': url}
        })