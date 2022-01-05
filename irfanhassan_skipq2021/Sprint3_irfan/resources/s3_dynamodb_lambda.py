import boto3
import os
from s3bucket_read import s3bucket_read as bucket

def lambda_handler(event,context):
    value = dict()
############ getting bucket name and file name from even ###########################################################
    bucketname = event['Records'][0]['s3']['bucket']['name']
    filename = event['Records'][0]['s3']['object']['key']
#################getting url list from s3 bucket and writing into dynamo DB table ####################################
    client = boto3.client('dynamodb')
    list_url=bucket(bucketname,filename).bucket_as_list()
    tablename = os.getenv('table_name')#getting table name
    for url in list_url:
        client.put_item(TableName= tablename,Item={'URL':{'S' : url}}) #putting url from json file to dynamoDBimport boto3
