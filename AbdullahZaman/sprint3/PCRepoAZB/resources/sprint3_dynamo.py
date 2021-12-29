import boto3,os
from resources import s3bucket
#import json

def lambda_handler(event, context):
    #write to dynamodb database
    URLs = s3bucket.read_file("abdullahzamanbucket", "urlsList.json")
    client_ = boto3.client('dynamodb')
    for U in URLs:
        item = {
            'URL_ADDRESS': {'S': U}
                }
        client_.put_item(TableName="AbdullahSprint3", Item=item)