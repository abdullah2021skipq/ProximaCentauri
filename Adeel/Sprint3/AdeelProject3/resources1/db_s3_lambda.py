import boto3,os

from bucket import Bucket as bo 

client = boto3.client('dynamodb')

def lambda_handler(event, context):
    
    
    client = boto3.client('dynamodb')
    
    bucket_name = event['Records'][0]['s3']['bucket']['name']
    key = event['Records'][0]['s3']['bucket']['key']
    
    Url_Monitor= bo('adeelskipq','urls.json').bucket_as_list()
    
    table_name = os.getenv('table_name')#getting table name
    
    for link in Url_Monitor:
        client.put_item(
        TableName = table_name,
        Item={'Links':{'S': link}
        })