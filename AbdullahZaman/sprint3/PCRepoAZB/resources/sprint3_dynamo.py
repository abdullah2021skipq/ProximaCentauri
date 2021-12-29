import boto3
from resources import s3bucket

def create_sprint3_table():
    client_ = boto3.resource('dynamodb', region_name='us-east-2')
    try:
        table = client_.create_table(TableName='AbdullahSprint3',
                                KeySchema=[
                                {
                                'AttributeName': 'URL_ADDRESS',
                                'KeyType': 'HASH'
                                }
                    ],
                                AttributeDefinitions=[
                                {
                                'AttributeName': 'URL_ADDRESS',
                                'AttributeType' : 'S'
                                }
                                ]
                    )
    except:
        pass


def putting_sprint3_data():
    try:
        URLs = s3bucket.read_file("abdullahzamanbucket", "urlsList.json")
        client_ = boto3.client('dynamodb')
        for U in URLs:
            item = {
                'URL_ADDRESS': {'S': U}
                    }
            client_.put_item(TableName="AbdullahSprint3", Item=item)
    except:
        pass