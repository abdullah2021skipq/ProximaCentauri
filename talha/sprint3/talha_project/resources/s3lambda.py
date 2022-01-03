import boto3
import os

import s3bucket_url 
def lambda_handler(event,context):
    ### Reading URLs from file in S3 bucket
    value = dict()
    bucketname = event['Records'][0]['s3']['bucket']['name']
    filename = event['Records'][0]['s3']['object']['key']
    client = boto3.client('dynamodb')
    list_url=  s3bucket_url.read_url_list(bucketname,filename)
    ### Writing the URLs in the Dynamodb table for URLS
    tablename = os.getenv('table_name')#getting table name
    for url in list_url:
        client.put_item(TableName= tablename,Item={'URL':{'S' : url}}) 