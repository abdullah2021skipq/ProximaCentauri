from aws_cdk import aws_iam
import boto3
from resources import s3
import time

def create_s3_table():
    client_ = boto3.resource('dynamodb')
    try:
        table = client_.create_table(
            TableName='waheeds3table',
            KeySchema=[
                {
                    'AttributeName': 'URLLL',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'URLLL',
                    'AttributeType': 'S'
                }
    
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )
    except:
        pass


def putting_data():
    URLS = s3.read_file("waheedbuc", "urlsList.json")
    client_ = boto3.client('dynamodb')
    for url in URLS:
        item = {
            'URL_ADDRESS': {'S': url}
                }
        print(item)
        client_.put_item(TableName="waheeds3table", 
                        Item=item)