import boto3
from resources import s3bucket
import time

def create_sprint3_table():
    client_ = boto3.resource('dynamodb')
    try:
        table = client_.create_table(
            TableName='AbdullahSprint3',
            KeySchema=[
                {
                    'AttributeName': 'URL_ADDRESS',
                    'KeyType': 'HASH'  # Partition key
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'URL_ADDRESS',
                    'AttributeType': 'S'
                }
    
            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 10,
                'WriteCapacityUnits': 10
            }
        )
        time.sleep(5)
    except:
        pass


def putting_sprint3_data():
    URLs = s3bucket.read_file("abdullahzamanbucket", "urlsList.json")
    client_ = boto3.client('dynamodb')
    for U in URLs:
        item = {
            'URL_ADDRESS': {'S': U}
                }
        print(item)
        client_.put_item(TableName="AbdullahSprint3", Item=item)